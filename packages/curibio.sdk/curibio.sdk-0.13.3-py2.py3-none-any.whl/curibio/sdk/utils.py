# -*- coding: utf-8 -*-
"""General utility/helpers."""
import logging
import os
from typing import List

from .plate_recording import PlateRecording

logger = logging.getLogger(__name__)


def create_xlsx_for_all_recordings(root_directory: str = ".") -> None:
    """Traverses subdirectories to analyze multiple recordings.

    Assumes that any folder with an H5 file in it has only H5 files from a single recording.

    For simple usage, navigate to the root folder you want to analyze, and run:
    ``python3 -c "from curibio.sdk import check_if_latest_version, create_xlsx_for_all_recordings; check_if_latest_version(); create_xlsx_for_all_recordings()"``

    Args:
        root_directory: where to start the search. Output excel files will all be created in this folder
    """
    list_of_dirs: List[str] = list()
    for root, _, files in os.walk(root_directory):
        if any(file_name.endswith(".h5") for file_name in files):
            list_of_dirs.append(root)
    list_of_dirs = sorted(list_of_dirs)  # ensure deterministic ordering for test suite
    total_recording_count = len(list_of_dirs)
    log_text = f"Analysis of the directory {os.path.abspath(root_directory)} completed. {total_recording_count} total recording directories located."
    logger.info(log_text)
    for idx, iter_dir in enumerate(list_of_dirs):
        log_text = f"Analyzing recording {idx+1} of {total_recording_count}: {os.path.abspath(iter_dir)}"
        logger.info(log_text)
        iter_recording = PlateRecording.from_directory(iter_dir)
        iter_recording.write_xlsx(root_directory)
        for (
            iter_h5_file
        ) in (
            iter_recording._files  # pylint:disable=protected-access # TODO (Eli 3/19/21): There were odd errors in Windows CI about files not being closed in the temp directory and so they couldn't be deleted, so temporarily putting in this patch
        ):
            iter_h5_file._h5_file.close()  # pylint:disable=protected-access # TODO (Eli 3/19/21): There were odd errors in Windows CI about files not being closed in the temp directory and so they couldn't be deleted, so temporarily putting in this patch
        del iter_recording  # Eli (3/19/21): Resolve windows error with closing file when it is still open
