import time
from typing import Literal, NamedTuple

from selenium import webdriver
from selenium.webdriver.common.by import By


class DriverFile(NamedTuple):
    """A named tuple representing a driver file(s) URL and its properties.

    Attributes:
        url (str): The download URL for the driver
        file_type (Literal["exe", "zip", "zip/folder", "zip/exe"]): The type of file to be downloaded
            "exe": Executable file
            "zip": Zip archive
            "zip/folder": Zip archive containing a folder
            "zip/exe": Zip archive containing an executable
        rename_as (str | None): Optional new filename to rename the downloaded file to.
            If None, keeps original filename.
    """

    url: str
    file_type: Literal["exe", "zip", "zip/folder", "zip/exe"]
    rename_as: str | None


def _gigabyte_driver(remote: webdriver.Remote, name: str) -> str:
    time.sleep(2)

    return remote\
        .find_element(By.XPATH, f"//div[contains(@class, 'table-body-Driver')][.//text()[contains(., '{name}')]]//a")\
        .get_attribute("href")


def _intel_driver(remote: webdriver.Remote) -> str:
    return remote\
        .find_element(By.CSS_SELECTOR, "button.dc-page-available-downloads-hero-button__cta")\
        .get_attribute("data-href")


def _msi_driver(remote: webdriver.Remote, button: str, name: str) -> str:
    try:
        # close cookie consent overlay
        remote.find_element(value="ccc-notify-dismiss").click()
    except:
        pass

    remote.find_element(
        By.XPATH, f"//div[@class='badges']//button[text()='{button}']").click()

    time.sleep(1)

    return remote\
        .find_element(By.XPATH, f"//div[@class='card card--web'][.//text()[contains(., '{name}')]]//a")\
        .get_attribute("href")


def amd_display(remote: webdriver.Remote) -> DriverFile:
    remote.get("https://www.amd.com/en/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-9000-series/amd-radeon-rx-9070-xt.html")

    return DriverFile(
        url=(remote
             .find_element(By.XPATH, "//a[@alt='Download' and contains(@href, 'win10-win11')]")
             .get_attribute("href")),
        file_type="zip",
        rename_as=None
    )


