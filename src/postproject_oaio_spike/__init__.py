"""OpenAssetIO discovery hook for the Manager validation."""

from openassetio.pluginSystem import PythonPluginSystemManagerPlugin


class Plugin(PythonPluginSystemManagerPlugin):
    """Create a fresh validation interface for each Manager instance."""

    @staticmethod
    def identifier():
        return "org.postproject.manager-validation"

    @classmethod
    def interface(cls):
        from .manager import Interface

        return Interface()


openassetioPlugin = Plugin
