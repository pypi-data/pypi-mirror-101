from setuptools import setup, find_packages
import re
version = re.findall('version\s*=\s*"(\S+)"\s*',
    open('./openitcr/settings.toml.example','r').read(), re.S)[0]

setup(
    name='openitcr',
    version = version,
    description='Open Information Technology Classroom',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown; charset=UTF-8",
    url='https://github.com/larryw3i/openitcr',
    download_url='https://github.com/larryw3i/openitcr',
    project_urls={
        'Code': 'https://github.com/larryw3i/openitcr',
        'Issue tracker': 'https://github.com/larryw3i/openitcr/issues',
        'Documentation': 'https://github.com/larryw3i/openitcr/docs/docs.md',
    },
    author='larryw3i',
    author_email='larryw3i@163.com',
    license='GPL-3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Babel==2.9.0',
        'pytz==2021.1',
        'toml==0.10.2',
    ],
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.7',
    scripts=['openitcr/bin/openitcr'],
)
