from list_directory import *
import os

def test_default_scenario():
    assert list_directory.short_format(os.path.listdir(./sample/),./sample)=['one','file.txt']
