from mate import MateModule, command, add_plugins
from mate.utils.colors import magenta
from mate.config import mate_config


class MateShow(MateModule):
    @command()
    def show_default(self):
        """Generic command for showing things about mate."""
        return "Executing Show."

    @command(option="all")
    def show_all(self):
        """Shows everything."""
        results = {}
        results["Version:"] = str(mate_config.mate_version)
        results["Author:"] = str(mate_config.mate_author)
        results["Project Directory:"] = str(mate_config.project_dir)
        results["Output Directory:"] = str(mate_config.output_dir)
        return results

    @command(option="mate")
    def show_mate(self):
        """Shows mate's details."""
        results = {}
        results["Version:"] = str(mate_config.mate_version)
        results["Author:"] = str(mate_config.mate_author)
        return results

    @command(option="context")
    def show_context(self):
        """Shows current running context."""
        results = {}
        results["Project Directory:"] = str(mate_config.project_dir)
        results["Output Directory:"] = str(mate_config.output_dir)
        return results


add_plugins(modules=[MateShow("show")])
