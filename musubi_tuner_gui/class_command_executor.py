import os
import subprocess
import psutil
import threading
import collections
import time
import sys
import gradio as gr

from .custom_logging import setup_logging
from .tj_i18n import t, get_language, DEFAULT_LANG

# Set up logging
log = setup_logging()


class CommandExecutor:
    """
    A class to execute and manage commands.
    """

    def __init__(self, headless: bool = False, config=None):
        """
        Initialize the CommandExecutor.
        """
        self.headless = headless
        self.process = None
        lang = get_language(config) if config is not None else DEFAULT_LANG

        # Live output capture for the "실시간 학습 로그" viewer (tj_projects_gui.py):
        # a bounded in-memory ring buffer of recent stdout/stderr lines, plus an
        # optional append-only log file for the current run.
        self.log_lines = collections.deque(maxlen=4000)
        self._log_lock = threading.Lock()
        self._log_file = None
        self._pump_thread = None

        self.button_run = gr.Button(
            t("ce_start_training_button", lang), variant="primary", scale=1
        )

        self.button_stop_training = gr.Button(
            t("ce_stop_training_button", lang),
            visible=self.process is not None or headless,
            variant="stop",
            scale=1,
        )

    def _pump_output(self, proc, log_file_path):
        log_fh = None
        if log_file_path:
            try:
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
                log_fh = open(log_file_path, "a", encoding="utf-8", errors="replace")
                log_fh.write(f"\n===== run started {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
            except Exception as e:
                log.warning(f"Could not open training log file {log_file_path}: {e}")
                log_fh = None
        try:
            for line in iter(proc.stdout.readline, ""):
                if line == "":
                    break
                # Still show it in this GUI process's own console (unchanged behavior).
                try:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                except Exception:
                    pass
                with self._log_lock:
                    self.log_lines.append(line.rstrip("\n"))
                if log_fh:
                    try:
                        log_fh.write(line)
                        log_fh.flush()
                    except Exception:
                        pass
        except Exception as e:
            with self._log_lock:
                self.log_lines.append(f"[log capture error: {e}]")
        finally:
            if log_fh:
                log_fh.close()

    def get_recent_log(self, n: int = 200) -> str:
        """Returns the tail of captured output, or "" if nothing has been
        captured yet. Callers render their own localized placeholder for the
        empty case rather than this returning one, so log text is never
        matched against a fixed (and language-dependent) sentinel string."""
        with self._log_lock:
            lines = list(self.log_lines)[-n:]
        return "\n".join(lines)

    def execute_command(self, run_cmd: str, log_file: str = None, **kwargs):
        """
        Execute a command if no other command is currently running.

        Parameters:
        - run_cmd (str): The command to execute.
        - log_file (str): Optional path to also append captured stdout/stderr to.
        - **kwargs: Additional keyword arguments to pass to subprocess.Popen.
        """
        if self.process and self.process.poll() is None:
            log.info("The command is already running. Please wait for it to finish.")
        else:
            # for i, item in enumerate(run_cmd):
            #     log.info(f"{i}: {item}")

            # Reconstruct the safe command string for display
            command_to_run = " ".join(run_cmd)
            log.info(f"Executing command: {command_to_run}")

            with self._log_lock:
                self.log_lines.clear()

            # Execute the command securely, capturing stdout/stderr so the GUI can
            # tail it live while still relaying every line to this process's own
            # console (same visible behavior as before).
            self.process = subprocess.Popen(
                run_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                **kwargs,
            )
            self._pump_thread = threading.Thread(
                target=self._pump_output, args=(self.process, log_file), daemon=True
            )
            self._pump_thread.start()
            log.debug("Command executed.")

    def kill_command(self):
        """
        Kill the currently running command and its child processes.
        """
        if self.is_running():
            try:
                # Get the parent process and kill all its children
                parent = psutil.Process(self.process.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                log.info("The running process has been terminated.")
            except psutil.NoSuchProcess:
                # Explicitly handle the case where the process does not exist
                log.info(
                    "The process does not exist. It might have terminated before the kill command was issued."
                )
            except Exception as e:
                # General exception handling for any other errors
                log.info(f"Error when terminating process: {e}")
        else:
            self.process = None
            log.info("There is no running process to kill.")

        return gr.Button(visible=True), gr.Button(visible=False or self.headless)

    def wait_for_training_to_end(self):
        while self.is_running():
            time.sleep(1)
            log.debug("Waiting for training to end...")
        log.info("Training has ended.")
        return gr.Button(visible=True), gr.Button(visible=False or self.headless)

    def is_running(self):
        """
        Check if the command is currently running.

        Returns:
        - bool: True if the command is running, False otherwise.
        """
        return self.process is not None and self.process.poll() is None
