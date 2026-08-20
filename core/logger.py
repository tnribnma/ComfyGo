import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from ..config import settings

class _SingletonLogger:
    _configured: bool = False
    _root: Optional[logging.Logger] = None

    @classmethod
    def configure(cls) -> logging.Logger:
        if cls._configured and cls._root:
            return cls._root

        root = logging.getLogger("comfygo")
        root.setLevel(settings.LOG_LEVEL.upper())
        root.propagate = False 

        if root.handlers:
            cls._root = root
            cls._configured = True
            return root

        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        root.addHandler(console)

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=10 * 1024 * 1024, 
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

        err_handler = logging.handlers.RotatingFileHandler(
            log_dir / "error.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(formatter)
        root.addHandler(err_handler)

        cls._root = root
        cls._configured = True
        return root

    @classmethod
    def get(cls, name: Optional[str] = None) -> logging.Logger:
        root = cls.configure()
        if name:
            return root.getChild(name)
        return root

def get_logger(name: Optional[str] = None) -> logging.Logger:
    return _SingletonLogger.get(name)

logger: logging.Logger = get_logger()