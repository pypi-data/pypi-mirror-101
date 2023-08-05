"""scrapli_cfg.platform.core.juniper_junos.patterns"""
import re

VERSION_PATTERN = re.compile(
    pattern=r"\d+\.\w+\.\w+",
)
OUTPUT_HEADER_PATTERN = re.compile(pattern=r"^## last commit.*$\nversion.*$", flags=re.M | re.I)
EDIT_PATTERN = re.compile(pattern=r"^\[edit\]$", flags=re.M)
