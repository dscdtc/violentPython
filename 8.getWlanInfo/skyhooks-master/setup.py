"""Installer for skyhooks
"""

import os
cwd = os.path.dirname(__file__)
__version__ = open(os.path.join(cwd, 'skyhooks', 'version.txt'),
                    'r').read().strip()

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

setup(
    name='skyhooks',
    description='Webhook handling utilities for asynchronous python apps ',
    long_description=open(os.path.join(cwd, 'README.rst')).readlines(),
    version=__version__,
    author='Wes Mason',
    author_email='wes@serverdensity.com',
    url='https://github.com/serverdensity/skyhooks',
    packages=find_packages('.', exclude=['ez_setup']),
    install_requires=open(os.path.join(cwd, 'requirements.txt')).readlines(),
    extra_requires={
        'gevent': open(os.path.join(cwd, 'gevent_requirements.txt')
                                        ).readlines(),
        'tornado': open(os.path.join(cwd, 'tornado_requirements.txt')
                                        ).readlines(),
        'twisted': open(os.path.join(cwd, 'twisted_requirements.txt')
                                        ).readlines(),
    },
    package_data={'skyhooks': ['version.txt']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'skyhooks-cleanup = skyhooks.tasks:cleanup_main'
        ],
    }
)
