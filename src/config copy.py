
"""Configuration module for driver download targets.

This module defines a structured dictionary `CLAW_PRIZES` that categorizes
various hardware-related drivers and utilities into groups such as 'display',
'network', 'miscellaneous', and 'tool'. Each entry specifies metadata for
downloading and optionally renaming driver files, including:

The configuration supports multiple vendors including AMD, Intel, Nvidia,
Realtek, MediaTek, and Qualcomm, and includes utility tools like CrystalDiskInfo,
FurMark, and HWInfo.
"""


import functools
from typing import Literal

import url
from driver_claw import ClawPrize

CLAW_PRIZES: dict[
    Literal['display', 'network', 'miscellaneous', 'tool'],
    list[ClawPrize]
] = {
    'tool': [
        {
            'path': 'y-cruncher',
            'url': url.y_cruncher,
            'file_type': 'zip/folder',
            'rename_as': None
        }
    ]
}