def amd_chipset(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.amd.com/en/support/downloads/drivers.html/chipsets/am5/x870e.html")

    return DriverFile(
        url=(remote
             .find_element(By.XPATH, "//a[@alt='Download' and contains(@href, 'chipset')]")
             .get_attribute("href")),
        file_type="exe",
        rename_as="AMD_Chipset_Software"
    )


def nvidia_display_game(remote: webdriver.Remote) -> DriverFile:
    remote.get("https://www.nvidia.com/zh-tw/geforce/game-ready-drivers/")

    remote.get(
        remote.find_element(By.XPATH, "//a[@id='DsktpGrdDwnldBtn']").get_attribute("href"))

    return DriverFile(
        url=(remote
             .find_element(By.XPATH, "//a[contains(@id, 'agreeDownload')]")
             .get_attribute("href")),
        file_type="zip",
        rename_as=None
    )


def intel_lan(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.intel.com/content/www/us/en/download/15084/intel-ethernet-adapter-complete-driver-pack.html")

    return DriverFile(url=_intel_driver(remote), file_type="zip", rename_as=None)


def realtek_lan(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://hk.msi.com/Motherboard/MAG-X870-TOMAHAWK-WIFI/support#driver")

    return DriverFile(
        url=_msi_driver(
            remote, "LAN Drivers", "Realtek PCI-E Ethernet Drivers"),
        file_type="zip/folder",
        rename_as=None
    )


def realtek_audio(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://hk.msi.com/Motherboard/MAG-X870-TOMAHAWK-WIFI/support#driver")

    return DriverFile(
        url=_msi_driver(
            remote, "On-Board Audio Drivers", "Realtek HD Universal Driver"),
        file_type="zip/folder",
        rename_as=None
    )


def intel_wifi(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.intel.com.tw/content/www/us/en/download/19351/intel-wireless-wi-fi-drivers-for-windows-10-and-windows-11.html")

    return DriverFile(url=_intel_driver(remote), file_type="exe", rename_as="WiFi-Driver64-Win10-Win11")


def intel_bluetooth(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.intel.com.tw/content/www/us/en/download/18649/intel-wireless-bluetooth-drivers-for-windows-10-and-windows-11.html")

    return DriverFile(url=_intel_driver(remote), file_type="exe", rename_as="BT-UWD-Win10-Win11")


def intel_inf_utility(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.intel.com/content/www/us/en/download/19347/chipset-inf-utility.html")

    return DriverFile(url=_intel_driver(remote), file_type="exe", rename_as=None)


def intel_display_arc(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.intel.com/content/www/us/en/download/785597/intel-arc-iris-xe-graphics-windows.html")

    return DriverFile(url=_intel_driver(remote), file_type="zip", rename_as=None)


def intel_display_uhd(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.intel.com/content/www/us/en/download/776137/intel-7th-10th-gen-processor-graphics-windows.html")

    return DriverFile(url=_intel_driver(remote), file_type="zip", rename_as=None)


def intel_ppm(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.gigabyte.com/Motherboard/B860M-AORUS-ELITE-WIFI6E/support#support-dl-driver-wlanbt")

    return DriverFile(
        url=_gigabyte_driver(remote, "Platform Power Management(PPM)"),
        file_type="zip/exe",
        rename_as="mb_driver_3713_ppm"
    )


def qualcomm_ncm865_wifi(remote: webdriver.Remote) -> DriverFile:
    if ("https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support" in remote.current_url):
        remote.refresh()
    else:
        remote.get(
            "https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-childModelsMenu")

    time.sleep(1)

    for anchor in remote.find_elements(By.XPATH, "//a[.//p[text()='GC-WIFI7 1.0']]"):
        if anchor.is_displayed():
            anchor.click()
            break
    else:
        raise ValueError("No visible element found")

    time.sleep(2)

    return DriverFile(
        url=_gigabyte_driver(remote, "WIFI"),
        file_type="zip/exe",
        rename_as="mb_driver_2686_qualcomm"
    )


def qualcomm_ncm865_bluetooth(remote: webdriver.Remote) -> DriverFile:
    if ("https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support" in remote.current_url):
        remote.refresh()
    else:
        remote.get(
            "https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-childModelsMenu")

    time.sleep(1)

    for anchor in remote.find_elements(By.XPATH, "//a[.//p[text()='GC-WIFI7 1.0']]"):
        if anchor.is_displayed():
            anchor.click()
            break
    else:
        raise ValueError("No visible element found")

    time.sleep(2)

    return DriverFile(
        url=_gigabyte_driver(remote, "Bluetooth"),
        file_type="zip/exe",
        rename_as="mb_driver_2687_qualcomm"
    )


def mediatek_7927_wifi(remote: webdriver.Remote) -> DriverFile:
    """RZ7xx (MT7925/MT7927)"""

    if ("https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support" in remote.current_url):
        remote.refresh()
    else:
        remote.get(
            "https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-childModelsMenu")

    time.sleep(1)

    for anchor in remote.find_elements(By.XPATH, "//a[.//p[text()='GC-WIFI7 1.1']]"):
        if anchor.is_displayed():
            anchor.click()
            break
    else:
        raise ValueError("No visible element found")

    time.sleep(2)

    return DriverFile(
        url=_gigabyte_driver(remote, "WIFI"),
        file_type="zip/exe",
        rename_as="mb_driver_2682_mtk"
    )


def mediatek_7927_bluetooth(remote: webdriver.Remote) -> DriverFile:
    """RZ7xx (MT7925/MT7927)"""

    if ("https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support" in remote.current_url):
        remote.refresh()
    else:
        remote.get(
            "https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-childModelsMenu")

    time.sleep(1)

    for anchor in remote.find_elements(By.XPATH, "//a[.//p[text()='GC-WIFI7 1.1']]"):
        if anchor.is_displayed():
            anchor.click()
            break
    else:
        raise ValueError("No visible element found")

    time.sleep(2)

    return DriverFile(
        url=_gigabyte_driver(remote, "Bluetooth"),
        file_type="zip/exe",
        rename_as="mb_driver_2683_mtk")


def mediatek_7922_wifi(remote: webdriver.Remote) -> DriverFile:
    """RZ6xx (MT7921/MT79x2)"""
    # remote.get(
    #     "https://www.asus.com/motherboards-components/motherboards//tuf-gaming"
    #     "/tuf-gaming-b650m-plus-wifi/helpdesk_download?model2Name=TUF-GAMING-B650M-PLUS-WIFI")

    # box = remote.find_element(By.XPATH,
    #                           "//section[.//div[text()='Wireless']]"
    #                           "//div[contains(@class, 'productSupportDriverBIOSBox')][.//text()[contains(., 'MediaTek')]]")
    return DriverFile(
        url="https://dlcdnets.asus.com/pub/ASUS/mb/Socket%20AM5/PRIME_X670E-PRO_WIFI/DRV_WiFi_MediaTek_SZ-TSD_W11_64_V3401063_20241225R.zip?model=TUF%20GAMING%20B650M-PLUS%20WIFI",
        file_type="zip",
        rename_as=None
    )


def mediatek_7922_bluetooth(remote: webdriver.Remote) -> DriverFile:
    """RZ6xx (MT7921/MT79x2)"""
    return DriverFile(
        url="https://dlcdnets.asus.com/pub/ASUS/mb/Socket%20AM5/PRIME_X670E-PRO_WIFI/DRV_Bluetooth_MTK_SZ-TSD_W11_64_V110380440_20241225R.zip?model=TUF%20GAMING%20B650M-PLUS%20WIFI",
        file_type="zip",
        rename_as=None
    )


def mediatek_7902_wifi(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.gigabyte.com/hk/Motherboard/B850M-FORCE-WIFI6E/support#dl")

    return DriverFile(
        url=_gigabyte_driver(remote, "MediaTek Wi-Fi 6E WIFI Driver"),
        file_type="zip/exe",
        rename_as="mb_driver_4716_mtk6ewifi"
    )


def mediatek_7902_bluetooth(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.gigabyte.com/hk/Motherboard/B850M-FORCE-WIFI6E/support#dl")

    return DriverFile(
        url=_gigabyte_driver(remote, "MediaTek Wi-Fi 6E Bluetooth Driver"),
        file_type="zip/exe",
        rename_as="mb_driver_4717_mtk6e"
    )


def realtek_8852be_wifi(remote: webdriver.Remote) -> DriverFile:
    return DriverFile(
        url="https://dlcdnets.asus.com/pub/ASUS/mb/08WIRELESS/DRV_WiFi_RTK_8852BE_SZ-TSD_W11_64_V6001151240_20220908B.zip?model=PRIME%20B650M-A%20WIFI",
        file_type="zip",
        rename_as=None
    )


def realtek_8852be_bluetooth(remote: webdriver.Remote) -> DriverFile:
    return DriverFile(
        url="https://dlcdnets.asus.com/pub/ASUS/mb/02BT/DRV_BT_RTK_8852BE_SZ-TSD_W11_64_V1640132401503_20240924R.zip?model=PRIME%20B650M-A%20WIFI",
        file_type="zip",
        rename_as=None
    )


def realtek_8852ce_wifi(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.gigabyte.com/Motherboard/B860M-AORUS-ELITE-WIFI6E/support#support-dl-driver-wlanbt")

    return DriverFile(
        url=_gigabyte_driver(remote, "8852 WIFI"),
        file_type="zip/exe",
        rename_as="mb_driver_674_realtek8852wifi"
    )


def realtek_8852ce_bluetooth(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.gigabyte.com/Motherboard/B860M-AORUS-ELITE-WIFI6E/support#support-dl-driver-wlanbt")

    return DriverFile(
        url=_gigabyte_driver(remote, "8852 Bluetooth"),
        file_type="zip/exe",
        rename_as="mb_driver_675_realtek8852"
    )


def realtek_8892ae_wifi(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.gigabyte.com/Motherboard/X870-AORUS-ELITE-WIFI7/support#support-dl-driver-wlanbt")

    return DriverFile(
        url=_gigabyte_driver(remote, "Realtek WIFI"),
        file_type="zip/exe",
        rename_as="mb_driver_3701_realtek8922wifi"
    )


def realtek_8892ae_bluetooth(remote: webdriver.Remote) -> DriverFile:
    remote.get(
        "https://www.gigabyte.com/Motherboard/X870-AORUS-ELITE-WIFI7/support#support-dl-driver-wlanbt")

    return DriverFile(
        url=_gigabyte_driver(remote, "Realtek Bluetooth"),
        file_type="zip/exe",
        rename_as="mb_driver_3702_realtek8922"
    )


def y_cruncher(remote: webdriver.Remote) -> DriverFile:
    remote.get("https://www.numberworld.org/y-cruncher/#Download")

    return DriverFile(
        url=remote
        .find_element(By.XPATH, "//table[contains(., 'Download Link')]//tr[contains(., 'Windows')]//a")
        .get_attribute("href"),
        file_type="zip/folder",
        rename_as=None
    )


def hwinfo(remote: webdriver.Remote) -> DriverFile:
    remote.get("https://www.hwinfo.com/download/")

    return DriverFile(
        url=remote
        .find_element(By.XPATH,
                      "//div[contains(@class, 'download') and contains(., 'Portable') and contains(., 'Windows')]"
                      "//li[contains(., 'SAC ftp (SK)')]//a")
        .get_attribute("href"),
        file_type="zip/exe",
        rename_as=None
    )


def occt(remote: webdriver.Remote) -> DriverFile:
    return DriverFile(
        url="https://www.ocbase.com/download/edition:Personal/os:Windows",
        file_type="exe",
        rename_as=None
    )


def furmark(remote: webdriver.Remote) -> DriverFile:
    remote.get("https://www.geeks3d.com/furmark/downloads/")

    remote.get(
        remote
        .find_element(By.XPATH, "//a[contains(., 'win64 - (ZIP)')]")
        .get_attribute("href")
    )

    time.sleep(5)

    return DriverFile(
        url=remote.find_element(
            By.XPATH, "//a[contains(., 'Geeks3D server')]").get_attribute("href"),
        file_type="zip/folder",
        rename_as=None
    )


def crystaldick_mark(remote: webdriver.Remote) -> DriverFile:
    remote.get("https://sourceforge.net/projects/crystalmarkretro/files/")

    version = remote.find_element(
        By.XPATH, "//a[contains(., 'Download Latest Version')]").get_attribute("title").split(":")[0]

    return DriverFile(
        url=f"https://download.sourceforge.net/crystalmarkretro/{version}",
        file_type="zip/exe",
        rename_as=None
    )


def crystaldick_info(remote: webdriver.Remote) -> DriverFile:
    remote.get("https://sourceforge.net/projects/crystaldiskinfo/files/")

    version = remote.find_element(
        By.XPATH, "//a[contains(., 'Download Latest Version')]").get_attribute("title").split(":")[0]

    return DriverFile(
        url=f"https://download.sourceforge.net/crystaldiskinfo/{version}",
        file_type="exe",
        rename_as=None
    )
