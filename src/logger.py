import logging
from logging.handlers import RotatingFileHandler


def app_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Для сохранения в файл
    file_handler = RotatingFileHandler(
        "fastapi_log.log", maxBytes=1048576, backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# Задаём логирование новым логером для основных используемых библиотек
for log_module in [
    "fastapi",
    "sqlalchemy.engine",
    "uvicorn",
    "uvicorn.access",
    "uvicorn.error",
    "diffusers",
    "rembg",
    "numpy",
    "torch",
    "asyncpg",
]:
    app_logger(log_module)
