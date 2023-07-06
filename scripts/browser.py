from __future__ import annotations

import os
import sys
import webbrowser

path = os.path.abspath(sys.argv[1])
print('Opening with browser:', path)
webbrowser.open(path)
