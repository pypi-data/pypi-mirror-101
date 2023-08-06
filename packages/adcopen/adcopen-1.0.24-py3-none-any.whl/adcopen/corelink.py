'''
(C) Copyright 2020-2021 Automated Design Corp. All Rights Reserved.
File Created: Wednesday, 3rd February 2021 7:44:24 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''

"""
Important!
Disable ctrl-c causing an exception and blocking graceful shutdown.
"""
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'


from typing import Any
import socketio
import json
import logging
import asyncio
import pandas as pd

from adcopen import Events

# Create a named logger instance
log = logging.getLogger(__name__)


class CoreLinkStopCodes:
    UNSPECIFIED = 0
    TEST_COMPLETED = 1
    USER_STOPPED = 2
    SYSTEM_FAULT = 3
    INVALID_DATA = 4


class CoreLinkSignals:
    """Signals we will send out to the autocore-server, but will never
    expect to receive.
    """
    ERROR_MESSAGE : str = "corelink/signals/error-message"
    VALUE_DATA_CHANGE : str = "dataChange"


class CoreLinkSlots:
    """Events from the autocore-server to the clients.
    """
    CONNECTED : str = 'adcopen/corelink/slots/connected'
    DISCONNECTED : str = 'adcopen/corelink/slots/disconnected'
    REQ_CONFIGURATION_VALUES : str = "adcopen/corelink/slots/req_configuration_values"
    SET_CONFIGURATION_VALUE : str = "adcopen/corelink/slots/set_configuration_value"
    VALUE_DATA_CHANGE : str = "dataChange"


class CoreLink:
    """Client Link to the AutoCore CoreLink server
    Asynchronous Inter-process communication.

    This is a minimumal implementation of the CoreLink "API" specific to how
    Python is used in our projects.
    """

    client : socketio.AsyncClient = None
    is_connected : bool = False
    subscribed_values = {}

    # By default, CoreLink will automatically save 
    auto_save_test_data : bool = True


    @staticmethod
    def start(host, port):
        """Start the Client connection. This method will return immediately
        and the connection will be monitored asynchronously. Do not execute
        futher CoreLink requests until the connected signal has been
        emitted.
        """

        CoreLink.client = socketio.AsyncClient()

        """ Callbacks from the client
        """

        @CoreLink.client.event
        async def connect():
            """The client has successfully connected to autocore-server
            """
            log.info(msg="CoreLink - connected!")
            CoreLink.is_connected = True

            Events.publish(CoreLinkSlots.CONNECTED, {})

        @CoreLink.client.event
        def disconnect():
            """The client has successfully connected to autocore-server
            """
            log.info(msg="CoreLink - disconnected!")
            CoreLink.is_connected = False
            Events.publish(CoreLinkSlots.DISCONNECTED, {})


        @CoreLink.client.on(CoreLinkSlots.VALUE_DATA_CHANGE)
        async def dataChange(data):
            """Datachange event, which is usually a value related to a tag.
            """
            if "topic" in data and "value" in data:

                if data["topic"] in CoreLink.subscribed_values:
                    """Buffer the value in case it is requested synchronously later
                    """
                    CoreLink.subscribed_values[data["topic"]] = data["value"]

                Events.publish(data["topic"], data["value"])            

        @CoreLink.client.event
        def connect_error():
            """Failed to connect to the server"""
            log.error("CoreLink - The connection failed!")      
            CoreLink.is_connected = False

        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(CoreLink.start_async(host,port), loop)

    @staticmethod
    def stop():
        """Stop processing and close the client connection to the AutoCore Server.
        """
        log.info(msg="CoreLink: Stopping connection")
        CoreLink.is_connected = False
        asyncio.run_coroutine_threadsafe(CoreLink.client.disconnect(), loop)


    @staticmethod
    def connect(host, port):
        """Make a synchronous connection to the AutoCore-Server.
        Blocks until the connection is completed.
        Use only for scripts not utilizing asyncio.
        """

        should_return = False

        async def run_connect(host, port):

            nonlocal should_return

            @Events.subscribe(CoreLinkSlots.CONNECTED)
            async def connected(data):
                nonlocal should_return

                should_return = True

            CoreLink.start(host,port)

            count = 0
            done = False
            while not done:

                count += 1
                await asyncio.sleep(delay=0.1)

                if should_return or count > 20:
                    done = True

            return should_return


        loop = asyncio.get_event_loop()
        ret = loop.run_until_complete(run_connect(host,port))

        return ret


    @staticmethod
    def disconnect():
        """Synchronous disconnection from the AutoCore-Server. 
        Blocks until disconnection is completed.
        Use only for scripts not utilizing asyncio.
        """
        log.info(msg="CoreLink: Stopping connection synchronously.")
        CoreLink.is_connected = False
        loop = asyncio.get_event_loop()
        ret = loop.run_until_complete(CoreLink.client.disconnect())





    @staticmethod
    async def start_async(host,port):
        """Asynchronous function to start the CoreLink connection.
        The socketio client should already be created.
        Don't call this function directly. Instead, call start, which
        will call this function after having made the necessary preparations.
        """
        log.info(f"Starting CoreLink connection http://{host}:{port}")
        await CoreLink.client.connect(f"http://{host}:{port}")


    @staticmethod
    def publish(topic : str, value : Any):
        """Publish any value on the specified topic to the autocore-server.        
        """

        payload = {"topic": topic, "value":value}

        if CoreLink.is_connected():
            CoreLink.client.emit(CoreLinkSignals.VALUE_DATA_CHANGE, value)
        else:
            raise Exception("Client is not connected.")


    @staticmethod
    def publish_error_message(moduleName : str, msg : str):
        """Broadcast an error message to the autocore-server and
        as a global Event.
        """
        out = {"module":moduleName, "message": msg}
        topic = "corelink/signals/error-message"
        Events.publish(topic, out)

        CoreLink.publish(CoreLinkSignals.ERROR_MESSAGE, msg)

    # @staticmethod
    # def publish_cycle_data(moduleName:str, data : any):
    #     """Broadcast data for the method to process to the autocore-server and as
    #     a global Event.

    #     It is expected that the autocore-server will spin up the Method script
    #     for this data to be processed. The data should also be placed into the
    #     in-memory data store for access later.
    #     """

    #     if isinstance(data, pd.DataFrame):
    #         data = data.to_json()            

    #     out = {"module":moduleName, "data": data}

    #     Events.publish(CoreLinkSignals.CYCLE_DATA, out)

    #     CoreLink.publish(CoreLinkSignals.CYCLE_DATA, json.dumps(out))

    # @staticmethod
    # def start_test(module_name:str = ""):
    #     """Signal the autocore-server to request a start of the test.
    #     For purely-automated systems. The general expectation is that
    #     the test will be started from the user interface.
    #     """

    #     CoreLink.publish(CoreLinkSignals.START_TEST, module_name)

    # @staticmethod
    # def stop_test(module_name:str = "", reason : CoreLinkStopCodes = CoreLinkStopCodes.UNSPECIFIED):
    #     """Signal the autocore-server to request stopping the test.
    #     Some ADC systems use this to simply interrupt a test before it's completed,
    #     others will just keep running until stopped by calling this function.

    #     params:
    #         module_name: the name of the module making the request. Informational.
    #         reason: The reaosn for stopping the test. May effect data being stored.
    #     """

    #     out = { "module":module_name, "reason":reason}
    #     CoreLink.publish(CoreLinkSignals.STOP_TEST, json.dumps(out))


    @staticmethod
    def set_value(key : str, value:Any) -> None:
        """Set and publish a value accessible through inter-process communication.
        """

        tmp = value

        if isinstance(tmp, pd.DataFrame):
            tmp = tmp.to_json()

        if not key in CoreLink.subscribed_values:
            CoreLink.subscribed_values[key] = tmp
            CoreLink.subscribe(key)
            CoreLink.subscribed_values.append(key)

        CoreLink.publish(key, tmp)


    @staticmethod
    def get_value(key:str) -> Any:
        """Get the value to the matching key, if it has been subscribed
        and refreshed, or set at least once.
        """

        if key in CoreLink.subscribed_values:
            return CoreLink.subscribed_values[key]
        else:
            return None

    # @staticmethod
    # def set_test_data(value:Any) -> None:
    #     """Set the current value of the test data. This should generally be a 
    #     pandas DataFrame, and this function will attempt to convert it into JSON.
    #     """
    #     CoreLink.set_value(CoreLinkValues.TEST_DATA, value)
        
    # @staticmethod
    # def get_test_data() -> pd.DataFrame:
    #     """Get the current test data structure as a Pandas DataFrame.
    #     CoreLink should have stored the value in memory as a JSON structure, and
    #     this function will attempt to convert the JSON to a DataFrame.
    #     """
    #     rc = CoreLink.get_value(CoreLinkValues.TEST_DATA)

    #     if isinstance(rc, pd.DataFrame):
    #         return rc
    #     else:
    #         pd.read_json(json.loads(rc))


    @staticmethod
    async def create_datastore(key : str) -> None:
        """Create a data store in the server.
        If the datastore already exists, this function does nothing.
        """
        should_return = False
        rc = False

        @CoreLink.client.on("res-datastore-create")
        async def res_create_datastore(data):
            nonlocal should_return
            should_return = True

            nonlocal rc
            if "success" in data:
                rc = data["success"]

        await CoreLink.client.emit("req-datastore-create", data={"key": key})

        count = 0
        done = False
        while not done:

            count += 1
            await asyncio.sleep(delay=0.1)

            if should_return or count > 20:
                done = True

        return rc


    @staticmethod
    async def get_datastore_value(key : str) -> Any:
        """Read a value from the existing datastore.
        """
        should_return = False
        rc = None
        success = False
        error_message = ""

        @CoreLink.client.on("res-datastore-get-value")
        async def res_create_datastore(data):
            nonlocal should_return
            should_return = True

            nonlocal rc
            nonlocal success
            nonlocal error_message


            if "success" in data:
                if data["success"]:
                    rc = data["value"]
                    success = True
                else:
                    error_message = data["errorMessage"]


        await CoreLink.client.emit("req-datastore-get-value", data={"key": key})

        count = 0
        done = False
        while not done:

            count += 1
            await asyncio.sleep(delay=0.1)

            if should_return or count > 20:
                done = True


        if not success:
            raise error_message

        return rc


    @staticmethod
    async def set_datastore_value(key : str, value : Any) -> None:
        """Set an existing data store to a value.
        """
        should_return = False
        success = False
        error_message = ""

        @CoreLink.client.on("res-datastore-set-value")
        async def res_create_datastore(data):
            nonlocal should_return
            should_return = True

            nonlocal success
            nonlocal error_message


            if "success" in data:
                if data["success"]:
                    success = True
                else:
                    error_message = data["errorMessage"]


        await CoreLink.client.emit("req-datastore-set-value", data={"key": key, "value" : value})

        count = 0
        done = False
        while not done:

            count += 1
            await asyncio.sleep(delay=0.1)

            if should_return or count > 20:
                done = True


        if not success:
            raise error_message


    @staticmethod
    async def append_datastore_value(key : str, value : Any) -> None:
        """Append a value to an existing datastore value. If that
        value is already an array, the value is append. If it isn't,
        then the existing value is converted to an array and the new 
        value appended.
        """
        should_return = False
        success = False
        error_message = ""

        @CoreLink.client.on("res-datastore-append-value")
        async def res_create_datastore(data):
            nonlocal should_return
            should_return = True

            nonlocal success
            nonlocal error_message


            if "success" in data:
                if data["success"]:
                    success = True
                else:
                    error_message = data["errorMessage"]


        await CoreLink.client.emit("req-datastore-append-value", data={"key": key, "value" : value})

        count = 0
        done = False
        while not done:

            count += 1
            await asyncio.sleep(delay=0.1)

            if should_return or count > 20:
                done = True


        if not success:
            raise error_message







if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")

    @Events.subscribe(CoreLinkSlots.CONNECTED)
    async def connected(data):
        print("SLOT connected")

        asyncio.run_coroutine_threadsafe(test_datastore(), loop)


    @Events.subscribe("simulator/rand10")
    async def subscribe_test(data):
        print(f"Received simulator/rand10 value: {data}")


    async def test_datastore():

        print( "Let's test the datastore!")

        try:
            await CoreLink.create_datastore("corelink-test")
            await asyncio.sleep(delay=2)
            await CoreLink.create_datastore("corelink-test")
            await asyncio.sleep(delay=2)
            await CoreLink.set_datastore_value("corelink-test", "too many secrets")
            await asyncio.sleep(delay=2)
            rc = await CoreLink.get_datastore_value("corelink-test")

            print(f"Data store value: {rc}")

            await asyncio.sleep(delay=2)
            rc = await CoreLink.append_datastore_value("corelink-test", "setec astronomy")
            await asyncio.sleep(delay=2)
            rc = await CoreLink.get_datastore_value("corelink-test")

            print(f"Data store value: {rc}")

            print( "DataStore test complete.")

        except Exception as ex:
            log.exception(ex)


    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:

        print("First, test synchronous connection")
        CoreLink.connect("127.0.0.1", 8081)

        print(f"Am I connected? {CoreLink.is_connected}")


        print("Stop connection synchrnously...")
        CoreLink.disconnect()

        print("Restart with async method...")

        CoreLink.start("127.0.0.1", 8081)
        print( "Press CTRL-C to stop.")  



        loop.run_forever()

    except KeyboardInterrupt:
        
        print( "Closing from keyboard request.")  


    except Exception as ex:

        print( f"CoreLink exception: {ex}")  
        print(ex)
            
    finally:
        
        CoreLink.stop()       
        
        loop.stop()

        print( "Goodbye.")
