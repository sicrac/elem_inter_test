from fabric import colors
from fabric import api

ENVIRONMENTS = ('dev', 'tst', 'acc', 'prd')


def select_settings(env):
    if env not in ENVIRONMENTS:
        print colors.red('Unknown env: %s' % env)
        print colors.red('Layer must be one of: %s' % ', '.join(ENVIRONMENTS))
        return
    else:
        api.local("echo 'from %s import *' > elem_inter_test/settings/__init__.py" % env)
