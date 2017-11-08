************
Throttle Bag
************
.. image:: https://img.shields.io/pypi/v/throttle-bag.svg
    :target: https://pypi.python.org/pypi/throttle-bag

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
  >>> import requests
  >>>
  >>> r = Throttle(requests, seconds=10, times=20)
  >>> while True:
  >>>     r.get('http://www.google.com')

API Reference
=============

``Throttle(throttled_object, seconds, times=1, aio=False, loop=None, delay=None)``
  Create a instance of ``Throttle`` to throttle invocations to all methods of throttled_object, according to frequence
  specified.

  :Args:
    * ``throttled_object``: The object to be throttled.
    * ``seconds``: Specify throttling interval in seconds.
    * ``times``: Specify how many invocations can be made in the given interval.
    * ``aio``: Whether use ``asyncio.sleep()`` instead of ``time.sleep()``.
    * ``loop``: The ``EventLoop`` if using asyncio. By default it is ``asyncio.get_event_loop()``.
    * ``delay``: Custom delay function. For synchronized, it is ``def delay(seconds)``; for asynchronized, it
      is ``async def delay(seconds)``.

Licensing
=========

This project is released under the terms of the MIT Open Source License. View
*LICENSE.txt* for more information.
