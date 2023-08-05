"""Dicom parsing module"""
import logging
import os
import re
import sys
import typing as t
import warnings
from pathlib import Path
from typing import NamedTuple

from fw_file.collection import FileCollection
from fw_file.dicom import DICOM, DICOMCollection
from fw_file.dicom.config import CONFIG
from fw_file.dicom.dicom import get_value
from fw_meta import MetaData
from nibabel.nicom import csareader
from pydicom.datadict import tag_for_keyword

from fw_gear_file_metadata_importer.util import (
    AnyPath,
    remove_empty_values,
    validate_file,
)

# Enabling some pydicom callbacks
CONFIG.fix_vr_mismatch = True
CONFIG.configure_pydicom()

log = logging.getLogger(__name__)

DENY_TAGS = {
    "PixelData",
    "Pixel Data",
    "ContourData",
    "EncryptedAttributesSequence",
    "OriginalAttributesSequence",
    "SpectroscopyData",
    "MrPhoenixProtocol",  # From Siemens CSA
    "MrEvaProtocol",  # From Siemens CSA
    "FileMetaInformationVersion",  # OB in file_meta
}

# TODO: extend that set
ARRAY_TAGS = {
    "AcquisitionNumber",
    "AcquisitionTime",
    "EchoTime",
    "ImageOrientationPatient",
    "ImagePositionPatient",
    "ImageType",
    "InstanceNumber",
    "SliceLocation",
}

# Private Dicom tag to keep, in the format (PrivateCreatorName, 0099xx10)
PRIVATE_TAGS = set()

# matches either hexadecimal, keyword or private tag notation
# e.g. "00100020" or "PatientID" or "GEMS_PARM_01, 0043xx01"
VALID_KEY = re.compile(r"^[\dA-Fa-f]{8}$|^[A-Za-z]+$|^\w+,\s*\d{4}[xX]{2}\d{2}$")


class DICOMFindings(NamedTuple):
    """Class to store findings on dicom file and report on them."""

    # True is file is zero_byte, false otherwise.
    zero_byte: bool
    # True is file can be decoded without Exception, false otherwise
    decoding: bool
    # List of tracking events (changes made to the raw data elements during decoding)
    tracking: list

    def is_valid(self):
        if not self.zero_byte and self.decoding:
            return True
        return False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}:"
            f"\n\t0-byte: {self.zero_byte}\n\tdecoding: {self.decoding}"
        )


def update_array_tag(custom_tags: t.Dict[str, bool]):
    """Update PRIVATE_TAGS and ARRAY_TAGS list.

    Args:
        custom_tags (dict): Dictionary of type with key/value of type tag: bool.
            If bool=True, tag is added to PRIVATE_TAGS and ARRAY_TAGS. If bool=False,
            tag is removed from PRIVATE_TAGS and ARRAY_TAGS.
    """
    if custom_tags:
        # validate key/value
        for k, v in custom_tags.items():
            if not VALID_KEY.match(k):
                log.error(
                    "Invalid key defined in project.info.context.header.dicom: %s\n"
                    "Valid key format is hexadecimal (e.g. '00100020'), "
                    "keyword (e.g. 'PatientID') or "
                    "private tag notation (e.g. 'GEMS_PARM_01, 0043xx01'). "
                    "Please check your project context.",
                    k,
                )
                sys.exit(1)
            if isinstance(v, str):
                if v.strip().lower() == "false":
                    custom_tags[k] = False
                elif v.strip().lower() == "true":
                    custom_tags[k] = True
                else:
                    log.error(
                        "Invalid value defined in project.info.context.header.dicom "
                        "for key %s. Valid value is boolean, 'True' or 'False'",
                        k,
                    )
                    sys.exit(1)

        for k, bool_val in custom_tags.items():
            is_private = False

            if "," in k:  # key pattern is "PrivateCreatorName, GGGGxxEE"
                k = tuple(p.strip() for p in k.split(","))
                is_private = True

            if bool_val:
                if is_private and k not in PRIVATE_TAGS:
                    PRIVATE_TAGS.add(k)
                if k not in ARRAY_TAGS:
                    ARRAY_TAGS.add(k)
            else:
                if k in PRIVATE_TAGS:
                    PRIVATE_TAGS.remove(k)
                if k in ARRAY_TAGS:
                    ARRAY_TAGS.remove(k)
                if k not in DENY_TAGS:
                    DENY_TAGS.add(k)


