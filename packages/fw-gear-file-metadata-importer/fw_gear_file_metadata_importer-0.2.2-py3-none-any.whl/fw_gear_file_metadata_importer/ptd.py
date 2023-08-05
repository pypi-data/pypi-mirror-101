import tempfile
import typing as t
from pathlib import Path

from fw_file.ptd import PTD
from fw_meta import MetaData

from fw_gear_file_metadata_importer import dicom

AnyPath = t.Union[str, Path]


def process(
    file_path, extract_ptd_header: bool = True, siemens_csa: bool = False
) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Process `file_path` and returns a `flywheel.FileEntry` and its corresponding meta.

    Args:
        file_path (Path-like): Path to input-file.
        file_path (bool): Whether to extract the PTD header (Default: True)
        siemens_csa (bool): If True, extracts Siemens CSA header (Default: False).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
        dict: Dictionary containing the qc metrics.

    """
    # Extract dicom header
    ptd_file = PTD(file_path)
    header = dicom.get_file_info_header(ptd_file.dcm, None, siemens_csa=siemens_csa)
    # Extract PTD preamble
    ptd_preamble = ptd_file.preamble.decode("utf-8")
    header.update({"ptd": ptd_preamble})

    qc = dicom.get_file_qc(ptd_file.dcm, ptd_file.filepath)
    fe = {"modality": ptd_file.dcm.get("Modality"), "info": {"header": header}}
    return fe, ptd_file.dcm.meta, qc
