#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:         core.py
# Purpose:      command core
# Created:      2019-01-21
# LastModify    2019-01-21
# Copyright:    Dormouse.Young
# Licence:      GPL V3.0
# ---------------------------------------------------------------------------
import logging
import os
import sys
import subprocess
from pathlib import Path


logging.basicConfig(
    format='%(asctime)s %(module)s %(funcName)s %(levelname)s %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def cmd_view(path):
    """
    view file
    :param path: the path of file
    :return: None
    """
    view_cmds = dict(
        txt='gvim',
        py='gvim',
    )
    logger.debug(path)
    view_path = Path(path)
    suffix = view_path.suffix[1:]
    if suffix:
        view_cmd = view_cmds.get(suffix)
        if view_cmd:
            subprocess.run([view_cmd, view_path])
    return


def cmd_edit(path):
    """
    edit file
    :param path: the path of file
    :return: None
    """
    view_cmds = dict(
        txt='gvim',
        py='gvim',
    )
    logger.debug(path)
    edit_path = Path(path)
    suffix = edit_path.suffix[1:]
    if suffix:
        view_cmd = view_cmds.get(suffix)
        if view_cmd:
            subprocess.run([view_cmd, edit_path])

def copy(source, target):
    s_path = Path(source)
    t_path = Path(target)
