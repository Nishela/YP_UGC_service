__all__ = (
    'LOGGING',
)

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOGGING = {
    "version": 1,
    "root": {"handlers": ["console"], "level": "DEBUG"},
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        }
    },
    "formatters": {
        "std_out": {
            "format": LOG_FORMAT,
            "datefmt": "%d-%m-%Y %I:%M:%S",
        }
    },
}
