# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tornado_openapi3']

package_data = \
{'': ['*']}

install_requires = \
['ietfparse>=1.7.0,<2.0.0',
 'openapi-core>=0.13.4,<0.14.0',
 'tornado>=4,<7',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'tornado-openapi3',
    'version': '1.0.1',
    'description': 'Tornado OpenAPI 3 request and response validation library',
    'long_description': '===================\n Tornado OpenAPI 3\n===================\n\n.. image:: https://travis-ci.com/correl/tornado-openapi3.svg?branch=master\n    :target: https://travis-ci.com/correl/tornado-openapi3\n.. image:: https://codecov.io/gh/correl/tornado-openapi3/branch/master/graph/badge.svg?token=CTYWWDXTL9\n    :target: https://codecov.io/gh/correl/tornado-openapi3\n.. image:: https://readthedocs.org/projects/tornado-openapi3/badge/\n    :target: https://tornado-openapi3.readthedocs.io\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n\nTornado OpenAPI 3 request and response validation library.\n\nProvides integration between the `Tornado`_ web framework and `Openapi-core`_\nlibrary for validating request and response objects against an `OpenAPI 3`_\nspecification.\n\nFull documentation is available at https://tornado-openapi3.readthedocs.io\n\nUsage\n=====\n\nAdding validation to request handlers\n-------------------------------------\n\n.. code:: python\n\n   import tornado.ioloop\n   import tornado.web\n   from tornado_openapi3.handler import OpenAPIRequestHandler\n\n\n   class MyRequestHandler(OpenAPIRequestHandler):\n       spec_dict = {\n           "openapi": "3.0.0",\n           "info": {\n               "title": "Simple Example",\n               "version": "1.0.0",\n           },\n           "paths": {\n               "/": {\n                   "get": {\n                       "responses": {\n                           "200": {\n                               "description": "Index",\n                               "content": {\n                                   "text/html": {\n                                       "schema": {"type": "string"},\n                                   }\n                               },\n                           }\n                       }\n                   }\n               }\n           },\n       }\n\n\n   class RootHandler(MyRequestHandler):\n       async def get(self):\n           self.finish("Hello, World!")\n\n\n   if __name__ == "__main__":\n       app = tornado.web.Application([(r"/", RootHandler)])\n       app.listen(8888)\n       tornado.ioloop.IOLoop.current().start()\n\nValidating responses in tests\n-----------------------------\n\n.. code:: python\n\n   import unittest\n\n   import tornado.web\n   from tornado_openapi3.testing import AsyncOpenAPITestCase\n\n\n   class RootHandler(tornado.web.RequestHandler):\n       async def get(self):\n           self.finish("Hello, World!")\n\n\n   class BaseTestCase(AsyncOpenAPITestCase):\n       spec_dict = {\n           "openapi": "3.0.0",\n           "info": {\n               "title": "Simple Example",\n               "version": "1.0.0",\n           },\n           "paths": {\n               "/": {\n                   "get": {\n                       "responses": {\n                           "200": {\n                               "description": "Index",\n                               "content": {\n                                   "text/html": {\n                                       "schema": {"type": "string"},\n                                   }\n                               },\n                           }\n                       }\n                   }\n               }\n           },\n       }\n\n       def get_app(self):\n           return tornado.web.Application([(r"/", RootHandler)])\n\n       def test_root_endpoint(self):\n           response = self.fetch("/")\n           self.assertEqual(200, response.code)\n           self.assertEqual(b"Hello, World!", response.body)\n\n\n   if __name__ == "__main__":\n       unittest.main()\n\nContributing\n============\n\nGetting Started\n---------------\n\nThis project uses `Poetry`_ to manage its dependencies. To set up a local\ndevelopment environment, just run:\n\n.. code:: sh\n\n    poetry install\n\nFormatting Code\n---------------\n\nThe `Black`_ tool is used by this project to format Python code. It is included\nas a development dependency, and should be run on all committed code. To format\ncode prior to committing it and submitting a PR, run:\n\n.. code:: sh\n\n    poetry run black .\n\nRunning Tests\n-------------\n\n`pytest`_ is the preferred test runner for this project. It is included as a\ndevelopment dependency, and is configured to track code coverage, `Flake8`_\nstyle compliance, and `Black`_ code formatting. Tests can be run in your\ndevelopment environment by running:\n\n.. code:: sh\n\n    poetry run pytest\n\nAdditionally, tests can be run using `tox`_, which will run the tests using\nmultiple versions of both Python and Tornado to ensure broad compatibility.\n\nConfiguring Hypothesis\n^^^^^^^^^^^^^^^^^^^^^^\n\nMany of the tests make use of `Hypothesis`_ to specify their expectations and\ngenerate a large volume of randomized test input. Because of this, the tests may\ntake a long time to run on slower computers. Two profiles are defined for\nHypothesis to use which can be selected by setting the ``HYPOTHESIS_PROFILE``\nenvironment variable to one of the following values:\n\n``ci``\n  Runs tests using the default Hypothesis settings (100 examples per test) and\n  no completion deadline.\n\n``dev``\n  The fastest profile, meant for local development only. Uses only 10 examples\n  per test with no completion deadline.\n\n\n.. _Black: https://github.com/psf/black\n.. _Flake8: https://flake8.pycqa.org/\n.. _Hypothesis: https://hypothesis.readthedocs.io/\n.. _OpenAPI 3: https://swagger.io/specification/\n.. _Openapi-core: https://github.com/p1c2u/openapi-core\n.. _Poetry: https://python-poetry.org/\n.. _Tornado: https://www.tornadoweb.org/\n.. _pytest: https://pytest.org/\n.. _tox: https://tox.readthedocs.io/\n',
    'author': 'Correl Roush',
    'author_email': 'correl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/correl/tornado-openapi3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
