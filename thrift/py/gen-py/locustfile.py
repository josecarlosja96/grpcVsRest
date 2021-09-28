#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
This contains to load test of Hello World example of gRPC call with locust.
"""

# Built-in/Generic Imports
import sys
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import inspect
import time
import gevent
from tutorial import Calculator
from tutorial.ttypes import InvalidOperation, Operation, Work

# Libs
from locust.contrib.fasthttp import FastHttpUser
from locust import task, events, constant
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, WorkerRunner

def stopwatch(func):
    """To be updated"""

    def wrapper(*args, **kwargs):
        """To be updated"""
        # get task's function name
        previous_frame = inspect.currentframe().f_back
        _, _, task_name, _, _ = inspect.getframeinfo(previous_frame)

        start = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            total = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        response_length=0,
                                        exception=e)
        else:
            total = int((time.time() - start) * 1000)
            events.request_success.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        response_length=0)
        return result

    return wrapper

class GRPCMyLocust(FastHttpUser):

    host = 'http://127.0.0.1:9090'
    wait_time = constant(0)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task
    @stopwatch
    def grpc_client_task(self):
        """To be updated"""
        try:
            transport = TSocket.TSocket('localhost', 9090)

            transport = TTransport.TBufferedTransport(transport)

            # Wrap in a protocol
            protocol = TBinaryProtocol.TBinaryProtocol(transport)

            # Create a client to use the protocol encoder
            client = Calculator.Client(protocol)

            # Connect!
            transport.open()
            client.zip()

            # Close!
            transport.close()

        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)

# Stopping the locust if a threshold (in this case the fail ratio) is exceeded
def checker(environment):
    while not environment.runner.state in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
        time.sleep(1)
        if environment.runner.stats.total.fail_ratio > 0.2:
            print(f"fail ratio was {environment.runner.stats.total.fail_ratio}, quitting")
            environment.runner.quit()
            return


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    if not isinstance(environment.runner, WorkerRunner):
        gevent.spawn(checker, environment)
