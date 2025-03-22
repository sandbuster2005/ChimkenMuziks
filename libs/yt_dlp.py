#!/usr/bin/python
# -*- coding: utf-8 -*-
from yt_dlp import main
import re
import sys
if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(main())
