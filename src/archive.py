import os

import patoolib

LIB7ZIP = patoolib.find_archive_program("7z", "unzip")


def unzip(source: os.PathLike, target: os.PathLike, silent: bool = True) -> int:
    return os.system(f"{LIB7ZIP[:2]}\"{LIB7ZIP[2:]}\" x \"{source}\" -o\"{target}\""
                     f"{"> nul" if silent else ""}")


def zip(target: os.PathLike, *source: os.PathLike, level: int = 5, silent: bool = True) -> int:
    return os.system(f"{LIB7ZIP[:2]}\"{LIB7ZIP[2:]}\" a \"{target}\" {" ".join(source)} "
                     f"-mx{level} {"> nul" if silent else ""}")
