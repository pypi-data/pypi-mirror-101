==========
PyProcSync
==========


.. image:: https://img.shields.io/pypi/v/pyprocsync.svg
        :target: https://pypi.python.org/pypi/pyprocsync

.. image:: https://img.shields.io/travis/marcsello/pyprocsync.svg
        :target: https://travis-ci.com/marcsello/pyprocsync

.. image:: https://readthedocs.org/projects/pyprocsync/badge/?version=latest
        :target: https://pyprocsync.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Synchronize events between processes over the network.
This package provides similar behaviour as Python's `threading.Event` but it is designed to be used with multiple processes running on different computers.

An example use-case might be controlling multiple industrial robots handling anomalous materials, where timing is critical.


* Free software: MIT license
* Documentation: https://pyprocsync.readthedocs.io



Features
--------

* Uses Redis as a backend
* About 1ms precision (see. `perf_tests`)
* Synchronize events based on system clock (NTP is a must have)
* Synchronize unlimited number of nodes with the same precision (Depends on the performance of Redis cluster)

Example
-------

Simple example that synchronizes 4 nodes::

    import redis
    from pyprocsync import ProcSync

    p = ProcSync(redis.from_url('redis://localhost:6379/0'))

    # Do some work

    p.sync("first", 4) # Block until all 4 nodes are reached the synchronization point

    # Time sensitive work



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
