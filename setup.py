import re

from setuptools import setup

with open('sutoppu.py', 'r') as f:
    regex_version = r"^__version__\s*=\s*['\"]([\d\.]*)['\"]"
    version = re.search(regex_version, f.read(), re.MULTILINE).group(1)

with open('README.md', 'rb') as file:
    readme = file.read().decode('utf-8')

setup(
    name='sutoppu',
    version=version,
    description="A simple python implementation of Specification pattern.",
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/u8slvn/sutoppu',
    author='u8slvn',
    author_email='u8slvn@gmail.com',
    license='MIT',
    download_url=f"https://github.com/u8slvn/sutoppu/archive/{version}.tar.gz",
    py_modules=['sutoppu'],
    platforms='all',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'specification',
        'specification-pattern'
        'DDD',
        'domain-driven-design'
        'business-rules',
        'verification',
    ],
    include_package_data=True,
    extras_require={
        'dev': [
            'pytest>=5.0.1',
            'pytest-cov>=2.7.1',
            'pytest-mock>=1.10.4',
            'coverage>=4.5.3',
            'flake8>=3.7.7',
            'bandit>=1.6.2',
        ]
    },
    python_requires='>=3.6',
)
