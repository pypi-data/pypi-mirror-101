.. _aiomsa-advanced:

==============
Advanced Usage
==============

Exposing Prometheus Metrics
===========================

Using the `prometheus_async <https://prometheus-async.readthedocs.io/en/stable/>`_
module, developers can easily add a ``/metrics`` endpoint to the webserver.

.. code-block:: python

   from aiohttp import web
   from aiomsa import init
   from prometheus_async import aio
   from prometheus_client import Counter


   FOO = Counter("foo", "description of foo")


   async def main():
       FOO.inc()


   if __name__ == "__main__":
       app = web.Application()
       app.router.add_get("/metrics", aio.web.server_stats)
       init(lambda: main(), app)
