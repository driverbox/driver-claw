import contextlib
import functools
import glob
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import requests
from selenium import webdriver
from tqdm.auto import tqdm

import archive


@contextlib.contextmanager
def get_browser():
    options = webdriver.FirefoxOptions()
    options.set_preference('intl.accept_languages', 'zh-Hant')
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    try:
        yield driver
    finally:
        driver.quit()


def download_and_save(url: str, file_type: Literal["exe", "zip", "zip/exe", "zip/folder"], rename_as: str | None,  path: os.PathLike,) -> None:
    path = Path(path)

    # AMD drivers require a referer header to be set
    if ("sourceforge" in url or "geeks3d" in url):
        headers = {}
    else:
        headers = {
            "referer": urlparse(url).hostname,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0"
        }

    with requests.get(url, stream=True, headers=headers, allow_redirects=True) as resp:
        resp.raise_for_status()
        if "html" in resp.headers['content-type']:
            raise ValueError("The URL responsed a HTML page.")

        resp.raw.read = functools.partial(resp.raw.read, decode_content=True)

        with (tqdm.wrapattr(resp.raw, "read", total=int(resp.headers.get('Content-Length', 0))) as content,
              tempfile.TemporaryFile(delete_on_close=False) as temp):
            shutil.copyfileobj(content, temp)

            temp.close()

            if "zip" in file_type:
                if (archive.unzip(temp.name, path) != 0):
                    raise RuntimeError("Failed to extract the zip file.")

                if file_type == "zip/folder":
                    for directory in os.listdir(path):
                        for file in glob.glob("*", root_dir=path.joinpath(directory)):
                            shutil.move(
                                path.joinpath(directory, file), path)
                    shutil.rmtree(path.joinpath(directory))

                if rename_as:
                    if len(exe := glob.glob(str(path.joinpath("*.exe")))) > 1:
                        raise NotImplementedError(
                            "More than 1 executable found.")

                    shutil.move(
                        exe[0], Path(*exe[0].split("\\")[:-1]).joinpath(f"{rename_as}.exe"))
            else:
                if "Content-Disposition" in resp.headers.keys():
                    fname = re.findall(
                        "filename=(.+)", resp.headers["Content-Disposition"])[0]
                else:
                    fname = urlparse(url).path.split("/")[-1]

                if rename_as:
                    fname = f"{rename_as}.{fname.split(".")[-1]}"

                shutil.move(temp.name, path.joinpath(fname.strip("\"")))
