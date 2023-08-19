import logging


def logger(frame: str) -> logging.Logger:
    """Function that returns the logger"""
    # Create and configure the logger
    logger = logging.getLogger(frame)
    logger.setLevel(logging.DEBUG)

    # Create and configure the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create and configure the formatter
    formatter = logging.Formatter("%(asctime)s | %(name)s: %(levelname)s → %(message)s")
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger
