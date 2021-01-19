import re
from dataclasses import dataclass


@dataclass
class RegexRemoval:
    description: str
    regex_str: str  # usually raw string: r"your string"

    def __post_init__(self):
        self.regex = re.compile(self.regex_str, re.IGNORECASE)


@dataclass
class RegexSubstitution:
    description: str
    regex_str: str  # usually raw string: r"your string"
    replacement: str

    def __post_init__(self):
        self.regex = re.compile(self.regex_str, re.IGNORECASE)


removals = [
    RegexRemoval("OBSCIS", r"(OBSCIS)"),
    RegexRemoval(
        "MO Suffix",
        r"\b\w\s\w\s\w\w?\s\w\s\d{2}(?: |\W)\d{2}(?: |\W)\d{4}",
    ),
]

substitutions = [
    RegexSubstitution("Less Than", r"&LT;", "<"),
    RegexSubstitution("Greater Than", r"&GT;", ">"),
    RegexSubstitution("With Out", r"\bw(?: |\W)o\b", "without"),
    RegexSubstitution(
        "Breaking and Entering",
        r"\bB ?& ?E\b",
        "breaking and entering",
    ),
    RegexSubstitution("Building", r"\bbldg\b", "building"),
    RegexSubstitution(
        "With Intent",
        r"\bw\W\s?in?t?e?n?t?\b",
        "with intent",
    ),
    RegexSubstitution(
        "Controlled Substance",
        r"\bcont?r?(?:\b|\W)(?:\b|\W)?sub(?:\b|stance\b)",
        "controlled substance",
    ),
    RegexSubstitution(
        "Controlled Substance 2",
        r"\bc\W?s\b",
        "controlled substance",
    ),
    RegexSubstitution(
        "Possession",
        r"\bposs\b",
        "possession",
    ),
    RegexSubstitution(
        "Criminal Sexual Conduct",
        r"\bcsc\b",
        "criminal sexual conduct",
    ),
    RegexSubstitution(
        "Attempted",
        r"\batt\b",
        "attempted",
    ),
    RegexSubstitution(
        "Violation of Probation",
        r"\bvop\b",
        "violation of probation",
    ),
    RegexSubstitution(
        "Conspiracy",
        r"\bcon\b",
        "conspiracy",
    ),
    RegexSubstitution(
        "Property",
        r"\bprop\b",
        "property",
    ),
    RegexSubstitution(
        "Criminal",
        r"\bcrim\b",
        "criminal",
    ),
    RegexSubstitution(
        "License",
        r"\blic\b",
        "license",
    ),
    RegexSubstitution(
        "Credit Card",
        r"\bcc\b",
        "credit card",
    ),
    RegexSubstitution(
        "Vehicle",
        r"\bveh\b",
        "vehicle",
    ),
    RegexSubstitution(
        "Assault",
        r"\baslt\b",
        "assault",
    ),
    RegexSubstitution(
        "Mentally",
        r"\bment\b",
        "mentally",
    ),
    RegexSubstitution(
        "Unknown",
        r"\bunk\b",
        "unknown",
    ),
    RegexSubstitution(
        "Statement",
        r"\bstmt\b",
        "statement",
    ),
    RegexSubstitution(
        "Degree",
        r"\bdeg\b",
        "degree",
    ),
    RegexSubstitution(
        "Robbery",
        r"\brobb\b",
        "robbery",
    ),
    RegexSubstitution(
        "Aggravated",
        r"\bagg\b",
        "aggravated",
    ),
    RegexSubstitution(
        "Forced",
        r"\bfrc\b",
        "forced",
    ),
    RegexSubstitution(
        "Danger",
        r"\bdng\b",
        "danger",
    ),
    RegexSubstitution(  # NOTE: Should be LOWEST
        "Substance",
        r"\bsub\b",
        "substance",
    ),
    RegexSubstitution(
        "Abetting",
        r"\babet\b",
        "abetting",
    ),
    RegexSubstitution(
        "Acquaintance",
        r"\bacq\b",
        "acquaintance",
    ),
    RegexSubstitution(
        "Adult",
        r"\badlt\b",
        "adult",
    ),
    RegexSubstitution(
        "Deliver",
        r"\bdel\b",
        "deliver",
    ),
    RegexSubstitution(
        "Within",
        r"\bw\/in\b",
        "within",
    ),
    RegexSubstitution(
        "Family",
        r"\bfam\b",
        "family",
    ),
    RegexSubstitution(
        "Burglary",
        r"\bburg\b",
        "burglary",
    ),
    RegexSubstitution(
        "Murder",
        r"\bmur\b",
        "murder",
    ),
    RegexSubstitution(
        "Representation",
        r"\brep\b",
        "representation",
    ),
    RegexSubstitution(
        "Previous",
        r"\bprev\b",
        "previous",
    ),
    RegexSubstitution(
        "Common",
        r"\bcom\b",
        "common",
    ),
]
