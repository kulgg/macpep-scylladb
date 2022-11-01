import re
from typing import List

ID_REGEX = re.compile("ID   (\w+).*", re.MULTILINE)
ACCESSION_LINES_REGEX = re.compile("AC   .*", re.MULTILINE)
ACCESSIONS_REGEX = re.compile("(\w+);\s?")
SEQUENCE_LINES_REGEX = re.compile("^     \w+.*", re.MULTILINE)
SEQUENCE_REGEX = re.compile("(\w+)\s?")
REVIEWED_STATUS_REGEX = re.compile("^ID.*?Reviewed;", re.MULTILINE)


def get_id(txt: str) -> str:
    match = ID_REGEX.match(txt)
    return match.group(1)


def get_accessions(txt: str) -> List[str]:
    accessions = []
    ac_lines = ACCESSION_LINES_REGEX.findall(txt)
    for line in ac_lines:
        accessions.extend(ACCESSIONS_REGEX.findall(line))
    return accessions


def get_sequence(txt: str) -> str:
    sequence = ""
    for line in SEQUENCE_LINES_REGEX.findall(txt):
        for sequence_part in SEQUENCE_REGEX.findall(line):
            sequence = f"{sequence}{sequence_part}"
    return sequence


def get_review_status(txt: str) -> bool:
    return bool(REVIEWED_STATUS_REGEX.search(txt))
