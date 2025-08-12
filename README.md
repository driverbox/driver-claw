# driver-claw
<a id="readme-top"></a>


<!-- PROJECT SHIELDS -->
<div align="center">

  [![Tag][tag-shield]][tag-url]
  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![License][license-shield]][license-url]
  
</div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">driver-claw</h3>

  <p align="center">
    A common-line tool that automates the process of find and download the latest common hardware drivers, and diagnostic tool.
    <br />
    <a href="https://github.com/markmybytes/driver-claw/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/markmybytes/driver-claw/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

driver-claw is a Python-based command-line utility for downloading the latest PC hardware drivers and diagnostic tools. Leveraging Selenium, it automatically navigates official websites and motherboard manufacturers' pages to locate and retrieve the most up-to-date versions of essential drivers and utilities.

This tool is also an accompanying tool for [driver-box](https://github.com/markmybytes/driver-box/), see [Usage](#usage) section for more.
This tool also serves as a companion to [driver-box](https://github.com/markmybytes/driver-box/). Refer to the [Usage](#usage) section for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
[<img src="https://img.shields.io/badge/python-306998?style=for-the-badge&logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/selenium-01a71c?style=for-the-badge&logo=selenium&logoColor=white">](https://www.selenium.dev/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) >= 3.12
- [7zip](https://www.7-zip.org/download.html)

### Setup

#### Install dependencies
```sh
pip install -r requirements.txt
```

### Commands

- Run the script
  ```sh
  python src/main.py
  ```

- Display help message
  ```sh
  python src/main.py -h
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

###  Specify 7-Zip Executable Location

This tool uses 7-Zip to archive and extract files. If the 7-Zip executable is not available in the system's PATH, you can specify its location using the `PATH_LIB_7ZIP` environment variable.

```sh
# CMD
set "PATH_LIB_7ZIP=C:/<path-to-7zip>" && python src/main.py

# Powershell
$env:PATH_LIB_7ZIP="C:/<path-to-7zip>"; python src/main.py
```

###  Including Extra Files in the Archive

Use `-i` or `--include-files` to specify the file or directory paths you want to include in the output archive.
To include multiple paths, either separate them with spaces or provide the option multiple times.

```sh
python src/main.py -i foo/ bar/ -i README.md
```

The `conf/` directory contains configuration files for the default set of drivers and tools used by driver-box.
To use this tool to download drivers and utilities for driver-box, include the directory as input:

```sh
python src/main.py -i conf/
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[tag-url]: https://github.com/markmybytes/driver-claw/releases
[tag-shield]: https://img.shields.io/github/v/tag/markmybytes/driver-claw?style=for-the-badge&label=LATEST&color=%23B1B1B1
[contributors-shield]: https://img.shields.io/github/contributors/markmybytes/driver-claw.svg?style=for-the-badge
[contributors-url]: https://github.com/markmybytes/driver-claw/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/markmybytes/driver-claw.svg?style=for-the-badge
[forks-url]: https://github.com/markmybytes/driver-claw/network/members
[stars-shield]: https://img.shields.io/github/stars/markmybytes/driver-claw.svg?style=for-the-badge
[stars-url]: https://github.com/markmybytes/driver-claw/stargazers
[issues-shield]: https://img.shields.io/github/issues/markmybytes/driver-claw.svg?style=for-the-badge
[issues-url]: https://github.com/markmybytes/driver-claw/issues
[license-shield]: https://img.shields.io/github/license/markmybytes/driver-claw.svg?style=for-the-badge
[license-url]: https://github.com/markmybytes/driver-claw/blob/master/LICENSE.txt
