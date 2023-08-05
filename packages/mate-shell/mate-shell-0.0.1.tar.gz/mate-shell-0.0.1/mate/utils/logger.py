import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.traceback import install

# global console and log object
console = Console()
log = logging.getLogger(__name__)
install()

# handler for logging in stdout and file
shellLogHandler = RichHandler()
log_file = open("/tmp/mate_debug.log", "a")
fileLogHandler = RichHandler(
    console=Console(file=log_file), rich_tracebacks=True, tracebacks_show_locals=True
)

log.setLevel(logging.DEBUG)
shellLogHandler.setLevel(logging.INFO)
fileLogHandler.setLevel(logging.DEBUG)

# the formatter determines what our logs will look like
fmt_shell = "<%(funcName)s> %(message)s"
fmt_file = fmt_shell

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shellLogHandler.setFormatter(shell_formatter)
fileLogHandler.setFormatter(file_formatter)

log.addHandler(shellLogHandler)
log.addHandler(fileLogHandler)
