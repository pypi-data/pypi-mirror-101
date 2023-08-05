from docstring_parser import parse
from mate.modules.core import MateModule, command
from mate.utils.colors import magenta
from mate.config import mate_config
from mate import add_plugins


def get_help(module, inline=None):
    results = {}
    module_path = module.get_path()
    if inline is not None:
        doc = parse(module.INLINE_SUBMODULES[inline].__doc__)
        desc = doc.short_description or "No description provided."
        cmd_path = " ".join(module_path + [inline]).strip()
        results[cmd_path] = "-- " + desc
        return results
    # print description of inline submodules
    for m in module.INLINE_SUBMODULES:
        doc = parse(module.INLINE_SUBMODULES[m].__doc__)
        desc = doc.short_description or "No description provided."
        cmd_path = " ".join(module_path + [m]).strip()
        results[cmd_path] = "-- " + desc
    # print description of submodules
    for m in module.get_modules():
        doc = parse(m.INLINE_SUBMODULES[""].__doc__)
        desc = doc.short_description or "No description provided."
        cmd_path = " ".join(m.get_path()).strip()
        results[cmd_path] = "-- " + desc

    return dict(sorted(results.items()))


class MateHelp(MateModule):
    @command()
    def help_default(self, *args):
        """Print list of commands."""
        if len(args) == 0:
            module = mate_config.module_record
        else:
            module = (
                mate_config.module_record.get_module_by_path(args)
                or mate_config.module_record
            )

            if list(args) == module.get_path():
                return get_help(module)
            elif (
                len(args) - len(module.get_path()) == 1
                and args[-1] in module.INLINE_SUBMODULES
            ):
                return get_help(module, args[-1])
            else:
                # let modules handle its MateUndefined
                return mate_config.module_record.parse_command(list(args))

        return get_help(module)


add_plugins([MateHelp("help")])
