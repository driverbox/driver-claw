import time
from typing import Literal

from selenium import webdriver
from selenium.webdriver.common.by import By


def intel(remote: webdriver.Remote, url: str) -> str:
    remote.get(url)
    return (remote
            .find_element(By.CSS_SELECTOR, "button.dc-page-available-downloads-hero-button__cta")
            .get_attribute("data-href"))


def amd(remote: webdriver.Remote, url: str, keyword: str) -> str:
    remote.get(url)
    return (remote
            .find_element(By.XPATH, f"//a[contains(@href, '.exe') and contains(@href, '{keyword}')]")
            .get_attribute("href"))


def gigabyte(remote: webdriver.Remote, url: str, dri_name: str) -> str:
    remote.get(url)
    time.sleep(2)

    return remote\
        .find_element(By.XPATH, f"//div[contains(@class, 'table-body-Driver')][.//text()[contains(., '{dri_name}')]]//a")\
        .get_attribute("href")


def gigabyte_wifi_card(remote: webdriver.Remote, version: str, dri_name: str) -> str:
    if ("https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support" in remote.current_url):
        remote.refresh()
    else:
        remote.get(
            "https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-childModelsMenu")

    time.sleep(3)

    for anchor in remote.find_elements(By.XPATH, f"//a[.//p[text()='{version}']]"):
        if anchor.is_displayed():
            anchor.click()
            break
    else:
        raise ValueError("No visible element found")

    time.sleep(2)

    # going to the same URL, browser will not refresh
    return gigabyte(remote, "https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-dl", dri_name)


def msi(remote: webdriver.Remote, url: str, dri_type: str, dri_name: str) -> str:
    remote.get(url)

    try:
        # close cookie consent overlay
        remote.find_element(value="ccc-notify-dismiss").click()
    except:
        pass

    remote.find_element(
        By.XPATH, f"//div[@class='badges']//button[text()='{dri_type}']").click()

    time.sleep(1)

    return remote\
        .find_element(By.XPATH, f"//div[@class='card card--web'][.//text()[contains(., '{dri_name}')]]//a")\
        .get_attribute("href")


def _gigabyte_driver(remote: webdriver.Remote, name: str) -> str:
    time.sleep(2)

    return remote\
        .find_element(By.XPATH, f"//div[contains(@class, 'table-body-Driver')][.//text()[contains(., '{name}')]]//a")\
        .get_attribute("href")


def crystaldick_info(remote: webdriver.Remote) -> str:
    remote.get("https://sourceforge.net/projects/crystaldiskinfo/files/")

    version = remote.find_element(
        By.XPATH, "//a[contains(., 'Download Latest Version')]").get_attribute("title").split(":")[0]

    return f"https://download.sourceforge.net/crystaldiskinfo/{version}"


def crystaldick_mark(remote: webdriver.Remote) -> str:
    remote.get("https://sourceforge.net/projects/crystalmarkretro/files/")

    version = remote.find_element(
        By.XPATH, "//a[contains(., 'Download Latest Version')]").get_attribute("title").split(":")[0]

    return f"https://download.sourceforge.net/crystalmarkretro/{version}"


def furmark(remote: webdriver.Remote) -> str:
    remote.get("https://www.geeks3d.com/furmark/downloads/")

    remote.get(
        remote
        .find_element(By.XPATH, "//a[contains(., 'win64 - (ZIP)')]")
        .get_attribute("href")
    )

    time.sleep(5)

    return remote.find_element(
        By.XPATH, "//a[contains(., 'Geeks3D server')]").get_attribute("href")


def hwinfo(remote: webdriver.Remote) -> str:
    remote.get("https://www.hwinfo.com/download/")
    return (remote
            .find_element(By.XPATH,
                          "//div[contains(@class, 'download') and contains(., 'Portable') and contains(., 'Windows')]"
                          "//li[contains(., 'SAC ftp (SK)')]//a")
            .get_attribute("href"))


# def mediatek_7902_bluetooth(remote: webdriver.Remote) -> str:
#     remote.get(
#         "https://www.gigabyte.com/hk/Motherboard/B850M-FORCE-WIFI6E/support#dl")

#     return DriverFile(
#         url=_gigabyte_driver(remote, "MediaTek Wi-Fi 6E Bluetooth Driver"),
#         file_type="zip/exe",
#         rename_as="mb_driver_4717_mtk6e"
#     )


# def mediatek_7902_wifi(remote: webdriver.Remote) -> str:
#     remote.get(
#         "https://www.gigabyte.com/hk/Motherboard/B850M-FORCE-WIFI6E/support#dl")

#     return DriverFile(
#         url=_gigabyte_driver(remote, "MediaTek Wi-Fi 6E WIFI Driver"),
#         file_type="zip/exe",
#         rename_as="mb_driver_4716_mtk6ewifi"
#     )


# def mediatek_7922_bluetooth(remote: webdriver.Remote) -> str:
#     """RZ6xx (MT7921/MT79x2)"""
#     return DriverFile(
#         url="https://dlcdnets.asus.com/pub/ASUS/mb/Socket%20AM5/PRIME_X670E-PRO_WIFI/DRV_Bluetooth_MTK_SZ-TSD_W11_64_V110380440_20241225R.zip?model=TUF%20GAMING%20B650M-PLUS%20WIFI",
#         file_type="zip",
#         rename_as=None
#     )


# def mediatek_7922_wifi(remote: webdriver.Remote) -> str:
#     """RZ6xx (MT7921/MT79x2)"""
#     # remote.get(
#     #     "https://www.asus.com/motherboards-components/motherboards//tuf-gaming"
#     #     "/tuf-gaming-b650m-plus-wifi/helpdesk_download?model2Name=TUF-GAMING-B650M-PLUS-WIFI")

#     # box = remote.find_element(By.XPATH,
#     #                           "//section[.//div[text()='Wireless']]"
#     #                           "//div[contains(@class, 'productSupportDriverBIOSBox')][.//text()[contains(., 'MediaTek')]]")
#     return DriverFile(
#         url="https://dlcdnets.asus.com/pub/ASUS/mb/Socket%20AM5/PRIME_X670E-PRO_WIFI/DRV_WiFi_MediaTek_SZ-TSD_W11_64_V3401063_20241225R.zip?model=TUF%20GAMING%20B650M-PLUS%20WIFI",
#         file_type="zip",
#         rename_as=None
#     )


def nvidia_grd(remote: webdriver.Remote, type_: Literal["desktop", "laptop"]) -> str:
    # TODO: stuido driver
    # https://www.nvidia.com/zh-tw/studio/resources/

    remote.get("https://www.nvidia.com/zh-tw/geforce/game-ready-drivers/")

    remote.get(
        remote.find_element(
            By.XPATH, f"//a[@id='{'DsktpGrdDwnldBtn' if type_ == 'desktop' else 'NtbkGrdDwnldBtn'}']")
        .get_attribute("href")
    )

    return (remote
            .find_element(By.XPATH, "//a[contains(@id, 'agreeDownload')]")
            .get_attribute("href"))


def occt(remote: webdriver.Remote) -> str:
    return "https://www.ocbase.com/download/edition:Personal/os:Windows"


def y_cruncher(remote: webdriver.Remote) -> str:
    remote.get("https://www.numberworld.org/y-cruncher/#Download")

    return (remote
            .find_element(By.XPATH, "//table[contains(., 'Download Link')]//tr[contains(., 'Windows')]//a")
            .get_attribute("href"))
