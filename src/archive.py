"""Handling archive operations.
"""

import os
import subprocess

import patoolib

try:
    LIB7ZIP = (os.getenv('PATH_LIB_7ZIP')
               or patoolib.find_archive_program("7z", "unzip"))

    if not os.path.exists(LIB7ZIP):
        raise FileNotFoundError
except (patoolib.util.PatoolError, FileNotFoundError):
    LIB7ZIP = None


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
    cmd = ([LIB7ZIP, 'x', str(source), f'-o{target}']
           if LIB7ZIP
           else ['powershell', 'Expand-Archive', '-Path', str(source), '-DestinationPath', f'"{target}"'])
    return subprocess.run(cmd, stdout=stream, stderr=stream).returncode


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
    cmd = ([LIB7ZIP, 'a', str(target), " ".join(source), f'-mx{level}']
           if LIB7ZIP
           else ['powershell', 'Compress-Archive', '-Path', ','.join(source),
                 '-DestinationPath', str(target), '-CompressionLevel',
                 'NoCompression' if level == 0 else 'Fastest' if level < 5 else 'Optimal',
                 '-Force']
           )
    return subprocess.run(cmd, stdout=stream, stderr=stream).returncode
