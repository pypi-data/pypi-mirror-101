# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ucr',
 'ucr.core',
 'ucr.core.architecture',
 'ucr.core.architecture.backbone',
 'ucr.core.architecture.head',
 'ucr.core.architecture.neck',
 'ucr.core.architecture.transform',
 'ucr.core.dataloader',
 'ucr.core.postprocess',
 'ucr.core.preprocess',
 'ucr.core.preprocess.text_image_aug',
 'ucr.inference',
 'ucr.utils']

package_data = \
{'': ['*'],
 'ucr': ['conf/*',
         'conf/architecture/*',
         'conf/hydra/job_logging/*',
         'conf/hydra/output/*',
         'conf/postprocess/*',
         'conf/preprocess/*'],
 'ucr.utils': ['dict/*', 'fonts/*', 'imgs/*']}

install_requires = \
['PyMuPDF>=1.18.10,<2.0.0',
 'hydra-core>=1.0.6,<2.0.0',
 'imgaug>=0.4.0,<0.5.0',
 'numpy<1.20.0',
 'opencv-python>=4.1.0,<5.0.0',
 'pandas>=1.1,<1.2',
 'pyclipper>=1.2.1,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.40,<5.0']

entry_points = \
{'console_scripts': ['ucr = ucr.ucr:main']}

setup_kwargs = {
    'name': 'ucr',
    'version': '0.2.12',
    'description': 'Universal Character Recognizer (UCR): Simple, Intuitive, Extensible, Multi-Lingual OCR engine',
    'long_description': '',
    'author': 'Abhigyan Raman',
    'author_email': 'abhigyan@docyard.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