def inspect_file(file_: DICOM) -> DICOMFindings:
    """Returns the DICOMFindings for the input DICOM instance."""
    zero_byte = False if os.path.getsize(file_.filepath) > 1 else True
    try:
        file_.decode()  # NB: file_.tracker gets populated during decoding.
        decoding = True
    except Exception:
        decoding = False

    # store tracking events
    file_.tracker.trim()
    tracking_events = [de.export() for de in file_.tracker.data_elements]
    return DICOMFindings(zero_byte, decoding, tracking_events)


def inspect_collection(collection: FileCollection) -> t.List:
    """Returns list of findings for each Dicom in collection"""
    findings = []
    for file_ in collection:
        findings.append(inspect_file(file_))
    return findings


def get_dicom_header(dcm: DICOM):
    """Returns a dictionary representation of the dicom header of the DICOM instance.

    Args:
        dcm (DICOM): The DICOM instance.

    Returns:
        dict: A dictionary representation of the dicom header.
    """
    header = {}

    header.update(get_preamble_dicom_header(dcm))
    header.update(get_core_dicom_header(dcm))
    header = remove_empty_values(header)

    return header


def get_preamble_dicom_header(dcm: DICOM):
    """Returns a dictionary representation of the dicom header preamble of the DICOM instance.

    Args:
        dcm (DICOM): The DICOM instance.

    Returns:
        dict: A dictionary representation of the dicom preamble header.
    """
    header = {}

    if not dcm:
        return header

    for kw in dcm.dataset.file_meta.dir():
        if kw in DENY_TAGS:
            continue
        header[kw] = get_value(dcm.dataset.file_meta[kw].value)
    return header


def get_core_dicom_header(dcm: DICOM):
    """Returns a dictionary representation of the dicom header but the preamble.

    Args:
        dcm (DICOM): The DICOM instance.

    Returns:
        dict: A dictionary representation of the dicom header.
    """
    header = {}

    if not dcm:
        return header

    for kw in dcm.dir() + list(PRIVATE_TAGS):
        if kw in DENY_TAGS:
            log.debug(f"Skipping {kw} - in DENY_TAGS.")
            continue
        # some keyword may be repeating group and none unique
        if tag_for_keyword(kw) is None and kw not in PRIVATE_TAGS:
            log.debug(f"Skipping {kw} - none unique.")
            continue
        try:
            elem = dcm.get_dataelem(kw)
            if elem.is_private and isinstance(kw, tuple):
                header_kw = ",".join(kw)
            else:
                header_kw = kw
            if elem.VR == "SQ":
                header[header_kw] = []
                for i, ds in enumerate(dcm[kw]):
                    header[header_kw].append(get_core_dicom_header(ds))
            else:
                header[header_kw] = dcm[kw]
        except KeyError:  # private tag
            continue

    return header


def get_siemens_csa_header(dcm: DICOM) -> t.Dict:
    """Returns a dict containing the Siemens CSA header for image and series.

    More on Siemens CSA header at https://nipy.org/nibabel/dicom/siemens_csa.html.

    Args:
        dcm (DICOM): The DICOM instance.

    Returns:
        dict: A dictionary containing the CSA header.

    """
    csa_header = {"image": {}, "series": {}}
    csa_header_image = csareader.get_csa_header(dcm.dataset.raw, csa_type="image")
    if csa_header_image:
        csa_header_image_tags = csa_header_image.get("tags", {})
        for k, v in csa_header_image_tags.items():
            if (v["items"] is not None and not v["items"] == []) and k not in DENY_TAGS:
                csa_header["image"][k] = v["items"]

    csa_header_series = csareader.get_csa_header(dcm.dataset.raw, csa_type="series")
    if csa_header_series:
        csa_header_series_tags = csa_header_series.get("tags", {})
        for k, v in csa_header_series_tags.items():
            if (v["items"] is not None and not v["items"] == []) and k not in DENY_TAGS:
                csa_header["series"][k] = v["items"]

    return csa_header


