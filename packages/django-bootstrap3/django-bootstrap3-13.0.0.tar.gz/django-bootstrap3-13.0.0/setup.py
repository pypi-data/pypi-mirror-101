# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootstrap3', 'bootstrap3.templatetags']

package_data = \
{'': ['*'], 'bootstrap3': ['templates/bootstrap3/*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-bootstrap3',
    'version': '13.0.0',
    'description': 'Bootstrap 3 support for Django projects',
    'long_description': '======================\nBootstrap 3 for Django\n======================\n\n.. image:: https://travis-ci.org/dyve/django-bootstrap3.svg\n    :target: https://travis-ci.org/dyve/django-bootstrap3\n\n.. image:: https://readthedocs.org/projects/django-bootstrap3/badge/?version=latest\n    :target: https://django-bootstrap3.readthedocs.io/en/latest/\n\n.. image:: https://img.shields.io/pypi/v/django-bootstrap3.svg\n    :target: https://pypi.org/project/django-bootstrap3/\n    :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://coveralls.io/repos/github/dyve/django-bootstrap3/badge.svg\n    :target: https://coveralls.io/r/dyve/django-bootstrap3\n\n\nBootstrap 3 integration for Django.\n\nGoal\n----\n\nThe goal of this project is to seamlessly blend Django and Bootstrap 3.\n\n**Want to use Bootstrap 4 in Django?**\n\nSee https://github.com/zostera/django-bootstrap4.\n\n\nRequirements\n------------\n\n- Python >= 3.6, Django >= 2.2 (see also https://docs.djangoproject.com/en/dev/faq/install/#faq-python-version-support)\n\nNeed older versions?\n++++++++++++++++++++\n\nThis is our history of dropping support for Python and Django versions. Note that this information is "as is", and you should really update to newer Python and Django versions. Using unsupported versions will lead to security risks and broken software.\n\n- The latest version supporting Python 3.5 Django 2.1 is 12.x.x.\n- The latest version supporting Django 1.11 and 2.0 is 11.x.x.\n- The latest version supporting Django < 1.11 is 9.x.x.\n- The latest version supporting Python 2.6 and Django < 1.8 is 6.x.x.\n\n\nInstallation\n------------\n\n1. Install using pip:\n\n   ``pip install django-bootstrap3``\n\n   Alternatively, you can install download or clone this repo and call ``pip install -e .``.\n\n2. Add to INSTALLED_APPS in your ``settings.py``:\n\n   ``\'bootstrap3\',``\n\n3. In your templates, load the ``bootstrap3`` library and use the ``bootstrap_*`` tags:\n\n\nExample template\n----------------\n\n   .. code:: Django\n\n    {% load bootstrap3 %}\n\n    {# Display a form #}\n\n    <form action="/url/to/submit/" method="post" class="form">\n        {% csrf_token %}\n        {% bootstrap_form form %}\n        {% buttons %}\n            <button type="submit" class="btn btn-primary">\n                {% bootstrap_icon "star" %} Submit\n            </button>\n        {% endbuttons %}\n    </form>\n\n\nDocumentation\n-------------\n\nThe full documentation is at https://django-bootstrap3.readthedocs.org/.\n\n\nBugs and suggestions\n--------------------\n\nIf you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.\n\nhttps://github.com/dyve/django-bootstrap3/issues\n\n\nLicense\n-------\n\nYou can use this under BSD-3-Clause. See `LICENSE <LICENSE>`_ file for details.\n\n\nAuthor\n------\n\nDeveloped and maintained by `Zostera <https://zostera.nl/>`_.\n\nOriginal author & Development lead: `Dylan Verheul <https://github.com/dyve>`_.\n\nThanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.\n\nPlease see `AUTHORS.rst <AUTHORS.rst>`_ for a list of contributors.\n',
    'author': 'Dylan Verheul',
    'author_email': 'dylan@zostera.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zostera/django-bootstrap3',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
