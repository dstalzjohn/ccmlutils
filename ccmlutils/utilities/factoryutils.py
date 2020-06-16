from pathlib import Path
from typing import Dict, Any, Optional
from importlib import import_module

from ccmlutils.config.envconfig import replace_id_keys


class ImportException(Exception):
    pass


def init_object_node(input_dict=None) -> Dict[str, Any]:
    return {"class": init_object(input_dict)}


def init_object(input_dict: Optional[dict] = None) -> Any:
    """
    Imports dynamically a class or function. When `type` is used the object is initialized with
    the given `params` accordingly. Otherwise (with `function`-keyword) only the imported object is returned.
    :param input_dict: dict with keywords (type and params) or function
    :return: Initialized or imported object/class/function.
    """
    use_params: bool = False
    if "type" in input_dict:
        cur_type: str = input_dict["type"]
        use_params = True
    elif "function" in input_dict:
        cur_type: str = input_dict["function"]
    else:
        raise ImportException("Neither type nor function keyword in param dict!")

    type_list = cur_type.rsplit(".", 1)
    try:
        imported_module = import_module(type_list[0])
    except ModuleNotFoundError as e:
        raise Exception(f"Module with name not found: {type_list[0]}") from e
    imported_type = getattr(imported_module, type_list[1])
    if use_params:
        init_dict = input_dict.get("params", dict())
        init_class = imported_type(**init_dict)
    else:
        init_class = imported_type

    return init_class


def subs_path_and_create_folder(filepath: str) -> str:
    filepath = replace_id_keys(filepath)
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    return filepath


def init_loss(loss: str or dict):
    if type(loss) is str:
        return loss
    loss_dict = {k: init_object(v) for k, v in loss.items()}
    return loss_dict
