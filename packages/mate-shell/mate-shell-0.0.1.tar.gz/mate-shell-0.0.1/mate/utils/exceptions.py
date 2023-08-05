import functools
from mate.utils.colors import red
from mate.config import mate_config


def mate_exception_handler(func):
    """Mate's fallback exception handler as a decorator.

    Args:
        func (function): Function on which decorator was specified.

    Returns:
        function: Argument function will be wrapped in a try/except and
        returned.
    """

    @functools.wraps(func)
    def tmp_func(self, inline_submodule_name, *args):
        try:
            return func(self, inline_submodule_name, *args)
        except TypeError:
            # if self.get_path() == ["help"]:
            #     self = (
            #         mate_config.module_record.get_module_by_path([inline_submodule_name] + list(args))
            #         or mate_config.module_record
            #     )
            #     inline_submodule_name = args[0]
            #     args = args[1:]
            if inline_submodule_name in self.INLINE_SUBMODULES:
                original_command = " ".join(
                    self.get_path() + [inline_submodule_name]
                ).strip()
                extra_command = args[0]
            else:
                original_command = " ".join(self.get_path()).strip()
                extra_command = inline_submodule_name

            if original_command == "":
                print(red(f'Undefined command: "{extra_command}". ' f'Try "help".'))
            else:
                print(
                    red(
                        f'Undefined {original_command} command: "{extra_command}". '
                        f'Try "help {original_command}".'
                    )
                )
            return False

    return tmp_func


class MateUndefined(TypeError):
    """Because we don't want to catch all TypeErrors.

    Args:
        TypeError ([type]): [description]
    """

    pass
