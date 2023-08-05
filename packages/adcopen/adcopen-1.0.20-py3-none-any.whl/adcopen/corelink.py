

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
    CYCLE_DATA : str = "adcopen/corelink/signals/publish_cycle_data"
    RESET_DATA : str = "adcopen/corelink/signals/reset_data"
    TEST_DATA_CHANGE : str = "adcopen/corelink/signals/test_data_change"
    START_TEST : str = "adcopen/corelink/signals/start_test"
    STOP_TEST : str = "adcopen/corelink/signals/stop_test"  #optional stopcode argument
    ERROR_MESSAGE : str = "corelink/signals/error-message"
    VALUE_DATA_CHANGE : str = "dataChange"


class CoreLinkSlots:
    """Events from the autocore-server to the clients.
    """
    CONNECTED : str = 'adcopen/corelink/slots/connected'
    DISCONNECTED : str = 'adcopen/corelink/slots/disconnected'
    CYCLE_DATA : str = 'adcopen/corelink/slots/cycle_data_received'
    RESET_DATA : str = "adcopen/corelink/slots/reset_data"
    TEST_DATA_CHANGE : str = "adcopen/corelink/slots/test_data_change"
    EXPORT_DATA : str = "adcopen/corelink/slots/export_data"
    REQ_CONFIGURATION_VALUES : str = "adcopen/corelink/slots/req_configuration_values"
    SET_CONFIGURATION_VALUE : str = "adcopen/corelink/slots/set_configuration_value"
    TEST_STARTED : str = "adcopen/corelink/slots/test_started"
    TEST_STOPPED : str = "adcopen/corelink/slots/test_stopped"
    VALUE_DATA_CHANGE : str = "dataChange"


class CoreLinkValues:
    """Standard value keys
    These probably aren't everything a particular system will need,
    but they are values every test should incorporate.
    """

    # the accumlated meta data for a test
    TEST_DATA : str = "adcopen/values/test_data"           
    # the name of the operator running the test
    OPERATOR_NAME : str = "adcopen/values/operator_name"
    # The name of this test.
    TEST_NAME : str = "adcopen/values/test_name"
    # The ID of the sample. Could be a barcode, could just be text.
    SAMPLE_ID : str = "adcopen/values/test_id"
    # Expected to be a JSON object/dict of key-value pairs with information
    TEST_METADATA : str = "adcopen/values/test_metadata"



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

    @staticmethod
    def publish_cycle_data(moduleName:str, data : any):
        """Broadcast data for the method to process to the autocore-server and as
        a global Event.

        It is expected that the autocore-server will spin up the Method script
        for this data to be processed. The data should also be placed into the
        in-memory data store for access later.
        """

        if isinstance(data, pd.DataFrame):
            data = data.to_json()            

        out = {"module":moduleName, "data": data}

        Events.publish(CoreLinkSignals.CYCLE_DATA, out)

        CoreLink.publish(CoreLinkSignals.CYCLE_DATA, json.dumps(out))

    @staticmethod
    def start_test(module_name:str = ""):
        """Signal the autocore-server to request a start of the test.
        For purely-automated systems. The general expectation is that
        the test will be started from the user interface.
        """

        CoreLink.publish(CoreLinkSignals.START_TEST, module_name)

    @staticmethod
    def stop_test(module_name:str = "", reason : CoreLinkStopCodes = CoreLinkStopCodes.UNSPECIFIED):
        """Signal the autocore-server to request stopping the test.
        Some ADC systems use this to simply interrupt a test before it's completed,
        others will just keep running until stopped by calling this function.

        params:
            module_name: the name of the module making the request. Informational.
            reason: The reaosn for stopping the test. May effect data being stored.
        """

        out = { "module":module_name, "reason":reason}
        CoreLink.publish(CoreLinkSignals.STOP_TEST, json.dumps(out))


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

    @staticmethod
    def set_test_data(value:Any) -> None:
        """Set the current value of the test data. This should generally be a 
        pandas DataFrame, and this function will attempt to convert it into JSON.
        """
        CoreLink.set_value(CoreLinkValues.TEST_DATA, value)
        
    @staticmethod
    def get_test_data() -> pd.DataFrame:
        """Get the current test data structure as a Pandas DataFrame.
        CoreLink should have stored the value in memory as a JSON structure, and
        this function will attempt to convert the JSON to a DataFrame.
        """
        rc = CoreLink.get_value(CoreLinkValues.TEST_DATA)

        if isinstance(rc, pd.DataFrame):
            return rc
        else:
            pd.read_json(json.loads(rc))
    



        




if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")

    @Events.subscribe(CoreLinkSlots.CONNECTED)
    async def connected(data):
        print("SLOT connected")
        CoreLink.subscribe("testtopic")
        #sample = {"Load" : [100,200,300,200], "Position": [1,2,3,4]}
        #rc = CoreLink.publish_cycle_data("CoreLinkClient", sample)


    @Events.subscribe(CoreLinkSlots.CYCLE_DATA)
    async def on_cycle_data(data):

        payload = json.loads(data)
        print(f"Data received from autocore!\n\t{payload}")



    @Events.subscribe("simulator/rand10")
    async def subscribe_test(data):
        print(f"Received simulator/rand10 value: {data}")

        sample = {"Load" : [100,200,300,200], "Position": [1,2,3,4]}
        CoreLink.publish_cycle_data("CoreLinkTest", pd.DataFrame(sample))

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:


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
