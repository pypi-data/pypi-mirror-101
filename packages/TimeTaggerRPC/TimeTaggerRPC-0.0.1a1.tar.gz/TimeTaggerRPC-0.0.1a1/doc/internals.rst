==================
How does it work
==================



`Time Tagger <https://www.swabianinstruments.com/time-tagger/>`__ is a great instrument for data acquisition whenever you are detecting, counting or analyzing single photons. 
You can quickly setup a time correlation measurement, coincidence analysis and much more. 
However at some point in your project you may want to control your experiment remotely. 
While you can simply use a remote desktop software, like VNC, TeamViewer, Windows Remote Desktop, etc.
What if you want to programmatically control your remote experiment? Are you using multiple computers and want to collect data from many of them at the same time? 
Then you will have to delve into programming remote control interfaces.
Luckily, this task is very common and there are many software libraries that 
release you from burden of dealing with network sockets and messaging protocols.

In this article, I will show you how to apply the :doc:`Pyro5<pyro5:index>` and how it allows you to achieve practically seamless access 
to the :doc:`Time Tagger's API<ttdoc:api/index>` remotely.



Remote procedure calling
===========================

Remote procedure calling (RPC) is a technology that allows to interact with remote programs
by calling their procedures and receiving the responses.
This involves a real code execution on one computer (server), 
while the client computer has only a substitute object (proxy) that mimics the real thing running on the sever.
The proxy object knows how to send requests and data to the server 
and the server knows how to interpret these requests and how to execute the real code.

In case of ``Pyro5`` the proxy object and server code is provided by the library 
and we only need to tell ``Pyro5`` what we want to become available remotely.


Initial setup
=================
You will need to have a Python 3.6 or newer installed on your computer. 
We recommend to use Anaconda distribution.

Install the `Time Tagger software <https://www.swabianinstruments.com/time-tagger/downloads/>`__ if have not done yet.
The further text assumes that you have the Time Tagger hardware and are familiar with the :doc:`Time Tagger API<ttdoc:api/index>`.

The last missing part, the Pyro5 package, you can install from `PyPi <https://pypi.org/project/Pyro5/>`__ as

:: 

    pip install Pyro5


Minimal example
====================

Here we start from the simplest functional example and demonstrate working remote communication.
The example consists of two parts, the server and the client code. 
You will need to run those in two separate command windows.

.. rubric:: Server code

All we need is to create an adapter class with methods which we want to access remotely and decorate it with 
:func:`pyro5:Pyro5.api.expose`. The following code is very simple and later we will extend it to expose more of the Time Tagger's functionality.

.. code-block:: python

    import Pyro5.api
    import TimeTagger as TT

    @Pyro5.api.expose
    class TimeTaggerRPC:
        """Adapter for the Time Tagger Library"""

        def scanTimeTagger(self):
            """This method will become available remotely."""
            return TT.scanTimeTagger()


    if __name__ == '__main__':
        # Start server and expose the TimeTaggerRPC class
        with Pyro5.api.Daemon(host='localhost', port=23000) as daemon:
            # Register class with Pyro 
            uri = daemon.register(TimeTaggerRPC, 'TimeTagger')     
            # Print the URI of the published object
            print(uri)
            # Start the server event loop
            daemon.requestLoop()                                  


.. rubric:: Client code

On the client side, we need to know the unique identifier of the exposed object which was printed when you started `server.py`
In Pyro5, every object is identified by a special string (URI) that contains object identity string and the server address.
As you can see in the code below, we do not use the Time Tagger software directly, but rather communicate to the server that has it.

.. code:: python

    import Pyro5.api

    # Connect to the TimeTaggerRPC object on the server
    # This line is all we need to establish remote communication
    TT = Pyro5.api.Proxy("PYRO:TimeTagger@localhost:23000")

    # Now we can call methods that will be executed on the server.
    # Lets check what Time Taggers are available at the server
    timetaggers = TT.scanTimeTagger()
    print(timetaggers)

    >> ['1740000ABC', '1750000ABC']


Congratulations! Now you have a very simple but functional communication to your remote Time Tagger software.

Creating the Time Tagger
=========================
By now our code can communicate over network and can only report the serial numbers of the connected Time Taggers.
In this section we will expand the server code and make it more useful.
Definitely, the next most important feature of the server is to expose the :func:`ttdoc:createTimeTagger` method 
so we can tell the server to initialize the Time Tagger hardware.

You may be tempted to quickly extend the `TimeTaggerRPC` class as follows.

.. code-block:: python

    @Pyro5.api.expose
    class TimeTaggerRPC:
        """Adapter for the Time Tagger Library"""

        def scanTimeTagger(self):
            """Return the serial numbers of the available Time Taggers."""
            return TT.scanTimeTagger()

        def createTimeTagger(self):
            """Create the Time Tagger."""
            return TT.createTimeTagger()  # This will fail! :(

