#!/usr/bin/env python3
import importlib.util
import logging
import logging.config
import os
import subprocess
from pathlib import Path
from typing import Optional

import uvicorn  # type: ignore


def configure_logging(
    logger: logging.Logger = logging.getLogger(),
    logging_conf: str = os.getenv("LOGGING_CONF", "inboard.logging_conf"),
) -> dict:
    """Configure Python logging based on a path to a logging module or file."""
    try:
        logging_conf_path = Path(logging_conf)
        spec = (
            importlib.util.spec_from_file_location("confspec", logging_conf_path)
            if logging_conf_path.is_file() and logging_conf_path.suffix == ".py"
            else importlib.util.find_spec(logging_conf)
        )
        if not spec:
            raise ImportError(f"Unable to import {logging_conf}")
        logging_conf_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(logging_conf_module)  # type: ignore[union-attr]
        if not hasattr(logging_conf_module, "LOGGING_CONFIG"):
            raise AttributeError(f"No LOGGING_CONFIG in {logging_conf_module.__name__}")
        logging_conf_dict = getattr(logging_conf_module, "LOGGING_CONFIG")
        if not isinstance(logging_conf_dict, dict):
            raise TypeError("LOGGING_CONFIG is not a dictionary instance")
        logging.config.dictConfig(logging_conf_dict)
        logger.debug(f"Logging dict config loaded from {logging_conf_path}.")
        return logging_conf_dict
    except Exception as e:
        logger.error(f"Error when setting logging module: {e.__class__.__name__} {e}.")
        raise


def run_pre_start_script(logger: logging.Logger = logging.getLogger()) -> str:
    """Run a pre-start script at the provided path."""
    logger.debug("Checking for pre-start script.")
    pre_start_path = os.getenv("PRE_START_PATH", "/app/inboard/app/prestart.py")
    if Path(pre_start_path).is_file():
        process = "python" if Path(pre_start_path).suffix == ".py" else "sh"
        run_message = f"Running pre-start script with {process} {pre_start_path}."
        logger.debug(run_message)
        subprocess.run([process, pre_start_path])
        message = f"Ran pre-start script with {process} {pre_start_path}."
    else:
        message = "No pre-start script found."
    logger.debug(message)
    return message


def set_app_module(logger: logging.Logger = logging.getLogger()) -> str:
    """Set the name of the Python module with the app instance to run."""
    try:
        app_module = str(os.getenv("APP_MODULE"))
        if not importlib.util.find_spec((module := app_module.split(sep=":")[0])):
            raise ImportError(f"Unable to find or import {module}")
        logger.debug(f"App module set to {app_module}.")
        return app_module
    except Exception as e:
        logger.error(f"Error when setting app module: {e.__class__.__name__} {e}.")
        raise


def set_gunicorn_options() -> list:
    """Set options for running the Gunicorn server."""
    gunicorn_conf_path = os.getenv("GUNICORN_CONF", "/app/inboard/gunicorn_conf.py")
    worker_class = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
    if not Path(gunicorn_conf_path).is_file():
        raise FileNotFoundError(f"Unable to find {gunicorn_conf_path}")
    return ["gunicorn", "-k", worker_class, "-c", gunicorn_conf_path]


def set_uvicorn_options(log_config: Optional[dict] = None) -> dict:
    """Set options for running the Uvicorn server."""
    with_reload = (
        True
        if (value := os.getenv("WITH_RELOAD")) and value.lower() == "true"
        else False
    )
    reload_dirs = (
        [d.lstrip() for d in str(os.getenv("RELOAD_DIRS")).split(sep=",")]
        if os.getenv("RELOAD_DIRS")
        else None
    )
    return dict(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "80")),
        log_config=log_config,
        log_level=os.getenv("LOG_LEVEL", "info"),
        reload=with_reload,
        reload_dirs=reload_dirs,
    )


def start_server(
    process_manager: str,
    app_module: str,
    logger: logging.Logger = logging.getLogger(),
    logging_conf_dict: Optional[dict] = None,
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        if process_manager == "gunicorn":
            logger.debug("Running Uvicorn with Gunicorn.")
            gunicorn_options: list = set_gunicorn_options()
            gunicorn_options.append(app_module)
            subprocess.run(gunicorn_options)
        elif process_manager == "uvicorn":
            logger.debug("Running Uvicorn without Gunicorn.")
            uvicorn_options: dict = set_uvicorn_options(log_config=logging_conf_dict)
            uvicorn.run(app_module, **uvicorn_options)
        else:
            raise NameError("Process manager needs to be either uvicorn or gunicorn")
    except Exception as e:
        logger.error(f"Error when starting server: {e.__class__.__name__} {e}.")
        raise


if __name__ == "__main__":  # pragma: no cover
    logger = logging.getLogger()
    logging_conf_dict = configure_logging(logger=logger)
    run_pre_start_script(logger=logger)
    start_server(
        str(os.getenv("PROCESS_MANAGER", "gunicorn")),
        app_module=set_app_module(logger=logger),
        logger=logger,
        logging_conf_dict=logging_conf_dict,
    )
