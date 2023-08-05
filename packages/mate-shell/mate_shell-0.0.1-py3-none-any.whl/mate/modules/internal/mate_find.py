from mate import MateModule, command, add_plugins


class MateFind(MateModule):
    @command()
    def find_default(self):
        """Generic command to find various artifacts."""
        return "Executing Find."


add_plugins(modules=[MateFind("find")])
