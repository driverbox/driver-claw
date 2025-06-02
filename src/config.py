from typing import Callable, Literal

from selenium.webdriver import Remote

import url

BASE_CONFIG: dict[
    Literal["display", "network", "miscellaneous", "tool"],
    list[dict[Literal["path", "url", "type"], str | Callable[[Remote], str]]]
] = {
    "display": [
        {
            "path": "AMD",
            "url": url.amd_display,
        },
        {
            "path": "Intel® Arc™ & Iris® Xe Graphics",
            "url": url.intel_display_arc,
        },
        {
            "path": "Intel® 7th-10th Gen Processor Graphics",
            "url": url.intel_display_uhd,
        },
        {
            "path": "Nvidia",
            "url": url.nvidia_display_game,
        }
    ],
    "network": [
        {
            "path": "Intel® Ethernet Adapter Complete Driver Pack",
            "url": url.intel_lan,
        },
        {
            "path": "Realtek",
            "url": url.realtek_lan,
        },
    ],
    "miscellaneous": [
        {
            "path": "AMD Chipset",
            "url": url.amd_chipset,
        },
        {
            "path": "Intel Chipset (INF Utility)",
            "url": url.intel_inf_utility,
        },
        {
            "path": "Intel® PPM",
            "url": url.intel_ppm,
        },
        {
            "path": "Intel® Wireless",
            "url": url.intel_wifi,
        },
        {
            "path": "Intel® Wireless",
            "url": url.intel_bluetooth,
        },
        {
            "path": "MediaTek MT7952_7927\\WIFI",
            "url": url.mediatek_7927_wifi,
        },
        {
            "path": "MediaTek MT7952_7927\\Bluetooth",
            "url": url.mediatek_7927_bluetooth,
        },
        {
            "path": "MediaTek MT7961_79X2\\WIFI",
            "url": url.mediatek_7922_wifi,
        },
        {
            "path": "MediaTek MT7961_79X2\\Bluetooth",
            "url": url.mediatek_7922_bluetooth,
        },
        {
            "path": "Qualcomm NCM865\\WIFI",
            "url": url.qualcomm_ncm865_wifi,
        },
        {
            "path": "Qualcomm NCM865\\Bluetooth",
            "url": url.qualcomm_ncm865_bluetooth,
        },
        {
            "path": "Realtek RTL8852BE\\WIFI",
            "url": url.realtek_8852be_wifi,
        },
        {
            "path": "Realtek RTL8852BE\\Bluetooth",
            "url": url.realtek_8852be_bluetooth,
        },
        {
            "path": "Realtek RTL8852CE\\WIFI",
            "url": url.realtek_8852ce_wifi,
        },
        {
            "path": "Realtek RTL8852CE\\Bluetooth",
            "url": url.realtek_8852ce_bluetooth,
        },
        {
            "path": "Realtek RTL8892AE\\WIFI",
            "url": url.realtek_8892ae_wifi,
        },
        {
            "path": "Realtek RTL8892AE\\Bluetooth",
            "url": url.realtek_8892ae_bluetooth,
        },
        {
            "path": "Realtek HD Universal",
            "url": url.realtek_audio,
        },
    ],
    "tool": [
        {
            "path": "y-cruncher",
            "url": url.y_cruncher
        },
        {
            "path": "HWInfo",
            "url": url.hwinfo
        },
        {
            "path": "OCCT",
            "url": url.occt
        },
        {
            "path": "CrystalDiskMark",
            "url": url.crystaldick_mark
        },
        {
            "path": "FurMark",
            "url": url.furmark
        },
        {
            "path": "CrystalDiskinfo",
            "url": url.crystaldick_info
        }
    ]
}
