# coding=utf-8
"""
This package contains the language-server code-editor widget
"""
import sys
from pyqode.core import api, modes, panels
from pyqode.language_server.backend import server, workers
from pyqode.language_server import modes as lsp_modes


class LanguageServerCodeEdit(api.CodeEdit):
    
    language_server_command = None  # Specified in subclasses
    language_identifier = None

    def __init__(
        self,
        parent=None,
        server_script=server.__file__,
        interpreter=sys.executable,
        args=None,
        create_default_actions=True,
        reuse_backend=True
    ):

        super().__init__(
            parent=parent,
            create_default_actions=create_default_actions
        )
        self._create_default_actions = create_default_actions
        if args is None:
            args = []
        self.backend.start(
            server_script,
            interpreter,
            args + [
                '--command', self.language_server_command,
                '--langid', self.language_identifier
            ],
            reuse=reuse_backend
        )
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(lsp_modes.CalltipsMode())
        self.modes.append(lsp_modes.DiagnosticsMode())
        self.panels.append(panels.CheckerPanel())
        self.panels.append(
            panels.GlobalCheckerPanel(),
            panels.GlobalCheckerPanel.Position.RIGHT
        )

    def clone(self):
        
        return self.__class__(
            parent=self.parent(),
            server_script=self.backend.server_script,
            interpreter=self.backend.interpreter,
            args=self.backend.args,
            create_default_actions=self._create_default_actions
        )
        
    def setPlainText(self, *args, **kwargs):
        
        super().setPlainText(*args, **kwargs)
        self.backend.send_request(
            workers.open_document,
            {
                'code': self.toPlainText().replace(u'\u2029', u'\n'),
                'path': self.file.path,
            }
        )

    def __repr__(self):
        
        return '{}(path={})'.format(self.__class__.__name__, self.file.path)


class RCodeEdit(LanguageServerCodeEdit):
    
    mimetypes = ['text/x-r', 'text/x-R']
    language_server_command = 'R --slave -e "languageserver::run()"'
    language_identifier = 'r'
    language = 'R'

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self._word_separators.remove('.')
