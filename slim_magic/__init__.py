"""pyslim magic"""
__version__ = '0.0.1'

from .slim_magic import SlimMagic

def load_ipython_extension(ipython):
    ipython.register_magics(SlimMagic)