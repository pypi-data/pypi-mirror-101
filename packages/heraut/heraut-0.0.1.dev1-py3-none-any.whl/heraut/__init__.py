from os import environ
import os
import pathlib
if 'HERAUT_DEFAULT' not in environ:
    # Ideally run this block once per user
    environ['HERAUT_DEFAULT'] = '.heraut_default'
    dirkey = str(pathlib.Path.home()) + '/' + environ['HERAUT_DEFAULT']
    if not os.path.isdir(dirkey):
        os.makedirs(dirkey)

from .listener import Listener
from .sender import Sender

