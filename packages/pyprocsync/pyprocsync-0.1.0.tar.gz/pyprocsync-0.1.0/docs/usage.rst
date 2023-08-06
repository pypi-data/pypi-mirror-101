=====
Usage
=====

Basics
------

To use PyProcSync in a project::

    from pyprocsync import ProcSync

In order to work you need a Redis server (or a cluster in large deployments) accessible by all the nodes that will run code that needs to be synchronized::

    import redis
    procsync = ProcSync(redis.from_url("redis://localhost:6379/0"), "testrun1")

**IMPORTANT:** The `run_id` (testrun1 in the above example) must be unique and the same on all nodes. After running a synchronized scenario the run_id must be changed to something different (and set the same on all nodes).

When your program reaches a point where it needs to synchronize to other nodes before continuing execution simply call `sync` and supply the name of the synchronization point and the nodes needed to be synchronized::

    # doing some work asychronously

    procsync.sync("test1", 3)  # <- Wait for all 3 nodes to reach the synchronization point named "test1"

    # continue executing at the same time as the other three nodes

**NOTE:** You do not need all your nodes that takes part of the same run to call `sync` thus you don't need to set the nodes parameter to the number of all nodes.
This allows you to define synchronization points only a portion of nodes need to synchronize to. But always make sure that the right amount of nodes are specified otherwise you may face unforeseen consequences.

You may call `close` after you no longer need to synchronize or your scenario reached the end. This unsubscribes from the subscribed pubsub channel, and closes Redis connection::

    procync.close()

Timeout
-------

It is possible to set a timeout when waiting for other nodes to synchronize.
In an ideal world this would be unnecessary because it's purpose is to allow developers recover from a scenario where one or more of the nodes became offline or simply taking an irrational amount of time to synchronize.

By default timeouts are disabled so each node waits infinite amount of time for a synchronized condition.

Using a timeout is simple, provide it as the third parameter to the `sync` call (in seconds)::

    from pyprocsync import TimeOutError

    try:
        procsync.sync("test2", 3, 60)
    except TimeOutError:
        # The synchronization could not be done in a minute.
        # Terminate everything!



Setting the delay
-----------------

Delay is the amount of time (seconds) added to the current time when announced. In other words it's the amount of time you give each node to receive the announced time of continue and wait the remaining time in order to continue the execution at the exact same time on each node.

Based on your network you may want to change this delay. The default value is 1 sec.

For example...
 * If your nodes are on remote locations where latency may go above 1 sec, and you encounter ANY `TooLateError` you HAVE TO increase the delay.
 * On the other hand, if all your processes run very close to eachother (even on the same host) you can decrease the delay to make synchronizations happen faster.

The delay is assigned when you create the ProcSync object::

    from pyprocsync import ProcSync, TooLateError

    procsync = ProcSync(redis.from_url("redis://localhost:6379/0"), "testrun2", 10)

    try:
        procsync.sync("test2", 3)
    except TooLateError:
        # 10 seconds wasn't enough time to distribute the time of continue
        # There is some serious problem
        # Terminate everything!

**NOTE:** When the delay is low enough, slight drifts between system clocks can also result in `TooLateError` error.
