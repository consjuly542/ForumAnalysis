#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os.path as path
import json
from source.Module import Module
from source.links_searcher import *


class LinkSearcherModule(Module):
    def run(self, file_origin, file_target):
        data = None
        with open(path.join(self.dir_origin, file_origin), 'r') as f_in:
            data = f_in.read()
        links = LinksSearcher(data).get_simple_links()
        res_file = path.join(self.dir_target, file_target)
        with open(res_file, 'w') as f_out:
            json.dump([link.__dict__ for link in links], f_out)
        return res_file
