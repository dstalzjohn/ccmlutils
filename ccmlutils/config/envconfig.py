from os import getenv, environ
from typing import Tuple

RUN_ID_KEY = "RUN_ID"
SHORT_ID_KEY = "SHORT_ID"
PIPELINE_KEY = "PIPELINE"
EXP_NAME_KEY = "EXPERIMENT_NAME"
EXP_PREFIX_KEY = "EXPERIMENT_PREFIX"


def get_run_id() -> str:
    return getenv(RUN_ID_KEY)


def get_short_id() -> str:
    return getenv(SHORT_ID_KEY)


def get_exp_name() -> str:
    return getenv(EXP_NAME_KEY)


def get_and_ask_for_exp_name() -> Tuple[str, bool]:
    """Returns the exp name and whether a commit should be applied"""
    do_commit = False
    if not EXP_NAME_KEY in environ:
        cur_input = input("Enter the experiment name: \n")
        environ[EXP_NAME_KEY] = cur_input
        do_commit = bool(len(cur_input) > 0)
    return get_exp_name(), do_commit


def replace_id_keys(input_str: str) -> str:
    input_str = input_str.replace("$" + SHORT_ID_KEY, get_short_id())
    input_str = input_str.replace("$" + RUN_ID_KEY, get_run_id())

    return input_str


def set_pipeline_name(name: str):
    """
    Sets a pipeline name if not already set.
    """
    if getenv(PIPELINE_KEY) is None:
        environ[PIPELINE_KEY] = name


def get_pipeline_name() -> str:
    return getenv(PIPELINE_KEY)
