# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicomtrolley']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0',
 'pydicom>=2.1.2,<3.0.0',
 'requests-futures>=1.0.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dicomtrolley',
    'version': '0.4.0',
    'description': 'Retrieve medical images via DICOM-QR and DICOMweb',
    'long_description': '# dicomtrolley\n\n[![CI](https://github.com/sjoerdk/dicomtrolley/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/sjoerdk/dicomtrolley/actions/workflows/build.yml?query=branch%3Amaster)\n[![PyPI](https://img.shields.io/pypi/v/dicomtrolley)](https://pypi.org/project/dicomtrolley/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicomtrolley)](https://pypi.org/project/dicomtrolley/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nRetrieve medical images using DICOM WADO and MINT.\nRequires python 3.7, 3.8 or 3.9\nRepresents images as `pydicom` Datasets.\n\n![A trolley](docs/resources/trolley.png)\n\n## Usage\n\n### Basic example\n```python\nsession = log_in_to(https://server/login)  # set up   \ntrolley = Trolley(mint=Mint(session, https://server/mint),\n                  wado=Wado(session, https://server/wado]))\n                  \nstudies = trolley.find_studies(\n    Query(patientName=\'B*\')  # find some studies\n\ntrolley.download_study(      # download a study by uid\n    study_instance_uid=studies[0].uid,\n    output_dir=\'/tmp/trolley\')\n```\n\n### Finding studies\n\n```python\nstudies = trolley.find_studies(       # simple find\n    Query(patientName=\'B*\')\n```\n\nQuery parameters can be found in [mint.query.Query](dicomtrolley/query.py). Valid include fields (which information gets sent back) can be found in [include_fields.py](dicomtrolley/include_fields.py): \n```python\nstudies = trolley.find_studies(\n    Query(modalitiesInStudy=\'CT*\',\n          patientSex="F",\n          minStudyDate=datetime(year=2015, month=3, day=1),\n          maxStudyDate=datetime(year=2020, month=3, day=1),\n          includeFields=[\'PatientBirthDate\',\n                         \'SOPClassesInStudy\']))\n```\n\n### Finding series and instance details\nTo include series and instance level information as well, use the `queryLevel` parameter \n```python\nstudies = trolley.find_studies(      # find studies series and instances\n    Query(studyInstanceID=\'B*\', \n          queryLevel=QueryLevels.INSTANCE)\n \na_series = studies.series[0]         # studies now contain series    \nan_instance = a_series.instances[0]  # and series contain instances\n```\n\n### Downloading data\n```python\ntrolley.download_study(              # simple download by uid\n    study_instance_uid=\'123\',  \n    output_dir=\'/tmp/trolley\')\n```\nMore control over download   \n```python\nstudies = trolley.find_studies(      # find study including instances\n    Query(PatientID=\'1234\',\n          queryLevel=QueryLevels.INSTANCE)\n\ninstances = trolley.extract_instances(  \n    studies.series[0])               # download only the first series \n\nfor instance in instances:\n    ds = trolley.get_dataset(instance)\n    ds.save_as(\n        f\'/tmp/{ds.PatientID}\')      # this is a pydicom dataset\n\n```\n\n## Caveats\nDicomtrolley has been developed for and tested on a Vitrea Connection 8.2.0.1 system. This claims to\nbe consistent with WADO and MINT 1.2 interfaces, but does not implement all parts of these standards. \n\nCertain query parameter values and restraints might be specific to Vitrea Connection 8.2.0.1. For example,\nthe exact list of DICOM elements that can be returned from a query might be different for different servers.\n',
    'author': 'sjoerdk',
    'author_email': 'sjoerd.kerkstra@radboudumc.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sjoerdk/dicomtrolley',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
