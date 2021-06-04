import subprocess
import sys
from threading import Lock, Thread
from time import sleep

from psutil import NoSuchProcess, Process

from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.dynamic.security.exit_handler import ExitHandler


class ProcessWrapper:
    def check_alive(self):
        if self._alive and self.process.returncode is not None:
            self._alive = False

    def check_pipe(self, read_pipe, write_pipe, write_stdout=False, write_stderr=False):
        while not self.is_finished():
            try:
                new_output = read_pipe.read(1)
            except ValueError:
                self.check_alive()
                continue

            if len(new_output) == 0:
                self._alive = False
                self.terminate()
                continue

            try:
                write_pipe.write(new_output)
            except ExitException:
                self._alive = False
                self.terminate()
                continue

            if write_stdout:
                self.stdout += new_output

            if write_stderr:
                self.stderr += new_output

            self.check_alive()

    def check_stdout(self):
        self.check_pipe(self.process.stdout, sys.stdout, write_stdout=True)

    def check_stderr(self):
        self.check_pipe(self.process.stderr, sys.stderr, write_stderr=True)

    def check_cpuload(self):
        while self._alive:
            try:
                cpu_load = self.ps.cpu_percent()
                self.cpu_load_history.append(cpu_load)
                if len(self.cpu_load_history) > self.cpu_load_length:
                    self.cpu_load_history.pop(0)
            except NoSuchProcess:
                self._alive = False
                break
            sleep(0.01)
            self.check_alive()

    def is_waiting_input(self) -> bool:
        return len(self.cpu_load_history) == self.cpu_load_length and sum(self.cpu_load_history) < 1

    def register_input_request(self):
        if not self.is_waiting_input():
            raise RuntimeError('Program is not waiting for the input')
        self.cpu_load_history = []

    def is_finished(self):
        if not self.check_early_finish:
            return not self._alive

        else:
            if not self._alive:
                return True

            try:
                is_running = self.ps.status() == 'running'
                if not is_running:
                    self._alive = False
                return not is_running
            except NoSuchProcess:
                self._alive = False
                return True

    def __init__(self, *args, check_early_finish=False):
        self.lock = Lock()

        self.process = subprocess.Popen(
            [str(a) for a in args],
            bufsize=0,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding='utf-8',
        )

        self.ps = Process(self.process.pid)

        self.cpu_load = self.ps.cpu_percent()
        self.cpu_load_history = []
        self.cpu_load_length = 10

        self.stdout = ''
        self.stderr = ''
        self._alive = True
        self.terminated = False
        self.check_early_finish = check_early_finish

        Thread(target=lambda: self.check_cpuload(), daemon=True).start()
        Thread(target=lambda: self.check_stdout(), daemon=True).start()
        Thread(target=lambda: self.check_stderr(), daemon=True).start()

    def terminate(self):
        OutputHandler.print('Terminate called')

        with self.lock:
            OutputHandler.print('Terminate - LOCK ACQUIRED')

            if not self.terminated:
                OutputHandler.print('Terminate - BEFORE WAIT STDERR')

                self.wait_output()

                OutputHandler.print('Terminate - AFTER WAIT STDERR')

                self._alive = False

                OutputHandler.print('Terminate - SELF ALIVE == FALSE')

                is_exit_replaced = ExitHandler.is_replaced()
                if is_exit_replaced:
                    ExitHandler.revert_exit()
                    OutputHandler.print('Terminate - EXIT REVERTED')

                try:
                    parent = Process(self.process.pid)
                    OutputHandler.print(f'Terminate - parent == {parent}')
                    for child in parent.children(recursive=True):
                        OutputHandler.print(f'Terminate - child kill {child}')
                        child.kill()
                    OutputHandler.print(f'Terminate - parent kill {parent}')
                    parent.kill()
                except NoSuchProcess:
                    OutputHandler.print(f'Terminate - NO SUCH PROCESS')
                    pass
                finally:
                    OutputHandler.print(f'Terminate - finally before kill')
                    self.process.kill()
                    OutputHandler.print(f'Terminate - finally before wait')
                    self.process.wait()

                    self.process.stdout.close()
                    self.process.stderr.close()
                    self.process.stdin.close()

                    if is_exit_replaced:
                        ExitHandler.replace_exit()
                        OutputHandler.print(f'Terminate - EXIT REPLACED AGAIN')

                self.terminated = True
                OutputHandler.print(f'Terminate - TERMINATED')
        OutputHandler.print(f'Terminate - finished')

    def wait_output(self):
        iterations = 50
        sleep_time = 50 / 1000

        curr_stdout = self.stdout
        curr_stderr = self.stderr
        while iterations != 0:
            sleep(sleep_time)
            if self.stderr == curr_stderr and self.stdout == curr_stdout:
                break
            curr_stderr = self.stderr
            curr_stdout = self.stdout
            iterations -= 1

    def is_error_happened(self) -> bool:
        return (
            not self._alive and len(self.stderr) > 0
            or 'Traceback' in self.stderr
        )
