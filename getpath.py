#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import time


class PathInfo:
    def __init__(self, path):
        self.path = path
        self.fields = [u'文件名', u'扩展名', u'大小', u'修改时间']
        self.time_format = "%Y-%m-%d %H:%M:%S"

    def get_fields(self):
        return self.fields

    def get_infos(self):
        files = os.listdir(self.path)
        infos = [self.get_file_info(filename) for filename in files]
        return infos

    def get_file_info(self, filename):
        name = os.path.join(self.path, filename)
        mod_time = os.path.getmtime(name)
        mod_time = time.strftime(self.time_format,
                                 time.localtime(mod_time))
        size = os.path.getsize(name)
        if os.path.isdir(name):
            ext_name = ''
        else:
            ext_name = os.path.splitext(filename)[1][1:]

        return [name, ext_name, size, mod_time]

if __name__ == "__main__":
    path = u'/home/dormouse/视频'
    print PathInfo(path).get_path_info()