def get_dicom_array_header(collection: DICOMCollection):
    """Returns array of dicom tags for tag in ARRAY_TAGS."""
    array_header = {}
    for t in ARRAY_TAGS:
        arr = collection.bulk_get(t)
        if any(arr):
            array_header[t] = arr
    return array_header


def get_file_info_header(
    dcm: DICOM,
    collection: t.Optional[DICOMCollection] = None,
    siemens_csa: bool = False,
) -> t.Dict:
    """Returns a dictionary representing the header of the DICOM instance.

    Args:
        dcm (DICOM): The DICOM instance.
        collection (DICOMCollection or None): A DICOMCollection instance.
        siemens_csa (bool): If true, extracts the Siemens CSA header and stores under
            "csa" key.

    Returns:
        dict: A dictionary containing the header information.
    """
    header = dict()
    header["dicom"] = get_dicom_header(dcm)
    if collection:
        header["dicom_array"] = get_dicom_array_header(collection)
    if siemens_csa:
        manufacturer = header["dicom"].get("Manufacturer")
        if (
            manufacturer
            and isinstance(manufacturer, str)
            and manufacturer.lower().strip() != "siemens"
        ):
            log.info("Manufacturer is not Siemens - skipping CSA parsing")
            return header
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                header["csa"] = get_siemens_csa_header(dcm)
    return header


def get_file_qc(dcm: DICOM, file_path: t.Optional[AnyPath] = None) -> t.Dict:
    """Returns the tracking trace of dcm.

    Args:
        dcm (DICOM): The DICOM instance.
        file_path (Path-like): Optional file path

    Returns:
        dict: Dictionary containing trace of updated data elements.
    """
    qc = {"filename": Path(file_path or dcm.filepath).parts[-1], "trace": []}
    if dcm.tracker:
        dcm.tracker.trim()
        for raw_elem in dcm.tracker.data_elements:
            de_trace = raw_elem.export()
            for event in de_trace["events"]:
                qc["trace"].append(f"Tag {de_trace['original'].tag} {event}")
    return qc


def preprocess_input(
    input_file: AnyPath,
) -> t.Tuple[DICOM, t.Union[DICOMCollection, None]]:
    """Returns a File instance from input_file.

    If input_file is a zip archive, returns one a representative zip member.

    Args:
        input_file (AnyPath): Path-like object to input file.

    Returns:
        DICOM, Collection or None: A representative DICOM File instance, and
            a Collection or None if input_file is not a zip archive.
    """
    if not isinstance(input_file, Path):
        input_file = Path(input_file)

    # validate input_file
    validation_errors = validate_file(input_file)
    if validation_errors:
        log.error(f"Errors found validating input file: {validation_errors}")
        sys.exit(1)

    if str(input_file).endswith(".zip"):

        collection = DICOMCollection.from_zip(input_file, force=True, track=True)
        try:
            collection.sort(key=lambda x: x.get("InstanceNumber"))
        except TypeError:  # InstanceNumber not found, not sorting
            log.info("InstanceNumber missing from collection - skipping sorting.")
            pass
        collection_findings = inspect_collection(collection)
        file_ = None
        for i, dicom_findings in enumerate(collection_findings):
            if dicom_findings.is_valid():
                file_ = collection[i]
                break

        if not file_:
            log.error(f"Unable to find a valid Dicom file in archive: {input_file}.")
            sys.exit(1)
    else:
        collection = None
        file_ = DICOM(input_file, force=True, track=True)
        dicom_findings = inspect_file(file_)
        if not dicom_findings.is_valid():
            log.error(f"Input file is invalid: {input_file}\n{dicom_findings}")
            sys.exit(1)

    return file_, collection


def process(
    input_path: AnyPath, siemens_csa: bool = False
) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Process `file_path` and returns a `flywheel.FileEntry` and its corresponding meta.

    Args:
        input_path (Path-like): Path to input-file.
        siemens_csa (bool): If True, extracts Siemens CSA header (Default: False).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
        dict: Dictionary containing the qc metrics.
    """
    file_, collection = preprocess_input(input_path)
    header = get_file_info_header(file_, collection, siemens_csa=siemens_csa)
    qc = get_file_qc(file_)
    fe = {"modality": file_.get("Modality"), "info": {"header": header}}
    return fe, file_.meta, qc
