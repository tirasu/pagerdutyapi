"""
Python wrapper for PagerDuty API, focused on reporting alerts (incidents) to it

source: https://github.com/tirasu/pagerdutyapi
author: Tomasz Jaskowski (http://www.jaskowski.info/)
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import re

CURRENT_DIR = os.path.dirname(__file__)


def parse_requirements(path):
    """
    Get version-less packages and follow any redirections
    :param path: path of the requirements file
    :type path: str or unicode
    :return: list of version-less requirements
    :rtype: list of str
    """
    result = []
    with open(path) as f:
        for line in f.read().splitlines():
            item = line.split('#', 1)[0].strip()
            if not item:
                continue  # Item is empty
            if item.startswith('-r '):
                # Take part after "-r " and use it as relative path:
                result.extend(parse_requirements(
                    os.path.join(os.path.dirname(path), item[3:].strip()),
                ))
            else:
                version_less_item = re.split(r'[=<>]', item, 1)[0]
                result.append(version_less_item)
    return result


setup(
    author='Tomasz Jaskowski',
    author_email='tadeck@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',  # just began
        # 'Development Status :: 3 - Alpha',  # testing
        # 'Development Status :: 4 - Beta',  # testing, but looks good
        # 'Development Status :: 5 - Production/Stable',  # used on production
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
    ],
    description='PagerDuty support, mostly reporting alerts',
    download_url=(
        'https://github.com/tirasu/pagerdutyapi/archive/v0.1.0.tar.gz'
    ),
    #install_requires=parse_requirements('requirements.txt'),
    install_requires=[
        'six',
        'requests',
    ],
    license='MIT',
    #long_description=open(os.path.join(CURRENT_DIR, 'README.rst')).read(),
    name='pagerdutyapi',
    packages=['pagerdutyapi'],
    url='https://github.com/tirasu/pagerdutyapi/',
    version='0.1.1',
)
