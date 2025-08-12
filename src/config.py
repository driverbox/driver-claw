
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
    'display': [
        {
            'path': 'AMD',
            'url': functools.partial(
                    url.amd,
                    url='https://www.amd.com/en/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-9000-series/amd-radeon-rx-9070-xt.html',
                    dri_name='win10-win11'),
            'file_type': 'zip',
            'rename_as': None
        },
        {
            'path': 'Intel® 7th-10th Gen Processor Graphics',
            'url': functools.partial(
                url.intel,
                url='https://www.intel.com/content/www/us/en/download/776137/intel-7th-10th-gen-processor-graphics-windows.html'
            ),
            'file_type': 'zip',
            'rename_as': None
        },
        {
            'path': 'Intel® Arc™ & Iris® Xe Graphics',
            'url': functools.partial(
                url.intel,
                url='https://www.intel.com/content/www/us/en/download/785597/intel-arc-iris-xe-graphics-windows.html'
            ),
            'file_type': 'zip',
            'rename_as': None
        },
        {
            'path': 'Nvidia',
            'url': functools.partial(url.nvidia_grd, dri_type='desktop'),
            'file_type': 'zip',
            'rename_as': None
        }
    ],
    'miscellaneous': [
        {
            'path': 'AMD Chipset',
            'url': functools.partial(
                url.amd,
                url='https://www.amd.com/en/support/downloads/drivers.html/chipsets/am5/x870e.html',
                dri_name='chipset'),
            'file_type': 'exe',
            'rename_as': 'AMD_Chipset_Software'
        },
        {
            'path': 'Intel Chipset (INF Utility)',
            'url': functools.partial(
                url.intel,
                url='https://www.intel.com/content/www/us/en/download/19347/chipset-inf-utility.html'
            ),
            'file_type': 'exe',
            'rename_as': None
        },
        {
            'path': 'Intel® PPM',
            'url': functools.partial(
                url.gigabyte,
                url='https://www.gigabyte.com/Motherboard/B860M-AORUS-ELITE-WIFI6E/support#support-dl-driver-wlanbt',
                dri_name='Platform Power Management(PPM)'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_3713_ppm'
        },
        {
            'path': 'Intel® Wireless',
            'url': functools.partial(
                url.intel,
                url='https://www.intel.com.tw/content/www/us/en/download/19351/intel-wireless-wi-fi-drivers-for-windows-10-and-windows-11.html'
            ),
            'file_type': 'exe',
            'rename_as': 'WiFi-Driver64-Win10-Win11'
        },
        {
            'path': 'Intel® Wireless',
            'url': functools.partial(
                url.intel,
                url='https://www.intel.com.tw/content/www/us/en/download/18649/intel-wireless-bluetooth-drivers-for-windows-10-and-windows-11.html'
            ),
            'file_type': 'exe',
            'rename_as': 'BT-UWD-Win10-Win11'
        },
        {
            'path': 'MediaTek MT7961_79X2\\Bluetooth',
            'url': functools.partial(
                url.gigabyte,
                url='https://www.gigabyte.com/hk/Motherboard/B850M-FORCE-WIFI6E/support#dl',
                dri_name='MediaTek Wi-Fi 6E Bluetooth Driver'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_4717_mtk6e'
        },
        {
            'path': 'MediaTek MT7961_79X2\\WIFI',
            'url': functools.partial(
                url.gigabyte,
                url='https://www.gigabyte.com/hk/Motherboard/B850M-FORCE-WIFI6E/support#dl',
                dri_name='MediaTek Wi-Fi 6E WIFI Driver'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_4716_mtk6ewifi'
        },
        {
            'path': 'MediaTek MT7952_7927\\Bluetooth',
            'url': functools.partial(
                url.gigabyte_wifi_card,
                dri_type='GC-WIFI7 1.1',
                dri_name='Bluetooth'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_2683_mtk'
        },
        {
            'path': 'MediaTek MT7952_7927\\WIFI',
            'url': functools.partial(
                url.gigabyte_wifi_card,
                dri_type='GC-WIFI7 1.1',
                dri_name='WIFI'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_2682_mtk'
        },
        {
            'path': 'Qualcomm NCM865\\Bluetooth',
            'url': functools.partial(
                url.gigabyte_wifi_card,
                dri_type='GC-WIFI7 1.0',
                dri_name='Bluetooth'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_2687_qualcomm'
        },
        {
            'path': 'Qualcomm NCM865\\WIFI',
            'url': functools.partial(
                url.gigabyte_wifi_card,
                dri_type='GC-WIFI7 1.0',
                dri_name='WIFI'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_2686_qualcomm'
        },
        {
            'path': 'Realtek HD Universal',
            'url': functools.partial(
                url.msi,
                url='https://hk.msi.com/Motherboard/MAG-X870-TOMAHAWK-WIFI/support#driver',
                dri_type='On-Board Audio Drivers',
                dri_name='Realtek HD Universal Driver'
            ),
            'file_type': 'zip/folder',
            'rename_as': None
        },
        {
            'path': 'Realtek RTL8852BE\\Bluetooth',
            'url': 'https://dlcdnets.asus.com/pub/ASUS/mb/02BT/DRV_BT_RTK_8852BE_SZ-TSD_W11_64_V1640132401503_20240924R.zip?model=PRIME%20B650M-A%20WIFI',
            'file_type': 'zip',
            'rename_as': None
        },
        {
            'path': 'Realtek RTL8852BE\\WIFI',
            'url': 'https://dlcdnets.asus.com/pub/ASUS/mb/08WIRELESS/DRV_WiFi_RTK_8852BE_SZ-TSD_W11_64_V6001151240_20220908B.zip?model=PRIME%20B650M-A%20WIFI',
            'file_type': 'zip',
            'rename_as': None
        },
        {
            'path': 'Realtek RTL8852CE\\Bluetooth',
            'url': functools.partial(
                url.gigabyte,
                url='https://www.gigabyte.com/Motherboard/B860M-AORUS-ELITE-WIFI6E/support#support-dl-driver-wlanbt',
                dri_name='8852 Bluetooth'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_675_realtek8852'
        },
        {
            'path': 'Realtek RTL8852CE\\WIFI',
            'url': functools.partial(
                url.gigabyte,
                url='https://www.gigabyte.com/Motherboard/B860M-AORUS-ELITE-WIFI6E/support#support-dl-driver-wlanbt',
                dri_name='8852 WIFI'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_674_realtek8852wifi'
        },
        {
            'path': 'Realtek RTL8892AE\\Bluetooth',
            'url': functools.partial(
                url.gigabyte,
                url='https://www.gigabyte.com/Motherboard/X870-AORUS-ELITE-WIFI7/support#support-dl-driver-wlanbt',
                dri_name='Realtek Bluetooth'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_3702_realtek8922'
        },
        {
            'path': 'Realtek RTL8892AE\\WIFI',
            'url': functools.partial(
                url.gigabyte,
                url='https://www.gigabyte.com/Motherboard/X870-AORUS-ELITE-WIFI7/support#support-dl-driver-wlanbt',
                dri_name='Realtek WIFI'
            ),
            'file_type': 'zip/exe',
            'rename_as': 'mb_driver_3701_realtek8922wifi'
        }
    ],
    'network': [
        {
            'path': 'Intel® Ethernet Adapter Complete Driver Pack',
            'url': functools.partial(
                url.intel,
                url='https://www.intel.com/content/www/us/en/download/15084/intel-ethernet-adapter-complete-driver-pack.html'
            ),
            'file_type': 'zip',
            'rename_as': None
        },
        {
            'path': 'Realtek',
            'url': functools.partial(
                url.msi,
                url='https://hk.msi.com/Motherboard/MAG-X870-TOMAHAWK-WIFI/support#driver',
                dri_type='LAN Drivers',
                dri_name='Realtek PCI-E Ethernet Drivers'
            ),
            'file_type': 'zip/folder',
            'rename_as': None
        }
    ],
    'tool': [
        {
            'path': 'CrystalDiskinfo',
            'url': url.crystaldick_info,
            'file_type': 'zip/exe',
            'rename_as': None

        },
        {
            'path': 'CrystalDiskMark',
            'url': url.crystaldick_mark,
            'file_type': 'zip/exe',
            'rename_as': None
        },
        {
            'path': 'FurMark',
            'url': url.furmark,
            'file_type': 'zip/folder',
            'rename_as': None
        },
        {
            'path': 'HWInfo',
            'url': url.hwinfo,
            'file_type': 'zip/exe',
            'rename_as': None
        },
        {
            'path': 'OCCT',
            'url': url.occt,
            'file_type': 'exe',
            'rename_as': None
        },
        {
            'path': 'y-cruncher',
            'url': url.y_cruncher,
            'file_type': 'zip/folder',
            'rename_as': None
        }
    ]
}
