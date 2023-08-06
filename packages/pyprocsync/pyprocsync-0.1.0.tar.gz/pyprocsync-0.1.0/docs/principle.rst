=================
Working principle
=================

PyProcSync's magic depends on important features of Redis:
The atomic increment-and-get_ and the built in pubsub_ message broker.

.. _increment-and-get: https://redis.io/commands/INCR
.. _pubsub: https://redis.io/topics/pubsub

The idea
--------

The goal of PyProcSync is to solve time critical program synchronization over the network between multiple nodes.
One simple and obvious solution is to use the nodes' clock since those can be synchronized very precisely using NTP_ and PTP_.
This way we don't need complicated and exotic synchronization protocols.

.. _NTP: https://tools.ietf.org/html/rfc5905
.. _PTP: https://en.wikipedia.org/wiki/Precision_Time_Protocol

The basic idea of PyProcSync is that each node may agree on a future timestamp on which they continue the execution. In theory this eliminates the network latency in the system completely.

This "agreement" protocol is realized using a Redis as shared memory and message broker.

Deciding the time of continue
-----------------------------

Given that we know of how many nodes are required to synchronize their execution.
We simply count if all nodes reached the synchronization point using a simple counter incremented when a process reached the synchronization point (conceptually similar to semaphores).

The last node reaching the synchronization point can identify that all nodes reached the point because the value of the counter will be equal to the number of the total number of required nodes.
Then the last node uses it's own system clock, adds a predefined amount of time and then publish that future timestamp.

Each node is then receive the timestamp calculated by the last node. And uses their own system clock to calculate the amount time it should sleep before continuing the execution.

Flow
----

The following figure depicts the basic flow of a synchronization using PyProcSync.

.. image:: _static/working-principle.svg
