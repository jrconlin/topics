import io
import os

from setuptools import find_packages, setup

__version__ = "0.1.0"


def read_from(file):
    reply = []
    with io.open(os.path.join(here, file), encoding='utf8') as f:
        for l in f:
            l = l.strip()
            if not l:
                break
            if l[0] != '#' or l[:2] != '//':
                reply.append(l)
    return reply


here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf8') as f:
        README = f.read()
    with io.open(os.path.join(here, 'CHANGELOG.md'), encoding='utf8') as f:
        CHANGES = f.read()
except:
    README = "TBD"
    CHANGES = "TBD"

setup(name="topics",
      version=__version__,
      packages=find_packages(),
      description='WebPush Topics demo',
      long_description=README + '\n\n' + CHANGES,
      classifiers=["Topic :: Internet :: WWW/HTTP",
                   "Programming Language :: Python :: Implementation :: PyPy",
                   'Programming Language :: Python',
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7"
                   ],
      keywords='push webpush topics',
      author="jr conlin",
      author_email="src+webpusher@jrconlin.com",
      url='',
      license="MPL2",
      test_suite="nose.collector",
      include_package_data=True,
      zip_safe=False,
      install_requires=read_from('requirements.txt'),
      tests_require=read_from('test-requirements.txt'),
      entry_points="""
      [console_secripts]
      server=push_server.main:main
      pusher=pusher.main:main
      """,
      )
