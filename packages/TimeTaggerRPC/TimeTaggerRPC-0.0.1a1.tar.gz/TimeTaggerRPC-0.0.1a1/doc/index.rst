.. Time Tagger RPC documentation master file, created by
   sphinx-quickstart on Thu Apr  1 11:53:59 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Remote Time Tagger with Python
===========================================


Install

::

   > pip install TimeTaggerRPC



Start the server on a PC with the Time Tagger connected.

::

   > TimeTaggerRPC-server


Control Time Tagger remotely over the network.

.. code-block:: python

   import matplotlib.pyplot as plt
   from TimeTaggerRPC import cleint

   with client.createProxy(host='localhost', port=23000) as TT:
      tagger = TT.createTimeTagger()

      hist = TT.Correlation(tagger, 1, 2, binwidth=10, n_bins=2000)
      hist.startFor(int(10e12), clear=True)

      x = hist.getIndex()
      while hist.isRunning():
         plt.pause(0.1)
         y = hist.getData()
         plt.plot(x, y)


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   internals




.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
