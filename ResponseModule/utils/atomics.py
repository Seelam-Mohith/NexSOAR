import re
from pathlib import PurePath

TECHNIQUE_ID_PATTERN = re.compile(r"^T\d{4}(?:\.\d{3})?$")
TECHNIQUE_HEADING_PATTERN = re.compile(
    r"^#\s+(T\d{4}(?:\.\d{3})?)\s*[-–—]\s*(.+?)\s*$",
    re.MULTILINE,
)


def _parts(source):
    return PurePath(str(source).replace("\\", "/")).parts


def technique_dir(source):
    """Directory name that holds the playbook, e.g. 'T1003.001'."""
    parts = _parts(source)
    return parts[-2] if len(parts) >= 2 else ""


def is_playbook(source):
    """True only for files that live directly in a T####[.###] directory.

    Keeps the platform index tables, the navigator matrices and the vendored
    readme files under src/ out of the corpus.
    """
    return bool(TECHNIQUE_ID_PATTERN.match(technique_dir(source)))


def parse_heading(text):
    """Return (technique_id, technique_name) from the playbook's H1 heading."""
    match = TECHNIQUE_HEADING_PATTERN.search(text or "")
    if not match:
        return None, None
    return match.group(1), match.group(2)


def describe_playbook(source, text):
    """Metadata for a playbook document, keyed for storage and filtering."""
    heading_id, name = parse_heading(text)
    return {
        "technique_id": heading_id or technique_dir(source),
        "technique_name": name or "",
    }


def chunk_header(metadata):
    """Heading line prefixed to a chunk so its embedding carries the technique."""
    technique_id = metadata.get("technique_id")
    technique_name = metadata.get("technique_name")
    if not technique_id:
        return ""
    if technique_name:
        return f"# {technique_id} - {technique_name}\n\n"
    return f"# {technique_id}\n\n"
