"""OpenAssetIO discovery hook for the disposable Manager spike."""

from openassetio.pluginSystem import PythonPluginSystemManagerPlugin


class Plugin(PythonPluginSystemManagerPlugin):
    """Create a fresh spike interface for each Manager instance."""

    @staticmethod
    def identifier():
        return "org.postproject.manager-spike"

    @classmethod
    def interface(cls):
        from .manager import Interface

        return Interface()


openassetioPlugin = Plugin

