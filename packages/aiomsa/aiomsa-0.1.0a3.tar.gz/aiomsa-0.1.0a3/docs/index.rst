==================================
Welcome to aiomsa's documentation!
==================================

.. toctree::
   :hidden:
   :maxdepth: 2

   reference
   advanced
   misc

*aiomsa* is a Python 3.7+ framework built using :mod:`asyncio`. At its core,
*aiomsa* provides a simple and standardized way to write xApps that can be deployed as
microservices in Python.

In addition, *aiomsa* creates an HTTP server with
:doc:`preinstalled endpoints<./routes>` for xApp configuration. Developers can add
their own endpoints to this server for their own application logic.

Usage
=====

The entrypoint for the *aiomsa* framework is the :func:`~.init` function.

.. autofunction:: aiomsa.init

Quickstart
----------

The follwing example shows how to use *aiomsa* to create a simple microservice for
consuming and printing records from an E2T subscription.

A ``lambda`` wrapper of ``main``, the entrypoint for the service's business logic, and
its parameters are supplied to the :func:`~.init` function.

.. code-block:: python

   from aiomsa import init
   from aiomsa.e2 import E2Client

   from .models import MyModel


   async def main():
      with E2Client(
         app_id="my_app", e2t_endpoint="e2t:5150", e2sub_endpoint="e2sub:5150"
      ) as e2:
         conns = await e2.list_nodes()
         subscription = await e2.subscribe(
            e2_node_id=conns[0],
            service_model_name="my_model",
            service_model_version="v1",
            trigger=bytes(MyModel(param="foo")),
         )

         async for msg in subscription:
            print(msg)


   if __name__ == "__main__":
      init(lambda: main())

Installation
============

*aiomsa* can be installed from PyPI.

.. code-block:: bash

    $ pip install aiomsa

You can also get the latest code from GitHub.

.. code-block:: bash

    $ poetry add git+https://github.com/facebookexternal/aiomsa

Dependencies
============

* Python 3.7+
* aiohttp
* aiohttp-swagger
* betterproto
