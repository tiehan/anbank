import os
base_dir = os.path.dirname(os.path.realpath(__file__))[:-7]

__version__ = 'anbank-res version: 0.0.1'

config ={
    'log_dir': os.path.join(base_dir,'log')
}