============
iterdub
============


.. image:: https://img.shields.io/pypi/v/iterdub.svg
        :target: https://pypi.python.org/pypi/iterdub

.. image:: https://img.shields.io/travis/mmore500/iterdub.svg
        :target: https://travis-ci.com/mmore500/iterdub

.. image:: https://readthedocs.org/projects/iterdub/badge/?version=latest
        :target: https://iterdub.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




iterdub makes generating a compact name to describe a series easy & consistent


* Free software: MIT license
* Documentation: https://iterdub.readthedocs.io.


.. code-block:: python3

  from iterdub import iterdub as ib

  # returns 'a'
  ib.dub(['a'])

  # returns 'a~b'
  ib.dub(['a', 'b'])

  # returns 'num_unique%3'
  ib.dub(['a', 'b', 'c'])

  # returns '1-5'
  ib.dub([1,2,3,4,5])

  # returns '1-5%2'
  ib.dub([1,3,5])

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
