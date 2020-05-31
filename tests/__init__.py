''' bobbit.tests '''

import os

def load_tests(loader, standard_tests, pattern):
    this_dir      = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern='test_*.py')
    standard_tests.addTests(package_tests)
    return standard_tests

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
