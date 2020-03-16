from os import makedirs
from os.path import join, dirname

docs_dir = join(dirname(__file__), '..', 'docs')
cache_dir = join(dirname(__file__), '..', 'cache')

makedirs(docs_dir, exist_ok=True)
makedirs(cache_dir, exist_ok=True)

data_dir = '/hdd/evan/Data/tuh_eeg_epilepsy'
