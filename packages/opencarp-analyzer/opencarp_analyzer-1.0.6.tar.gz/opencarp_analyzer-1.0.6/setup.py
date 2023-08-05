import setuptools
import json
import os

with open("README.md","r") as f:
    long_description = f.read()

with open(os.path.join(os.path.dirname(__file__),"opencarp_analyzer","version.json"),"r") as f:
    version = json.loads(f.read())

setuptools.setup(
    name='opencarp_analyzer',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version= version["version"],
    packages=setuptools.find_packages() ,
    data_files = [("opencarp_analyzer", ["opencarp_analyzer/version.json"])],
    include_package_data=True,
    url='https://github.com/regmibijay/opencarp-analyzer',
    license='MIT',
    author='Bijay Regmi',
    author_email='opencarp-analyzer@regdelivery.de',
    description='OpenCARP Trace Analyzer',
    install_requires = ['pandas','matplotlib'],
    entry_points = {'console_scripts': [
    'opencarp-analyzer=opencarp_analyzer.analyzer:main',
    'opencarp-plotter=opencarp_analyzer.plotter:main',
    ]},
    python_requires = '>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)