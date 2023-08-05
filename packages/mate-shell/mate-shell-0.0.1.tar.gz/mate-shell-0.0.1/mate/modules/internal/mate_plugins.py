import datetime
from mate import MateModule, command, add_plugins
from mate.config import mate_config


class MateShowPlugins(MateModule):
    @command()
    def show_plugins(self):
        """List loaded plugins."""
        results = {}
        for m in mate_config.plugin_manager.list_name_plugin():
            if "mate.modules." not in m[0]:
                results[m[0]] = m[1]
        return results


@command(option="time")
def show_time(self):
    return str(datetime.datetime.now())


add_plugins(modules=[MateShowPlugins("plugins"), show_time], parent="show")
