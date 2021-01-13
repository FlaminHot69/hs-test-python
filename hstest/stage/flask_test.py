from urllib.request import urlopen

from hstest.common.utils import clean_text
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.exception.outcomes import UnexpectedError
from hstest.stage.stage_test import StageTest
from hstest.test_case.attach.flask_settings import FlaskSettings
from hstest.testing.runner.flask_application_runner import FlaskApplicationRunner
from hstest.testing.settings import Settings


class FlaskTest(StageTest):
    runner = FlaskApplicationRunner
    attach: FlaskSettings = FlaskSettings()

    def __init__(self, source_name: str = ''):
        super().__init__(source_name)
        loop_detector.working = False
        Settings.do_reset_output = False

        if self.source_name:
            if type(self.source_name) == str:
                self.attach.sources += [(self.source_name, None)]
            elif type(self.source_name) == tuple:
                self.attach.sources += [self.source_name]
            elif type(self.source_name) == list:
                self.attach.sources += self.source_name

    def get_url(self, source: None):
        create_url = lambda port: f'http://localhost:{port}/'

        if len(self.attach.sources) == 1:
            return create_url(self.attach.sources[0][1])
        elif len(self.attach.sources) == 0:
            raise UnexpectedError(f'Cannot find sources')

        sources_fits = [i for i in self.attach.sources if i[0] == source]
        if len(sources_fits) == 0:
            raise UnexpectedError(f'Bad source: {source}')
        elif len(sources_fits) > 1:
            raise UnexpectedError(f'Multiple sources ({len(sources_fits)}) found: {source}')

        return create_url(sources_fits[1])

    def get(self, link: str, source: None) -> str:
        if link.startswith('/'):
            link = link[1:]

        if not link.startswith('http://'):
            link = self.get_url(source) + link

        return clean_text(urlopen(link).read().decode())
