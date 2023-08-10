import os
import random
from dataclasses import dataclass
from typing import Optional, List, Tuple

from PySide6.QtCore import QRect
from PySide6.QtGui import QColor


@dataclass
class FileInfo:
    full_filename: str
    size: int
    md5: Optional[str]
    rects: List[QRect]
    filled_rects: List[Tuple[QRect, QColor]]
    processing_progress: float


def get_file_infos(dir_name: str) -> List[FileInfo]:
    file_infos = list()

    if not os.path.isdir(dir_name):
        return file_infos

    for file in os.listdir(dir_name):
        # TODO remove
        # if file.endswith('.sqlite'):
        #     continue

        full_filename = os.path.join(dir_name, file)
        if not os.path.isfile(full_filename):
            continue

        file_infos.append(FileInfo(full_filename, os.stat(full_filename).st_size, None, list(), list(), 0))

    return file_infos
