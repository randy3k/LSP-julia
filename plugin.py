from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig

import subprocess
import sublime
import os


def julia_pkg_dir():
    if sublime.platform() == "windows":
        # make sure console does not come up
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        startupinfo = None

    return subprocess.check_output(
        ["julia", "-e", "import LanguageServer; print(dirname(dirname(pathof(LanguageServer))))"],
        startupinfo=startupinfo
    ).decode("utf-8")


class LspJuliaPlugin(LanguageHandler):
    name = "julials"

    def __init__(self):
        if sublime.platform == "windows":
            command = [
                "julia",
                "--startup-file=no",
                "--history-file=no",
                "-e",
                "using LanguageServer;" +
                "import SymbolServer;" +
                "server = LanguageServer.LanguageServerInstance(stdin, stdout, false);" +
                "server.runlinter = true;" +
                "run(server);"
            ]
        else:
            command = [
                "bash",
                os.path.join(julia_pkg_dir(), "contrib", "languageserver.sh")
            ]

        self._config = ClientConfig(
            name=self.name,
            binary_args=command,
            tcp_port=None,
            scopes=["source.julia"],
            syntaxes=["Packages/Julia/Julia.sublime-syntax"],
            languageId='julia',
            enabled=False,
            init_options=dict(),
            settings={"runlinter": True},
            env=dict()
        )

    @property
    def config(self):
        return self._config

    def on_start(self, window):
        return True
