


**!!! This is a development alpha version !!!**

Time Tagger RPC implementation using Pyro5.


### Install

```
> pip install TimeTaggerRPC
```

### Run server
Start the server on a PC with the Time Tagger connected.

```
> TimeTaggerRPC-server
```

### Client example
Control Time Tagger remotely over the network.


```python
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
```