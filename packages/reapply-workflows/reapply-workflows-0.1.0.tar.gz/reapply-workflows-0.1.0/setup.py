# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backend',
 'backend.inference_core',
 'backend.inference_core.algorithms',
 'backend.inference_core.reapply',
 'backend.inference_core.reapply.data_structures',
 'backend.inference_core.reapply.data_structures.Provenance',
 'backend.inference_core.reapply.reapply_algorithms',
 'backend.server',
 'backend.server.celery',
 'backend.server.database',
 'backend.server.database.schemas',
 'backend.server.database.schemas.algorithms',
 'backend.server.routes',
 'backend.server.routes.dataset',
 'backend.server.routes.project',
 'backend.utils']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Cors>=3.0.9,<4.0.0',
 'Flask>=1.1.2,<2.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'SQLAlchemy>=1.3.20,<2.0.0',
 'asciitree>=0.3.3,<0.4.0',
 'celery>=5.0.5,<6.0.0',
 'firebase-admin>=4.5.2,<5.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'paretoset>=1.2.0,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'tqdm>=4.56.2,<5.0.0']

setup_kwargs = {
    'name': 'reapply-workflows',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kiran Gadhave',
    'author_email': 'kirangadhave2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
