from typing import Callable, List, Optional
from hstest.dynamic.handle import StdoutHandler
from hstest.check_result import CheckResult
from hstest.exceptions import TestPassedException
from hstest.exceptions import WrongAnswerException
from hstest.utils import normalize_line_endings

InputFunction = Callable[[str], object]


class DynamicInputFunction:
    def __init__(self, trigger_count: int, func: InputFunction):
        self.trigger_count = trigger_count
        self.input_function = func


class InputMock:
    def __init__(self):
        self.input_lines: List[str] = []
        self.input_text_funcs: List[DynamicInputFunction] = []

    def provide_text(self, text: str):
        texts = [DynamicInputFunction(1, lambda t, saved=text: saved)]
        self.set_texts(texts)

    def set_texts(self, texts: List[DynamicInputFunction]):
        self.input_lines = []
        self.input_text_funcs = texts

    def readline(self):

        # todo check test run and throw EOFError

        next_line = self.eject_next_line()
        if next_line is not None:
            return next_line

        raise EOFError('EOF when reading a line')

    def eject_next_line(self) -> Optional[str]:
        if len(self.input_lines) == 0:
            self.input_lines = self.eject_next_input()
            if len(self.input_lines) == 0:
                return None

        next_line = self.input_lines.pop(0) + '\n'
        StdoutHandler.inject_input('> ' + next_line)

    def eject_next_input(self) -> List[str]:
        if len(self.input_text_funcs) == 0:
            return []

        input_function = self.input_text_funcs[0]
        if input_function.trigger_count > 0:
            input_function.trigger_count -= 1

        curr_output = StdoutHandler.get_partial_output()
        next_func = input_function.input_function

        new_input: str = ''
        try:
            obj = next_func(curr_output)
            if isinstance(obj, str):
                new_input = obj
            elif isinstance(obj, CheckResult):
                if obj.result:
                    raise TestPassedException()
                else:
                    raise WrongAnswerException(obj.feedback)
        except BaseException as ex:
            # todo add test run
            pass

        if input_function.trigger_count == 0:
            self.input_text_funcs.pop(0)

        new_input = normalize_line_endings(new_input)
        return new_input.split('\n')
