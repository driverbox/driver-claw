"""Handling archive operations using 7z.
"""

import os
import subprocess

import patoolib

LIB7ZIP = (os.getenv('PATH_LIB_7ZIP')
           or patoolib.find_archive_program("7z", "unzip"))


def unzip(source: os.PathLike, target: os.PathLike, silent: bool = True) -> int:
    """Extract a zip archive to the specified target directory.

    Args:
        source (os.PathLike): Path to the zip file.
        target (os.PathLike): Directory to extract files to.
        silent (bool): Suppress console output if True. Defaults to True.

    Returns:
        int: Exit code of the extraction process (0 for success).
    """
    stream = subprocess.DEVNULL if silent else None
    return subprocess.run([LIB7ZIP, 'x', source, f'-o{target}'], stdout=stream, stderr=stream).returncode


def zip(target: os.PathLike, *source: os.PathLike, level: int = 5, silent: bool = True) -> int:
    """Create a zip archive from source files or directories.

    Args:
        target (os.PathLike): Path for the output zip file.
        *source (os.PathLike): Paths to files or directories to archive.
        level (int): Compression level (0-9). Defaults to 5.
        silent (bool): Suppress console output if True. Defaults to True.

    Returns:
        int: Exit code of the compression process (0 for success).
    """
    stream = subprocess.DEVNULL if silent else None
    return subprocess.run([LIB7ZIP, 'a', target, " ".join(source), f'-mx{level}'], stdout=stream, stderr=stream).returncode
