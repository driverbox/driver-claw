"""
URL resolution module for driver and utility downloads.

This module provides functions that use Selenium WebDriver to automate
browser interactions and extract direct download URLs for various hardware
drivers and system utilities from vendor websites.

Each function targets a specific vendor or tool, navigating their support
pages and locating the appropriate download link using XPath or CSS selectors.
"""


import time
from typing import Literal

from selenium import webdriver
from selenium.webdriver.common.by import By


def amd(remote: webdriver.Remote, url: str, dri_name: str) -> str:
    """Fetch AMD driver download URL.

    Args:
        remote (webdriver.Remote): Selenium WebDriver instance.
        url (str): AMD download page URL.
        dri_name (str): Keyword in the download URL to filter the download link.

    Returns:
        str: Direct download URL for the driver.
    """
    remote.get(url)
    return (remote
            .find_element(By.XPATH, f'//a[contains(@href, ".exe") and contains(@href, "{dri_name}")]')
            .get_attribute('href'))


def intel(remote: webdriver.Remote, url: str) -> str:
    """Fetch Intel driver download URL.

    Args:
        remote (webdriver.Remote): Selenium WebDriver instance.
        url (str): Intel download page URL.

    Returns:
        str: Direct download URL for the driver.
    """
    remote.get(url)
    return (remote
            .find_element(By.CSS_SELECTOR, 'button.dc-page-available-downloads-hero-button__cta')
            .get_attribute('data-href'))


def gigabyte(remote: webdriver.Remote, url: str, dri_name: str) -> str:
    """
    Fetch Gigabyte driver download URL.

    Args:
        remote (webdriver.Remote): Selenium WebDriver instance.
        url (str): Gigabyte download page URL.
        dri_name (str): Driver name to locate.

    Returns:
        str: Direct download URL for the driver.
    """
    remote.get(url)
    time.sleep(2)

    return (remote
            .find_element(By.XPATH, f'//div[contains(@class, "table-body-Driver")][.//text()[contains(., "{dri_name}")]]//a')
            .get_attribute('href'))


def gigabyte_wifi_card(remote: webdriver.Remote, dri_type: str, dri_name: str) -> str:
    """Fetch Gigabyte GC-WIFI7 card driver download URL.

    Args:
        remote (webdriver.Remote): Selenium WebDriver instance.
        dri_type (str): Wi-Fi card version.
        dri_name (str): Driver name to locate.

    Returns:
        str: Direct download URL for the driver.

    Raises:
        ValueError: If no visible version element is found.
    """
    if ('https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support' in remote.current_url):
        remote.refresh()
    else:
        remote.get(
            'https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-childModelsMenu')

    time.sleep(3)

    for anchor in remote.find_elements(By.XPATH, f'//a[.//p[text()="{dri_type}"]]'):
        if anchor.is_displayed():
            anchor.click()
            break
    else:
        raise ValueError('No visible element found')

    time.sleep(2)

    # going to the same URL, browser will not refresh
    return gigabyte(remote, 'https://www.gigabyte.com/PC-Accessory/GC-WIFI7/support#support-dl', dri_name)


def msi(remote: webdriver.Remote, url: str, dri_type: str, dri_name: str) -> str:
    """Fetch MSI driver download URL.

    Args:
        remote (webdriver.Remote): Selenium WebDriver instance.
        url (str): MSI download page URL.
        dri_type (str): Driver type to filter.
        dri_name (str): Driver name to locate.

    Returns:
        str: Direct download URL for the driver.
    """
    remote.get(url)

    try:
        # close cookie consent overlay
        remote.find_element(value='ccc-notify-dismiss').click()
    except:
        pass

    remote.find_element(
        By.XPATH, f'//div[@class="badges"]//button[text()="{dri_type}"]').click()

    time.sleep(1)

    return remote\
        .find_element(By.XPATH, f'//div[@class="card card--web"][.//text()[contains(., "{dri_name}")]]//a')\
        .get_attribute('href')


def nvidia_grd(remote: webdriver.Remote, dri_type: Literal['desktop', 'laptop']) -> str:
    """Fetch NVIDIA Game Ready Driver download URL.

    Args:
        remote (webdriver.Remote): Selenium WebDriver instance.
        dri_type (Literal["desktop", "laptop"]): Device type for driver.

    Returns:
        str: Direct download URL for the driver.
    """
    # TODO: stuido driver
    # https://www.nvidia.com/zh-tw/studio/resources/

    remote.get('https://www.nvidia.com/zh-tw/geforce/game-ready-drivers/')

    remote.get(
        remote.find_element(
            By.XPATH, f'//a[@id="{'DsktpGrdDwnldBtn' if dri_type == 'desktop' else 'NtbkGrdDwnldBtn'}"]')
        .get_attribute('href')
    )

    return (remote
            .find_element(By.XPATH, '//a[contains(@id, "agreeDownload")]')
            .get_attribute('href'))


# ---------------------------------------------
#                   Tools
# ---------------------------------------------


def crystaldick_info(remote: webdriver.Remote) -> str:
    """Fetch CrystalDiskInfo download URL.
    """
    remote.get('https://sourceforge.net/projects/crystaldiskinfo/files/')

    version = remote.find_element(
        By.XPATH, '//a[contains(., "Download Latest Version")]').get_attribute('title').split(':')[0]

    return f'https://download.sourceforge.net/crystaldiskinfo/{version}'


def crystaldick_mark(remote: webdriver.Remote) -> str:
    """Fetch CrystalDiskMark download URL.
    """
    remote.get('https://sourceforge.net/projects/crystalmarkretro/files/')

    version = remote.find_element(
        By.XPATH, '//a[contains(., "Download Latest Version")]').get_attribute('title').split(':')[0]

    return f'https://download.sourceforge.net/crystalmarkretro/{version}'


def furmark(remote: webdriver.Remote) -> str:
    """Fetch FurMark download URL.
    """
    remote.get('https://www.geeks3d.com/furmark/downloads/')

    remote.get(
        remote
        .find_element(By.XPATH, '//a[contains(., "win64 - (ZIP)")]')
        .get_attribute('href')
    )

    time.sleep(5)

    return remote.find_element(
        By.XPATH, '//a[contains(., "Geeks3D server")]').get_attribute('href')


def hwinfo(remote: webdriver.Remote) -> str:
    """Fetch HWiNFO download URL.
    """
    remote.get('https://www.hwinfo.com/download/')
    return (remote
            .find_element(By.XPATH,
                          '//div[contains(@class, "download") and contains(., "Portable") and contains(., "Windows")]'
                          '//li[contains(., "SAC ftp (SK)")]//a')
            .get_attribute('href'))


def occt(remote: webdriver.Remote) -> str:
    """Fetch OCCT download URL.
    """
    return 'https://www.ocbase.com/download/edition:Personal/os:Windows'


def y_cruncher(remote: webdriver.Remote) -> str:
    """Fetch y-cruncher download URL.
    """
    remote.get('https://www.numberworld.org/y-cruncher/#Download')

    return (remote
            .find_element(By.XPATH, '//table[contains(., "Download Link")]//tr[contains(., "Windows")]//a')
            .get_attribute('href'))
