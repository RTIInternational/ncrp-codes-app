import re
from dataclasses import dataclass
from string import punctuation
import pandas as pd

all_punctuation = punctuation + "‘’"


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
    priority: int = 1  # higher → run later

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
    RegexSubstitution("Less Than", r"(?:&LT;|\<)", " < "),
    RegexSubstitution("Greater Than", r"(?:&GT;|\>)", " > "),
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
        r"\bcont?r?(?:\b|\W)(?:\b|\W)?subs?t?(?:\b|stance\b)",
        "controlled substance",
    ),
    RegexSubstitution(
        "Controlled Substance 2",
        r"\bc\W?s\b",
        "controlled substance",
    ),
    RegexSubstitution(
        "Possession",
        r"\bposs?\b",
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
        r"\bass?lt\b",
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
    RegexSubstitution("Substance", r"\bsub\b", "substance", 20),
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
    RegexSubstitution(
        "of a",
        r"\bofa\b",
        "of a",
    ),
    RegexSubstitution(
        "violent",
        r"\bviol\b",
        "violent",
    ),
    RegexSubstitution(
        "perform",
        r"\bperf\b",
        "perform",
    ),
    RegexSubstitution(
        "official",
        r"\boffl\b",
        "official",
    ),
    RegexSubstitution(
        "household",
        r"\b(?:hh|hsehld)\b",
        "household",
    ),
    RegexSubstitution(
        "Other",
        r"\both\b",
        "other",
    ),
    RegexSubstitution(
        "Weapon",
        r"\bweap\b",
        "weapon",
    ),
    RegexSubstitution(
        "Bodily Harm",
        r"\bbod\Wha?rm\b",
        "bodily harm",
    ),
    RegexSubstitution(
        "Schedule",
        r"\bsc?he?d?\b",
        "schedule",
    ),
    RegexSubstitution(
        "Personal",
        r"\bpers\b",
        "personal",
    ),
    RegexSubstitution(
        "prohibited",
        r"\bproh\b",
        "prohibited",
    ),
    RegexSubstitution(
        "alcoholic beverage",
        r"\balc\Wbev\b",
        "alcoholic beverage",
    ),
    RegexSubstitution(
        "manufacturing",
        r"\b(?:mfg|manuf)\b",
        "manufacturing",
    ),
    RegexSubstitution(
        "domestic",
        r"\bdom\b",
        "domestic",
    ),
    RegexSubstitution(
        "distribution",
        r"\bdist\b",
        "distribution",
    ),
    RegexSubstitution(
        "stolen",
        r"\bstln\b",
        "stolen",
    ),
    RegexSubstitution(
        "years",
        r"\byrs\b",
        "years",
    ),
    RegexSubstitution(
        "intent",
        r"\bint\b",
        "intent",
    ),
    RegexSubstitution(
        "manufacturing or delivering",
        r"\bman\Wdel\b",
        "manufacturing delivering",
    ),
    RegexSubstitution(  # Revisit this
        "minimum mandatory",
        r"\bmin\Wman\b",
        "minimum mandatory",
    ),
    RegexSubstitution(
        "stranger",
        r"\bstr(?:ngr)?\b",
        "stranger",
    ),
    RegexSubstitution(
        "personal use",
        r"\bpers use\b",
        "personal use",
    ),
    RegexSubstitution(
        "force",
        r"\bfo?rc\b",
        "force",
    ),
    RegexSubstitution(
        "occupied",
        r"\bocc\b",
        "occupied",
    ),
    RegexSubstitution(
        "residence",
        r"\bres\b",
        "residence",
    ),
    RegexSubstitution(
        "terrorism threats",
        r"\bterr thrts\b",
        "terrorism threats",
    ),
    RegexSubstitution(
        "sexual offense",
        r"\bsex off\b",
        "sexual offense",
    ),
    RegexSubstitution(
        "type",
        r"\btyp\b",
        "type",
    ),
    RegexSubstitution(
        "probation revocation",
        r"\bprob rev\b",
        "probation revocation",
    ),
    RegexSubstitution(
        "management",
        r"\bmg,t\b",
        "management",
    ),
    RegexSubstitution(
        "subsistence",
        r"\bsubsist\b",
        "subsistence",
    ),
    RegexSubstitution(
        "penalty group",
        r"\bpg\b",
        "penalty group",
    ),
]


def cleaner(text):
    if pd.isnull(text):
        return ""
    # Remove Commas from Numbers
    text = re.sub(r"(\d+?),(\d+?)", r"\1\2", text)
    # TODO: double check this `'s` regex
    text = re.sub(r"\b(\S+?)'(s)", r"\1\2", text)
    # Do all substitutions (Case insensitive on raw text)
    substitutions_sorted = sorted(substitutions, key=lambda s: s.priority)
    for substitution in substitutions_sorted:
        text = re.sub(substitution.regex, substitution.replacement, text)
    # Remove any terms we don't want
    for removal in removals:
        text = re.sub(removal.regex, " ", text)
    # Then remove remaining punctuation
    for punct in all_punctuation:
        text = text.replace(punct, " ")
    text = " ".join(text.split())  # removes extra spaces: "  " → " "
    text = text.lower()
    return text
