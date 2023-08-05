from pathlib import Path
from mate.__version__ import __author__, __version__


class MateConfig(object):
    """Central config class for mate."""

    def __init__(self):
        home = Path.home()
        self.mate_version = __version__
        self.mate_author = __author__
        self.mate_dir = (
            Path(".mate").resolve() if Path(".mate").exists() else Path(home / ".mate")
        )
        # self.mate_conf = Path(self.mate_dir / ".mate.conf")
        self.mate_hist = Path(self.mate_dir / ".mate_history")

        self.project_dir = Path.cwd()
        self.output_dir = Path(self.mate_dir / "output")
        self.socket = None

        if not self.mate_dir.exists():
            self.mate_dir.mkdir(exist_ok=True)
            self.output_dir.mkdir(exist_ok=True)
            # Path(self.mate_conf).touch()
            Path(self.mate_hist).touch()

        # initialize command hierarchy
        self.prompt_status = "+"
        self.command = {}
        self.module_record = None
        self.plugin_manager = None
        self.shells = ["mate"]


def config_init():
    """Initialize global config to be used through out mate."""
    global mate_config
    mate_config = MateConfig()


config_init()
