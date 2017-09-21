************
Throttle Bag
************

A Python library for API throttling.

Installation
============

To install the latest release on `PyPi <https://pypi.python.org/pypi/throttle-bag>`_,
simply run:

::

  pip install throttle_bag

Or to install the latest development version, run:

::

  git clone https://github.com/xinhuang/throttle-bag.git
  cd throttle-bag
  python setup.py install

Quick Tutorial
==============

.. code:: pycon

  >>> from throttle_bag import Throttle
  >>>
  >>> api = Throttle(ThrottledServer(), seconds=10, times=20)
  >>> while True:
  >>>     api.get()

API Reference
=============

``Throttle(throttled_object, seconds, times=1)``
  Create a instance of ``Throttle`` to throttle invocations to all methods of throttled_object, according to frequence
  specified.

  :Args:
    * ``seconds``: Specify throttling interval in seconds.
    * ``times``: Specify how many invocations can be made in given interval.

Licensing
=========

This project is released under the terms of the MIT Open Source License. View
*LICENSE.txt* for more information.