To our great disappointment, the `createTimeTagger` method will fail when you try to access it from the client.
The reason is in how the RPC communication works. 
The data and the program code has a certain format in which it is stored in the computer's memory, 
and this memory cannot be easily or safely accessed from a remote computer. 
The RPC communication overcomes this problem by using data serialization, i.e. 
converting the data into a generalized format suitable for sending over network 
and understandable by a client system.

The `Pyro5`, more specifically the `serpent` serializer it employs by default, 
knows how to serialize the standard Python data types like list of strings returned by :func:`ttdoc:scanTimeTagger`. 
However, it has no idea how to interpret the :class:`ttdoc:TimeTagger` object returned by the :func:`ttdoc.createTimeTagger`. 
Moreover, instead of sending the :class:`ttdoc:TimeTagger` object to the client, 
we actually want to send a proxy object which allows the client talk to the :class:`ttdoc:TimeTagger` object on the server.

For the :class:`ttdoc:TimeTagger`, we define an adapter class. Then we modify the :meth:`TimeTaggerRPC.createTimeTagger` 
so that it creates an instance of the adapter class, registers it with Pyro and returns it. 
Pyro will automatically take care of creating a proxy object for the client. 


.. code-block:: python

    @Pyro5.api.expose
    class TimeTagger:
        """Adapter for the Time Tagger object"""

        def __init__(self, args, kwargs):
            self._obj = TT.createTimeTagger(*args, **kwargs)

        def setTestSignal(self, *args):
            return self._obj.setTestSignal(*args)

        def getSerial(self):
            return self._obj.getSerial()

        # ... Other methods of the TT.TimeTagger class are omitted here.


    @Pyro5.api.expose
    class TimeTaggerRPC:
        """Adapter for the Time Tagger Library"""

        def scanTimeTagger(self):
            """Return the serial numbers of the available Time Taggers."""
            return TT.scanTimeTagger()

        def createTimeTagger(self, *args, **kwargs):
            """Create the Time Tagger."""
            tagger = TimeTagger(args, kwargs)
            self._pyroDaemon.register(tagger)
            return tagger
            # Pyro will automatically create and send a proxy object 
            # to the client.


Measurements and virtual channels
=============================================
By now we are able to list available Time Tagger devices and create TimeTagger objects. 
The remaining part is to implement access to the measurements and virtual channels.
We will use the same approach as with the TimeTagger class and create adapter classes for them.
Note that the methods :meth:`ttdoc:Histogram.getIndex` and :meth:`ttdoc:Histogram.getData` return :class:`numpy:numpy.ndarray` arrays
which we also have to convert to the Python list before sending to the client.

.. code-block:: python

    @Pyro5.api.expose
    class Histogram:
        """Adapter class for Histogram measurement."""

        def __init__(self, tagger, args, kwargs):
            self._obj = TT.Histogram(tagger._obj, *args, **kwargs)

        def start(self):
            return self._obj.start()

        def startFor(self, capture_duration, clear):
            return self._obj.startFor(capture_duration, clear=clear)

        def stop(self):
            return self._obj.stop()

        def clear(self):
            return self._obj.clear()

        def isRunning(self):
            return self._obj.isRunning()

        def getIndex(self):
            return self._obj.getIndex().tolist()

        def getData(self):
            return self._obj.getData().tolist()


    @Pyro5.api.expose
    class DelayedChannel():
        """Adapter class for DelayedChannel."""

        def __init__(self, tagger, args, kwargs):
            self._obj = TT.DelayedChannel(tagger._obj, *args, **kwargs)

        def getChannel(self):
            return self._obj.getChannel()


    @Pyro5.api.expose
    class TimeTaggerRPC:
        """Adapter class for the Time Tagger Library"""

        #  Earlier code omitted (...)

        def Histogram(self, tagger_proxy, *args, **kwargs):
            """Create Histogram measurement."""
            objectId = proxy._pyroUri.object
            tagger_obj = self._pyroDaemon.objectsById.get(objectId)
            pyro_obj = Histogram(tagger_obj, args, kwargs)
            self._pyroDaemon.register(pyro_obj)
            return pyro_obj

        def DelayedChannel(self, tagger_proxy, *args, **kwargs):
            """Create DelayedChannel."""
            objectId = proxy._pyroUri.object
            tagger_obj = self._pyroDaemon.objectsById.get(objectId)
            pyro_obj = DelayedChannel(tagger_obj, args, kwargs)
            self._pyroDaemon.register(pyro_obj)
            return pyro_obj

Working example
================

Download the complete source files 
    * :download:`server.py <../TimeTaggerRPC/server.py>`
    * :download:`simple_example.py <../examples/simple_example.py>`

Start the server in a terminal window

:: 

    > python server.py

Now open a second terminal window and run the example 

:: 

    > python simple_example.py

Let us take a look at the source code of the example, (shown below). 
You may recognize that it is practically the same as if you would use the Time Tagger package directly.
The only difference is that the import code ``import TimeTagger as TT`` is replaced by the proxy object creation
``TT = Pyro5.api.Proxy("PYRO:TimeTagger@localhost:23000")``.

.. literalinclude:: ../examples/simple_example.py
    :caption: simple_example.py
    :language: python
    
