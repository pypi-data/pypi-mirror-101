import sys
import shlex
import pluggy
import logging
import argparse
import sentry_sdk

from mate.config import mate_config

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal

from mate.libs import mate_hookspecs
from mate.utils.logger import log, shellLogHandler
from mate.utils.colors import red, yellow, green
from mate.modules.core import MateRecord
from mate.modules.internal import *
from mate.__version__ import __version__


bindings = KeyBindings()


@bindings.add("c-d")
def _(event):
    def take_it_easy():
        print(red("Try Ctrl-C maybe?"))

    run_in_terminal(take_it_easy)


sentry_sdk.init(
    "https://14832cd3088d43c699774d79cf9fa774@o481905.ingest.sentry.io/5704793",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


def get_plugin_manager():
    """Initializes plugin manager and registers plugin library.

    Returns:
        pm: plugin manager
    """
    pm = pluggy.PluginManager("mate")
    pm.add_hookspecs(mate_hookspecs)
    for group in mate_config.shells:
        pm.load_setuptools_entrypoints(group)
    for x in sys.modules:
        if "mate.modules.internal." in x:
            pm.register(sys.modules[x])
    # pm.register(sys.modules[__name__])
    return pm


def load_plugins():
    # initializing plugin manager and mate modules
    pm = get_plugin_manager()
    record = MateRecord("mate", pm.hook)
    record.add_modules()
    mate_config.module_record = record
    mate_config.plugin_manager = pm


def print_banner():
    """Prints mate's banner i.e. version info."""
    print(green("mate " + __version__))
    print('For help, type "help".')


def prompt_style():
    """Specifies the colors of different block/classes in mate's prompt

    Returns:
        style: Style object is parsed by prompt toolkit to make prompt fancy.
    """
    if mate_config.prompt_status == "+":
        status_color = "#00aa00"
    elif mate_config.prompt_status == "-":
        status_color = "#aa0000"
    style = Style.from_dict(
        {
            # User input (default text).
            "": "#ffffff",
            # Prompt.
            "execname": "ansicyan",
            "bracket": "#ffffff",
            "status": status_color,
            "arrow": "ansicyan",
        }
    )
    return style


def prompt_message():
    """Creates mate's prompt design.

    Returns:
        message: Message object is parsed by prompt toolkit to create prompt.
    """
    execname = "mate"
    shells = mate_config.shells
    if shells != ["mate"]:
        if len(shells) == 1:
            execname = shells[0] + " " + execname
        else:
            execname = "super" + " " + execname
    message = [
        ("class:execname", execname),
        ("class:bracket", " ["),
        ("class:status", mate_config.prompt_status),
        ("class:bracket", "] "),
        ("class:arrow", "> "),
    ]

    return message


def set_prompt_status(status):
    """Sets state (+/-) into mate's prompt,
    which reflects whether last command was executed successfully or not

    Args:
        status ([type]): [description]
    """
    mate_config.prompt_status = status


def parse_args(args):
    """Parse command line arguments of mate.

    Args:
        args (list): List of arguments (except sys.argv[0]) passed to mate.

    Returns:
        parsed_args: Collection of arguments parsed by argparse.
    """
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "-V", "--version", action="version", version="%(prog)s " + __version__
    )
    parse.add_argument(
        "--debug",
        dest="debug",
        default=False,
        action="store_true",
        help="Set console log level to DEBUG.",
    )
    parse.add_argument(
        "-p",
        "--project-dir",
        dest="project_dir",
        help="Specify root directory of a project for analysis.",
    )
    parse.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help="Specify root directory to store various result files.",
    )
    parse.add_argument(
        "-s",
        "--socket",
        dest="socket",
        help="Provide [Protocol]Host[:Port] of a service for analysis.",
    )
    parse.add_argument(
        "--shells",
        dest="shells",
        default="mate",
        help="Specify setuptools group names separated by comma to fetch plugins instead of default 'mate'.",
    )
    parse.add_argument(
        "--exec",
        dest="exec",
        help="Provide mate shell command for batch execution.",
    )
    return parse.parse_args(args)


def main():
    """I do the actual work."""
    # command line arg parsing
    args = parse_args(sys.argv[1:])
    if args.debug:
        shellLogHandler.setLevel(logging.DEBUG)
    if args.project_dir:
        mate_config.project_dir = args.project_dir
    if args.output_dir:
        mate_config.output_dir = args.output_dir
    if args.socket:
        mate_config.socket = args.socket
    if args.shells:
        mate_config.shells = args.shells.strip().strip(",").split(",")

    if not args.exec:
        # a nice banner
        print_banner()
        print("Loading modules... ", end="")

    # load plugins
    load_plugins()

    if not args.exec:
        print("Done.")

    if args.exec:
        mate_config.module_record.parse_command(shlex.split(args.exec))
        return

    completer = NestedCompleter.from_nested_dict(
        mate_config.module_record.get_autocompleter()
    )

    # setting up interpreter prompt
    history_file = mate_config.mate_hist
    session = PromptSession(
        history=FileHistory(history_file),
        style=None,
        wrap_lines=True,
    )

    log.debug("- Starting shell.")

    try:
        while True:
            prompt = session.prompt(
                prompt_message(),
                style=prompt_style(),
                completer=completer,
                complete_while_typing=True,
                key_bindings=bindings,
            )
            command = prompt.strip()
            # passing cmd string tokens for parsing
            cmd_tokens = shlex.split(command)
            command_status = True
            if len(cmd_tokens) > 0:
                command_status = mate_config.module_record.parse_command(cmd_tokens)
            if command_status:
                set_prompt_status("+")
            else:
                set_prompt_status("-")

    except KeyboardInterrupt:
        print(yellow("\n( ╥﹏╥) ノシ  ") + red("bye...\n"))
        sys.exit()
    except Exception:
        log.error("Wait! What happened now...", exc_info=True)
