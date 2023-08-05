import pluggy
import sys
import inspect

hookspec = pluggy.HookspecMarker("mate")
hookimpl = pluggy.HookimplMarker("mate")


@hookspec
def mate_add_modules(modules=[], parent=None):
    """Prototype of module/plugin collection function."""


def add_plugins(modules=[], parent=None):
    @hookimpl
    def mate_add_modules(modules=modules, parent=parent):
        """Responsible to collect all modules and plugins.

        Returns:
            list: Contains MateModules to be added in MateRecord.
        """
        for module in modules:
            module.__parent = parent
        return modules

    frame = inspect.currentframe()
    target = sys.modules[frame.f_back.f_locals["__name__"]]
    target.mate_add_modules = mate_add_modules
