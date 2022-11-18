import ast
import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_debug.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='Joseph Nix',
    author_email='nixjdm@terminallabs.com',
    description=description,
    keywords='Lektor plugin',
    license='BSD-3-Clause',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-debug',
    packages=find_packages(),
    py_modules=['lektor_debug'],
    url='https://github.com/terminal-labs/lektor-debug',
    version='0.1.5',
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
    ],
    entry_points={
        'lektor.plugins': [
            'debug = lektor_debug:DebugPlugin',
        ]
    }
)
