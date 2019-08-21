"""Setup app from setup.cfg"""
from setuptools import find_packages, setup

__version__ = '0.0.1'


with open('requirements.txt', 'r') as fh:
    reqs = fh.read()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='tagsreport',
    version=__version__,
    packages=find_packages(),
    author='icaro',
    author_email='icarosoares01@gmail.com',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tagsreport=report.cli:report_tag'
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=reqs,
    description='Tags report client',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    python_requires='>=3',
)