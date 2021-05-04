import re
from dataclasses import dataclass
from string import punctuation
import pandas as pd

all_punctuation = punctuation + "‘’·—»"

# "regex separator"
# captures the following: 1+ spaces OR 1+ non-word characters (ex: "/", "-"), OR 1 word boundary
# apply the this variable using an `fr` string in the regex substituion (ex: `fr"\bw{sep}force\b"`)
sep = "(?: +|\W+|\b)"


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
    RegexRemoval(
        "Thurston Prefix", r"\S{1,2}\s\d\S{0,3}\.\d\S{0,3}\.\d\S{0,3}(?:\.\d?\S{0,3}?)?"
    ),
]

substitutions = [
    # RegexSubstitution("Less Than", r"(?:&LT;|lt|\<)", " < "), # TODO turn back on LT but with word boundaries etc
    # RegexSubstitution("Greater Than", r"(?:&GT;|gt|\>)", " > "), # TODO turn back on GT but with word boundaries etc
    # WITH terms ===========
    RegexSubstitution("With Out", fr"\bw{sep}(?:o|out)\b", "without"),
    RegexSubstitution("With Out 2", fr"\bwo\b", "without"),
    RegexSubstitution("Within", fr"\bw{sep}(?:i|in)\b", "within", priority=20),
    RegexSubstitution(
        "With Intent",
        fr"\bw{sep}\s?in?t?e?n?t?\b",
        "with intent",
    ),
    RegexSubstitution(
        "with a",
        fr"\bw{sep}a\b",
        "with a",
    ),
    RegexSubstitution(
        "with report",
        fr"\bw{sep}report\b",
        "with report",
    ),
    RegexSubstitution(
        "with license",
        fr"\bw{sep}license\b",
        "with license",
    ),
    RegexSubstitution(
        "with murder",
        fr"\bw{sep}murder\b",
        "with murder",
    ),
    RegexSubstitution(
        "with injury",
        fr"\bw{sep}(?:injury|inj)\b",
        "with injury",
    ),
    RegexSubstitution(
        "with turned",
        fr"\bw{sep}turned\b",
        "with turned",
    ),
    RegexSubstitution(
        "with altered",
        fr"\bw{sep}alt\b",
        "with altered",
    ),
    RegexSubstitution(
        "with deadly",
        fr"\bw{sep}deadly\b",
        "with deadly",
    ),
    RegexSubstitution(
        "with dangerous weapon",
        fr"\b(?:with|w){sep}(?:dangerous|d){sep}(?:weapon|wpn|weapn|weap)\b",
        "with dangerous weapon",
    ),
    RegexSubstitution(
        "with child",
        fr"\b(?:with|w){sep}(?:child|chi|chld)\b",
        "with child",
    ),
    RegexSubstitution(
        "with minor",
        fr"\bw{sep}minor\b",
        "with minor",
    ),
    RegexSubstitution(
        "with kidnapping",
        fr"\bw{sep}kidnapping\b",
        "with kidnapping",
    ),
    RegexSubstitution(
        "with agency",
        fr"\bw{sep}agency\b",
        "with agency",
    ),
    RegexSubstitution(
        "with firearm",
        fr"\bw{sep}firearm\b",
        "with firearm",
    ),
    RegexSubstitution(
        "with weapon",
        fr"\bw{sep}(?:weapon|wpn|weapn|weap)\b",
        "with weapon",
    ),
    RegexSubstitution(
        "with knife",
        fr"\bw{sep}knife\b",
        "with knife",
    ),
    RegexSubstitution(
        "with force",
        fr"\bw{sep}force\b",
        "with force",
    ),
    RegexSubstitution(
        "with extenuating circumstances",
        fr"\bw{sep}ext{sep}circumstances\b",
        "with extenuating circumstances",
    ),
    RegexSubstitution(
        "with prior",
        fr"\bw{sep}prior\b",
        "with prior",
    ),
    RegexSubstitution(
        "with previous",
        fr"\bw{sep}previous\b",
        "with previous",
    ),
    RegexSubstitution(
        "with domestic violence",
        fr"\bw{sep}dv\b",
        "with domestic violence",
    ),
    RegexSubstitution(
        "with suspended",
        fr"\bw{sep}suspended\b",
        "with suspended",
    ),
    RegexSubstitution(  # doublecheck this
        "vehicle with",
        fr"\bvehicle{sep}w{sep}",
        "vehicle with",
    ),
    RegexSubstitution(  # TODO: is this "possession with" or "possession weapon"? see concealed weapon as example
        "possession with",
        fr"\b(?:possession|possess){sep}w{sep}",
        "possession with",
    ),
    RegexSubstitution(
        "neglect with",
        fr"\bneglect{sep}w{sep}",
        "neglect with",
    ),
    RegexSubstitution(
        "cooperate with",
        fr"\bcooperate{sep}w{sep}",
        "cooperate with",
    ),
    RegexSubstitution(
        "interfere with",
        fr"\binterfere{sep}w{sep}",
        "interfere with",
    ),
    RegexSubstitution(  # TODO consolidate tamper/tampering?
        "tamper with",
        fr"\btamper{sep}w{sep}",
        "tamper with",
    ),
    RegexSubstitution(
        "tampering with",
        fr"\btampering{sep}w{sep}",
        "tampering with",
    ),
    RegexSubstitution(
        "assault with",
        fr"\bassault{sep}w{sep}",
        "assault with",
    ),
    # FIREARM TERMS
    RegexSubstitution(
        "firearm with altered identification numbers",
        fr"\bfirearm{sep}(?:with|w){sep}alter\b",
        "firearm with altered identification numbers",
    ),
    RegexSubstitution(
        "firearm",
        fr"\bf{sep}a\b",
        "firearm",
    ),
    RegexSubstitution(
        "intimidation",
        fr"\b(?:intim|intimid)\b",
        "intimidation",
    ),
    # DOMESTIC VIOLENCE TERMS / PROTECTION / RESTRAINING ORDERS
    RegexSubstitution(
        "protective order",
        r"\b(?:protective|protection|prot){sep}(?:order|ord|or)\b",
        "protective order",
    ),
    RegexSubstitution(
        "domestic violence protective order",
        r"\bdvpo\b",
        "domestic violence protective order",
    ),
    RegexSubstitution("domestic", r"\bdom\b", "domestic", priority=20),
    RegexSubstitution(
        "domestic violence",
        r"\bdv\b",
        "domestic violence",
    ),
    RegexSubstitution(
        "domestic violence 2",
        fr"\bd{sep}v\b",
        "domestic violence",
    ),
    RegexSubstitution(
        "witness testimony",
        fr"\bwit{sep}tes\b",
        "witness testimony",
    ),
    # CONVICTION TERMS ==
    RegexSubstitution(
        "misdemeanor conviction",
        fr"\b(?:misdemeanor|misd){sep}(?:convic|conv)\b",
        "misdemeanor conviction",
    ),
    RegexSubstitution(
        "prior conviction",
        fr"\b(?:prior|pr|pri){sep}(?:convic|conv)\b",
        "prior conviction",
    ),
    # ==== GENERAL TERMS =====
    RegexSubstitution(
        "offender accountability act",
        fr"\boaa\b",
        "offender accountability act",
    ),
    RegexSubstitution(
        "interfere",
        fr"\b(?:interf|interfer)\b",
        "interfere",
    ),
    RegexSubstitution(  # TODO should we leave obstructing/obstruction separate terms or lump into obstruct?
        "obstruct",
        fr"\b(?:ob|obstructing|obstruction)\b",
        "obstruct",
    ),
    RegexSubstitution(
        "law enforcement officer",
        fr"\bleo\b",
        "law enforcement officer",
    ),
    RegexSubstitution(
        "minor",
        fr"\bminr\b",
        "minor",
    ),
    RegexSubstitution(
        "major",
        fr"\bmajr\b",
        "major",
    ),
    RegexSubstitution(
        "willful",
        fr"\b(?:wilfl|wlfl)\b",
        "willful",
    ),
    RegexSubstitution(
        "issue worthless checks",
        fr"\b(?:issue|iss){sep}(?:worthless|wrthlss|wrtls){sep}(?:checks|cks)\b",
        "worthless",
    ),
    RegexSubstitution(
        "issue multiple worthless checks",
        fr"\b(?:issue|iss){sep}(?:multiple|mltpl){sep}(?:worthless|wrthlss|wrtls){sep}(?:checks|cks)\b",
        "worthless",
    ),
    RegexSubstitution(
        "unauthorized",
        fr"\b(?:unauth|unau|unauthd)\b",
        "unauthorized",
    ),
    RegexSubstitution(
        "child support",
        fr"\b(?:child|chld|chi){sep}(?:support|supp|sup)\b",
        "child support",
    ),
    RegexSubstitution(
        "unlawful",
        r"\b(?:unlawfully|unlaw|unlawfl|unlawf)\b",
        "unlawful",
    ),
    RegexSubstitution(
        "Possession",
        r"\bposs?\b",
        "possession",
    ),
    RegexSubstitution(
        "Embezzlement",
        r"\b(?:embezzle|embezz|embez)\b",
        "possession",
    ),
    RegexSubstitution(
        "Abetting",
        r"\b(?:abett|abetted)\b",
        "Abetting",
    ),
    RegexSubstitution("emergency", r"\b(?:emerg|emer)\b", "emergency", priority=20),
    RegexSubstitution(
        "Attempted",
        r"\batt\b",
        "attempted",
    ),
    RegexSubstitution(
        "Battery",
        r"\bbatt\b",
        "battery",
    ),
    RegexSubstitution(
        "Violation of Probation",
        r"\bvop\b",
        "violation of probation",
    ),
    RegexSubstitution(  # TODO revisit this - 'con' shows up in some DV-related text, may not be a one-size fits all regex / 'consp' to conspiracy or conspire?
        "Conspiracy",
        r"\b(?:con|consp)\b",
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
        "electric power",
        r"\belec{sep}pwr\b",
        "electric power",
    ),
    # VEHICLE terms ===========
    RegexSubstitution(
        "Vehicle",
        r"\bveh\b",
        "vehicle",
    ),
    RegexSubstitution(
        "Vehicles",
        r"\bvehs\b",
        "vehicles",
    ),
    RegexSubstitution(
        "commercial motor vehicle",
        r"\bcmv\b",
        "commercial motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle",
        fr"\b(?:mtr|mot){sep}(?:vehicle|veh)\b",
        "motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle 2",
        fr"\bm{sep}v\b",
        "motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle 3",
        fr"\b(?:mtv|mv)\b",
        "motor vehicle",
    ),
    RegexSubstitution("odometer", fr"\bodom\b", "odometer"),
    # =====
    RegexSubstitution(
        "Assault",
        r"\bass?lt\b",
        "assault",
    ),
    RegexSubstitution(
        "Assault 2",
        r"\bass\b",
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
        r"\bdegr?e?\b",
        "degree",
    ),
    RegexSubstitution(
        "Felony",
        r"\b(?:fe|fel|felo|felny)\b",
        "felony",
    ),
    RegexSubstitution(
        "misdemeanor",
        r"\bmisd\b",
        "misdemeanor",
    ),
    # AGE / FEMALE
    RegexSubstitution(
        "age female",
        fr"\bage{sep}f\b",
        "age female",
    ),
    RegexSubstitution(
        "old female",
        fr"\bold{sep}f\b",
        "old female",
    ),
    RegexSubstitution(
        "older female",
        fr"\bolder{sep}f\b",
        "older female",
    ),
    RegexSubstitution(
        "13 female",
        fr"\b13{sep}f\b",
        "13 female",
    ),
    RegexSubstitution(
        "15 female",
        fr"\b15{sep}f\b",
        "15 female",
    ),
    RegexSubstitution(
        "17 female",
        fr"\b17{sep}f\b",
        "17 female",
    ),
    # AGE / MALE
    RegexSubstitution(
        "age male",
        fr"\bage{sep}m\b",
        "age male",
    ),
    RegexSubstitution(
        "old male",
        fr"\bold{sep}m\b",
        "old male",
    ),
    RegexSubstitution(
        "older male",
        fr"\bolder{sep}m\b",
        "older male",
    ),
    RegexSubstitution(
        "13 male",
        fr"\b13{sep}m\b",
        "13 male",
    ),
    RegexSubstitution(
        "15 male",
        fr"\b15{sep}m\b",
        "15 male",
    ),
    RegexSubstitution(
        "17 male",
        fr"\b17{sep}m\b",
        "17 male",
    ),
    # ======
    RegexSubstitution(
        "Robbery",
        r"\brobb\b",
        "robbery",
    ),
    RegexSubstitution(
        "Attempted Robbery",
        fr"\battempted{sep}(?:rob|robb)\b",
        "attempted robbery",
    ),
    RegexSubstitution(
        "Detainer Robbery",
        fr"\bdetainer{sep}(?:rob|robb)\b",
        "detainer robbery",
    ),
    RegexSubstitution(
        "Aggravated",
        r"\b(?:agg|aggrav|aggr|aggravted)\b",
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
        "Breaking and Entering",
        r"\bB ?& ?E\b",
        "breaking and entering",
    ),
    RegexSubstitution("Building", r"\bbldg\b", "building"),
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
        "conspiracy to commit",
        fr"\bconsp{sep}comm\b",
        "conspiracy to commit",
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
    RegexSubstitution(  # TODO revisit this - 'viol' relates to 'violation' too
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
        r"\b(?:hh|hsehld|hhld)\b",
        "household",
    ),
    RegexSubstitution(
        "Other",
        r"\both\b",
        "other",
    ),
    # WEAPON TERMS =========
    RegexSubstitution(
        "Weapon", r"\b(?:wea|wpn|weapn|weap|weapo)\b", "weapon", priority=20
    ),
    RegexSubstitution(
        "Weapons", r"\b(?:wea|wpn|weapn|weap|weapo)s\b", "weapons", priority=20
    ),
    RegexSubstitution("dangerous weapon", r"\bdw\b", "dangerous weapon"),
    RegexSubstitution("dangerous weapon 2", fr"\bd{sep}w\b", "dangerous weapon"),
    RegexSubstitution("concealed weapon", fr"\bconcealed{sep}w\b", "concealed weapon"),
    # HARM terms =======
    RegexSubstitution(
        "Bodily Harm",
        fr"\b(?:bod{sep}ha?rm|bh)\b",
        "bodily harm",
    ),
    RegexSubstitution(
        "Great Bodily",
        fr"\bgrt{sep}bodily\b",
        "great bodily",
    ),
    RegexSubstitution(
        "Great Bodily Injury",
        fr"\bgbi\b",
        "great bodily injury",
    ),
    RegexSubstitution(
        "Substantial Bodily Harm",
        r"\bsbh\b",
        "substantial bodily harm",
    ),
    RegexSubstitution(
        "injury",
        r"\binj\b",
        "injury",
    ),
    RegexSubstitution(
        "inflict",
        r"\binflt\b",
        "inflict",
    ),
    # ====
    RegexSubstitution(
        "Personal",
        r"\bpers\b",
        "personal",
    ),
    RegexSubstitution(
        "false",
        r"\bfls\b",
        "false",
    ),
    RegexSubstitution(
        "imprisonment",
        r"\b(?:imprison|impris|imprsn)\b",
        "imprisonment",
    ),
    RegexSubstitution(
        "prohibited",
        r"\bproh\b",
        "prohibited",
    ),
    RegexSubstitution(
        "alcoholic beverage", r"\balc\Wbev\b", "alcoholic beverage", priority=20
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
        "operate",
        r"\b(?:oper|op)\b",
        "operate",
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
        r"\bterr(?:\W|\b)thrts\b",
        "terrorism threats",
    ),
    # SEXUAL OFFENSES  =====
    RegexSubstitution(
        "Criminal Sexual Conduct",
        r"\bcsc\b",
        "criminal sexual conduct",
    ),
    RegexSubstitution(
        "sexual offense",
        r"\b(?:sexual|sex){sep}(?:offense|offen|off)\b",
        "sexual offense",
    ),
    RegexSubstitution(
        "sexual offenses",
        r"\b(?:sexual|sex){sep}(?:offense|offen|off)s\b",
        "sexual offenses",
    ),
    RegexSubstitution(
        "sexual assault",
        fr"\b(?:sexual|sex){sep}(?:assault|assult|assualt|ass|asst)\b",
        "sexual assault",
    ),
    RegexSubstitution(
        "sexual contact",
        fr"\b(?:sexual|sex){sep}(?:contact)\b",
        "sexual contact",
    ),
    RegexSubstitution(
        "sex act",
        fr"\b(?:sexual|sex){sep}(?:act|acts)\b",
        "sex act",
    ),
    RegexSubstitution(
        "sexual abuse",
        fr"\b(?:sexual|sex){sep}(?:abuse|ab)\b",
        "sexual abuse",
    ),
    RegexSubstitution(
        "commit sex abuse",
        fr"\bcomm{sep}sex{sep}abuse\b",
        "commit sex abuse",
    ),
    RegexSubstitution(
        "commit sex act",
        fr"\bcomm{sep}sex{sep}act\b",
        "commit sex act",
    ),
    RegexSubstitution(
        "commit sex abuse minor",
        fr"\bcommsexabuseminor\b",
        "commit sex abuse minor",
    ),
    RegexSubstitution(
        "sexual battery",
        fr"\b(?:sexual|sex){sep}(?:battery|batt|bat)\b",
        "sexual battery",
    ),
    RegexSubstitution(  # TODO: should these actually map to "sexual misconduct"?
        "sexual conduct",
        fr"\b(?:sexual|sex){sep}(?:conduct|cndct|cond|con)\b",
        "sexual conduct",
    ),
    RegexSubstitution(
        "sexual penetration",
        fr"\b(?:sexual|sex){sep}(?:penetration|pen)\b",
        "sexual penetration",
    ),
    RegexSubstitution(  # TODO: Revisit - hard to tell if exp/expl maps to "exploitation" or "explicit"
        "sexual exploitation",
        fr"\b(?:sexual|sex){sep}(?:exploitation|exploit)\b",
        "sexual exploitation",
    ),
    RegexSubstitution(
        "sexual performance",
        fr"\b(?:sexual|sex){sep}(?:performance|perform)\b",
        "sexual performance",
    ),
    RegexSubstitution(
        "sexual imposition",
        fr"\b(?:sexual|sex){sep}(?:imposition|imp)\b",
        "sexual imposition",
    ),
    RegexSubstitution(  # TODO: Revisit - hard to tell if offen/off maps to "offender" or "offense"
        "sex offender",
        fr"\b(?:sexual|sex){sep}(?:offender|offend|offndr|ofndr)\b",
        "sex offender",
    ),
    RegexSubstitution(
        "sexual predator",
        fr"\b(?:sexual|sex){sep}(?:predator|pred)\b",
        "sexual predator",
    ),
    # ====
    RegexSubstitution(
        "type",
        r"\btyp\b",
        "type",
    ),
    RegexSubstitution(
        "misconduct",
        r"\bmiscond\b",
        "misconduct",
    ),
    RegexSubstitution(
        "mischief",
        r"\bmisch\b",
        "mischief",
    ),
    RegexSubstitution(
        "probation revocation",
        fr"\bprob{sep}(?:rev|revo)\b",
        "probation revocation",
    ),
    RegexSubstitution(
        "management",
        r"\bmgmt\b",
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
    RegexSubstitution(
        "community custody",
        r"\bcomm custody\b",
        "community custody",
    ),
    RegexSubstitution(
        "contempt",
        r"\bcntmpt\b",
        "contempt",
    ),
    RegexSubstitution(
        "counterfeit",
        r"\b(?:cntft|cntrft|cntrfeit|cnterft)\b",
        "counterfeit",
    ),
    RegexSubstitution(
        "counts",
        r"\bcnts\b",
        "counts",
    ),
    RegexSubstitution(
        "victim",
        r"\b(?:vict|vctm)\b",
        "victim",
    ),
    # NUMBER TERMS ===========
    RegexSubstitution("first", r"\b1st\b", "first", priority=20),
    RegexSubstitution(
        "first degree", r"\b(?:first|1|1st){sep}(?:dgr|dg)\b", "first degree"
    ),
    RegexSubstitution(
        "circumstances in the first degree",
        fr"\bcircumstances{sep}1\b",
        "circumstances in the first degree",
    ),
    RegexSubstitution("second", r"\b2nd\b", "second", priority=20),
    RegexSubstitution(
        "second degree", r"\b(?:second|2|2nd){sep}(?:dgr|dg)\b", "second degree"
    ),
    RegexSubstitution(
        "circumstances in the second degree",
        fr"\bcircumstances{sep}2\b",
        "circumstances in the second degree",
    ),
    RegexSubstitution("third", r"\b3rd\b", "third", priority=20),
    RegexSubstitution(
        "third degree", r"\b(?:third|3|3rd){sep}(?:dgr|dg)\b", "third degree"
    ),
    RegexSubstitution(
        "circumstances in the third degree",
        fr"\bcircumstances{sep}3\b",
        "circumstances in the third degree",
    ),
    RegexSubstitution("fourth", r"\b4th\b", "fourth", priority=20),
    RegexSubstitution("fifth", r"\b5th\b", "fifth", priority=20),
    RegexSubstitution("sixth", r"\b6th\b", "sixth", priority=20),
    RegexSubstitution("seventh", r"\b7th\b", "seventh", priority=20),
    RegexSubstitution("eighth", r"\b8th\b", "eighth", priority=20),
    RegexSubstitution("ninth", r"\b9th\b", "ninth", priority=20),
    RegexSubstitution("tenth", r"\b10th\b", "tenth", priority=20),
    # SCHEDULE terms ===========
    # observed "l" for use of "i" across schedule terms
    RegexSubstitution("Schedule", r"\b(?:sc?he?d?|sch)\b", "schedule", priority=20),
    RegexSubstitution(
        "schedule one",
        fr"\bschedule{sep}(?:i|1|l)\b",
        "schedule one",
    ),
    RegexSubstitution(
        "schedule two",
        fr"\bschedule{sep}(?:ii|2|ll)\b",
        "schedule two",
    ),
    RegexSubstitution(
        "schedule three",
        fr"\bschedule{sep}(?:iii|3|lll)\b",
        "schedule three",
    ),
    RegexSubstitution(
        "schedule four",
        fr"\bschedule{sep}(?:iv|4|lv)\b",
        "schedule four",
    ),
    RegexSubstitution(
        "schedule five",
        fr"\bschedule{sep}(?:v|5)\b",
        "schedule five",
    ),
    RegexSubstitution(
        "schedule six",
        fr"\bschedule{sep}(?:vi|6|vl)\b",
        "schedule six",
    ),
    # DRIVING TERMS ===========
    RegexSubstitution(
        "driving",
        r"\bdrvg\b",
        "driving",
    ),
    RegexSubstitution(
        "driving 2",
        r"\bdriv{sep}g\b",
        "driving",
    ),
    RegexSubstitution(
        "driving under the influence",
        r"\bdui\b",
        "driving under the influence",
    ),
    RegexSubstitution(
        "driving while impaired",
        r"\bdwi\b",
        "driving while impaired",
    ),
    RegexSubstitution(
        "driving while license suspended",
        r"\bdwls\b",
        "driving while license suspended",
    ),
    RegexSubstitution(
        "driving while license revoked",
        r"\bdwlr\b",
        "driving while license revoked",
    ),
    RegexSubstitution(
        "revoked",
        r"\brevkd\b",
        "revoked",
    ),
    RegexSubstitution(
        "reckless endangerment",
        fr"\breckles{sep}endanger\b",
        "reckless endangerment",
    ),
    RegexSubstitution(
        "highway",
        fr"\bhi{sep}way\b",
        "highway",
    ),
    # ========
    RegexSubstitution(
        "retail theft",
        fr"\bretail{sep}thft\b",
        "retail theft",
    ),
    RegexSubstitution(
        "impregnate girl",
        fr"\b(?:impregnate|impreg){sep}(?:girl|grl)\b",
        "impregnate girl",
    ),
    RegexSubstitution(
        "worker compensation",
        fr"\bwrkr{sep}cmp\b",
        "worker compensation",
    ),
    RegexSubstitution(
        "disregard",
        fr"\bdisreg\b",
        "disregard",
    ),
    RegexSubstitution(
        "red light",
        fr"\bred{sep}light\b",
        "red light",
    ),
    RegexSubstitution(
        "electrical appliance",
        fr"\belct{sep}appl\b",
        "electrical appliance",
    ),
    RegexSubstitution(
        "serial number",
        fr"\b(?:serial|ser){sep}(?:number|nmbr|num|nu|no)\b",
        "serial number",
    ),
    # DISTRIBUTION / FURNISH / TRAFFICK TERMS =======
    RegexSubstitution(  # TODO: revisit traff/traf', more likely to be traffick/ing but could be traffic (cars)
        "traffick",
        r"\b(?:tfk|traff|traf)\b",
        "traffick",
    ),
    RegexSubstitution(  # TODO: revisit adding 'dist', more likely to be distribution but could be disturbance
        "distribution",
        r"\b(?:distr|distrib)\b",
        "distribution",
    ),
    RegexSubstitution(
        "furnish",
        r"\b(?:furnishing|furn)\b",
        "furnish",
    ),
    RegexSubstitution(  # TODO: revisit adding 'man', more likely to be manufacture/ing but could have other meaning
        "manufacturing",
        r"\b(?:mfg|manuf|manu)\b",
        "manufacturing",
    ),
    # DRUG TERMS ===========
    RegexSubstitution(
        "marijuana",
        r"\b(?:marij|marihuana|mari|marijuan|marijua|mariju|mj)\b",
        "marijuana",
    ),
    RegexSubstitution(  # TODO : evaluate adding "coc" for cocaine... it may also connect to "contempt of court" / most likely cocaine
        "cocaine",
        r"\b(?:cocain|coca|cocai)\b",
        "cocaine",
    ),
    RegexSubstitution(
        "rohypnol",
        r"\brohypnl\b",
        "rohypnol",
    ),
    RegexSubstitution(
        "heroine",
        r"\bher\b",
        "heroine",
    ),
    RegexSubstitution(
        "methamphetamine",
        r"\b(?:meth|metham|methamphet|methamph)\b",
        "methamphetamine",
    ),
    RegexSubstitution(
        "paraphernalia",
        r"\b(?:para|paraph|paraphenalia|parap)\b",
        "paraphernalia",
    ),
    # ALCOHOL TERMS ===========
    RegexSubstitution(
        "blood alcohol concentration",
        r"\bbac\b",
        "blood alcohol concentration",
    ),
    RegexSubstitution(
        "alcohol",
        r"\b(?:alc|alch|alchol|alcohl|alco|alcoh)\b",
        "alcohol",
    ),
    RegexSubstitution(
        "over legal",
        r"\b(?:over|ov){sep}(?:legal|leg)\b",
        "over legal",
    ),
    # SUBSTANCE TERMS ========
    RegexSubstitution(
        "Substance",
        r"\b(?:sub|subs|substanc|substan|substnces|subtance|substa|substnc|sunstance)\b",
        "substance",
        20,
    ),
    RegexSubstitution("controlled", r"\b(?:cntrld|cntrl)\b", "controlled", 20),
    RegexSubstitution(
        "controlled dangerous substances",
        r"\bcds\b",
        "controlled dangerous substances",
    ),
    RegexSubstitution(
        "Controlled Substance",
        fr"\bcont?r?{sep}?subs?t?(?:\b|stance\b)",
        "controlled substance",
    ),
    RegexSubstitution(
        "Controlled Substance 2",
        r"\bc\W?s\b",
        "controlled substance",
    ),
    RegexSubstitution(
        "unlawful possession of a controlled substance",
        r"\bupcs\b",
        "unlawful possession of a controlled substance",
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
