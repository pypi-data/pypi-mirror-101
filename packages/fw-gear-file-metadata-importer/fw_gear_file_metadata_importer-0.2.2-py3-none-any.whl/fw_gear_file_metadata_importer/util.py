"""Util module."""
import copy
import os
import typing as t
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext
from fw_meta import MetaData

AnyPath = t.Union[str, Path]


def get_startswith_lstrip_dict(dict_: t.Dict, startswith: str) -> t.Dict:
    """Returns dictionary filtered with keys starting with startswith."""
    res = {}
    for k, v in dict_.items():
        if k.startswith(startswith):
            res[k.split(f"{startswith}.")[1]] = v
    return res


def validate_file(filepath: AnyPath) -> t.List[str]:
    """Returns a list of validation errors if any."""
    errors = []
    errors += validate_file_size(filepath)
    return errors


def validate_file_size(filepath: AnyPath) -> t.List[str]:
    """Returns a list of validation errors related to file size."""
    errors = []
    if not os.path.getsize(filepath) > 1:
        errors.append("File is empty: {}".format(filepath))
    return errors


def create_metadata(
    context: GearToolkitContext, fe: t.Dict, meta: MetaData, qc: t.Dict
):
    """Populates .metadata.json.

    Args:
        context (GearToolkitContext): The gear context.
        fe (dict): A dictionary containing the file attributes to update.
        meta (MetaData): A MetaData containing the file "metadata" (parents container info)
        qc (dict): A dictionary containing the qc namespace info.
    """
    file_name = context.get_input("input-file")["location"]["name"]

    # current file info object
    info = copy.deepcopy(context.get_input("input-file")["object"]["info"])

    # Build qc namespace
    if "qc" not in info:
        info["qc"] = {}
    # add gear_info
    qc.update(
        {
            "gear_info": {
                "version": context.manifest["version"],
                "name": context.manifest["name"],
            }
        }
    )
    # overwrite qc.<gear-name> with current qc value
    info["qc"][context.manifest["name"]] = qc

    # file update
    info.update(fe.get("info", {}))  # to preserve existing info key/value
    context.update_file_metadata(file_name, modality=fe.get("modality"), info=info)

    # parent containers update
    # TODO revisit that age cannot be passed
    if "session.age" in meta:
        _ = meta.pop("session.age")
    context.update_container_metadata(
        "session", **get_startswith_lstrip_dict(meta, "session")
    )
    context.update_container_metadata(
        "subject", **get_startswith_lstrip_dict(meta, "subject")
    )
    context.update_container_metadata(
        "acquisition", **get_startswith_lstrip_dict(meta, "acquisition")
    )

    # https://flywheelio.atlassian.net/browse/GEAR-868
    # Subject needs to be updated on session in old-core
    # These two lines make this gear compatible with 15.x.x and 14.x.x
    sub = context._metadata.pop("subject")
    context._metadata.get("session").update({"subject": sub})


def remove_empty_values(d: t.Dict, recurse=True) -> t.Dict:
    """Removes empty value in dictionary.

    Args:
        d (dict): A dictionary.
        recurse (bool): If true, recurse nested dictionary.

    Returns:
        dict: A filtered dictionary.
    """
    d_copy = copy.deepcopy(d)
    for k, v in d.items():
        if isinstance(v, dict) and recurse:
            d_copy[k] = remove_empty_values(v, recurse=recurse)
        if v == "" or v is None or v == [] or v == {}:
            d_copy.pop(k)
    return d_copy
