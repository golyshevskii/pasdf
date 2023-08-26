import logging
from functools import partial

import pytest
from logger import logger

log = partial(logger, "frame")

log_levels = [
    (logging.DEBUG, "DEBUG"),
    (logging.INFO, "INFO"),
    (logging.ERROR, "ERROR"),
]


@pytest.mark.parametrize("level, expected_level_name", log_levels)
def test_logger_output(caplog, level, expected_level_name):
    logger = log()

    with caplog.at_level(level=level):
        logger.log(level, "Cool message")

    assert any(record.levelname == expected_level_name for record in caplog.records)
    assert any("Cool message" in record.message for record in caplog.records)


def test_logger_level_setting():
    logger = log()
    assert logger.level == logging.DEBUG
