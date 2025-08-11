import contextlib
import functools
import glob
import os
import pickle
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable, Literal, TypedDict
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver import Remote
from tqdm import tqdm

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


class ClawPrize(TypedDict):
    path: str
    url: str | Callable[[Remote], str]
    file_type: Literal["exe", "zip", "zip/folder", "zip/exe"]
    rename_as: str | None


class DriverClaw:

    @property
    def path_error_log(self) -> Path:
        return self.dest.joinpath('.failscrapes.pkl')

    def __init__(self, destination: str | Path):
        self.dest = Path(destination)

    def load_failed(self):
        with open(self.path_error_log, 'rb') as f:
            return pickle.load(f)

    def start(self, targets: dict[str, list[ClawPrize]], on_error: Literal['exit', 'log', 'ignore']):
        failed_downloads: dict[str, list] = {}

        with get_browser() as browser:
            scrape_items = [{**item, 'category': category}
                            for category, items in targets.items()
                            for item in items]

            for i, item in enumerate(scrape_items):
                category = item['category']
                fullpath = self.dest.joinpath(category, item['path'])
                fullpath.mkdir(parents=True, exist_ok=True)

                try:
                    print(f'Processing {i+1:>2}/{len(scrape_items)}: '
                          f'[{category}] {item['path']}')

                    print("├ Locating download URL...")
                    url = (item['url']
                           if type(item['url']) is str
                           else item['url'](browser))

                    print("├ Downloading...")
                    self.download_and_save(
                        url, item["file_type"], item["rename_as"], fullpath)
                except Exception as e:
                    print(f'┴ Failed: {e}')

                    if on_error == 'exit':
                        sys.exit(1)
                    if on_error == 'log':
                        failed_downloads.setdefault(category, [])
                        failed_downloads[category].append(item)
                    continue

                print('┴ Completed.')

        if on_error == 'log' and len(failed_downloads) > 0:
            self._dump_failed(failed_downloads)

        if len(failed_downloads) == 0:
            self.path_error_log.unlink(True)

        return failed_downloads

    def download_and_save(self, url: str, file_type: Literal["exe", "zip", "zip/exe", "zip/folder"], rename_as: str | None,  path: str | Path) -> None:
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

            resp.raw.read = functools.partial(
                resp.raw.read, decode_content=True)

            with tempfile.TemporaryFile(delete_on_close=False) as temp:
                with tqdm.wrapattr(resp.raw, "read", total=int(resp.headers.get('Content-Length', 0))) as content:
                    shutil.copyfileobj(content, temp)
                temp.close()

                print("├ Organising...")
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

    def _dump_failed(self, failed: dict[str, list[ClawPrize]]):
        with open(self.path_error_log, 'wb') as f:
            return pickle.dump(failed, f)
