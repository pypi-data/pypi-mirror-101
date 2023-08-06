'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Tuesday, 16th March 2021 7:20:17 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''

from adcopen import Events
from typing import Any

class RTrig:
    """Rising Edge detector.

    Attributes
    ----------
    input : bool
        A rising edge sets the output Q for one execution.
    signal : string
        A topic name to signal any time the output Q transitions to True
    userdata : Any
        Optional data that can be attached to the instance.

    """

    input : bool = False
    signal : str = None
    userdata : Any = None

    _m : bool = False
    _monitor_topic : str = None

    def __init__(self, 
        input:bool=False, 
        monitor_topic:str=None, 
        signal:str=None,
        userdata:Any = None
    ) -> None:
        """Constructor

        Parameters
        ----------

        input : bool
            Optional. A rising edge sets the output Q for one execution.
        monitor_topic : str
            Optional. Register a topic for the class to monitor, 
            updating the input value automatically.
        signal : str    
            Optional. A topic name to signal any time the output Q has changed.
        userdata : Any
            Optional data that can be attached to the instance.

        """
        self.input = input
        self.signal = signal
        self.userdata = userdata
        self._m = self.input        
        self.set_monitor_topic(monitor_topic)
        
    def set_monitor_topic(self, monitor_topic:str) -> None:
        """Register a topic for the class to monitor, updating the input value
        automatically.
        """
        if not monitor_topic == None:

            # Register monitoring this topic

            self._monitor_topic = monitor_topic


            def monitor_topic_changed(val):
                self.input = val

                if self.signal != None and len(self.signal) > 0:
                    self.q()

            Events.subscribe_method(self._monitor_topic, monitor_topic_changed)
        
        
        elif not self._monitor_topic == None:

            # Unregister monitoring this topic
            # @todo: add this ability to the events library
            # supplying a second argument to the pop method ensures that
            # an exception will not be thrown if the topic has not be registered
            Events.subs.pop(self._monitor_topic, "") 

        else:
            self._monitor_topic = None        

    def q(self) -> bool:
        """Rising edge output. Returns True only on the
        rising edge condition of input.
        """
        ret = self.input and not self._m

        if ret and self.signal != None:
            Events.publish(self.signal, self.userdata)

            

        self._m = self.input
        return ret




class FTrig:
    """Falling Edge detector

    Attributes
    ----------
    input : bool
        A falling edge sets the output q for one execution.
    signal : string
        A topic name to signal any time the output Q transitions to True
    userdata : Any
        Optional data that can be attached to the instance.        
    """

    input : bool = True
    signal : str = None
    userdata : Any = None

    _m : bool = True
    _monitor_topic : str = None

    def __init__(self, 
        input:bool=True, 
        monitor_topic:str=None, 
        signal:str = None,
        userdata:Any=None
    ) -> None:
        """Constructor

        Parameters
        ----------

        input : bool
            Optional. A rising edge sets the output Q for one execution.
        monitor_topic : str
            Optional. Register a topic for the class to monitor, 
            updating the input value automatically.
        signal : str    
            Optional. A topic name to signal any time the output Q has changed.
        """
        self.input = input
        self.signal = signal
        self.userdata = userdata
        self._m = self.input        
        self.set_monitor_topic(monitor_topic)

    def set_monitor_topic(self, monitor_topic:str) -> None:
        """Register a topic for the class to monitor, updating the input value
        automatically.
        """
        if not monitor_topic == None:

            # Register monitoring this topic

            self._monitor_topic = monitor_topic


            def monitor_topic_changed(val):
                self.input = val

                if self.signal != None and len(self.signal) > 0:
                    self.q()

            Events.subscribe_method(self._monitor_topic, monitor_topic_changed)
        
        
        elif not self._monitor_topic == None:

            # Unregister monitoring this topic
            # @todo: add this ability to the events library
            # supplying a second argument to the pop method ensures that
            # an exception will not be thrown if the topic has not be registered
            Events.subs.pop(self._monitor_topic, "") 

        else:
            self._monitor_topic = None        

    def q(self) -> bool:
        """Falling edge output. Returns True only on the
        falling edge condition of input.
        """
        ret = not self.input and not self._m

        if ret and self.signal != None:
            Events.publish(self.signal, self.userdata)

        self._m = not self.input
        return ret





if __name__ == '__main__':

    import asyncio
    import logging

    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")


    @Events.subscribe("rt-done")
    async def rtdone(value):
        print(f"rt-done {value}")

    @Events.subscribe("ft-done")
    async def ftdone(value):
        print(f"ft-done {value}")        

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


    async def test_basic():
        """Basic test using the RTrig in a non-blocking scenario,
        similar to structured text.
        """

        print( "\n\n\nTest basic usage...")


        rt = RTrig(signal="rt-done", userdata="basic usage")
        ft = FTrig(signal="ft-done", userdata="basic usage")

        for x in range(1,10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        rt.input = True
        ft.input = True

        for x in range(1,10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        rt.input = False
        ft.input = False

        for x in range(1,10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)


        print("Basic usage test complete.")


    async def test_monitor():
        """In this test, the RTrig isn't updated from code, but by
        using asynchronous events.
        """


        print( "\n\n\nTest monitor_topic...")

        rt = RTrig(signal="rt-done", userdata="monitor usage", monitor_topic="mysignal")
        ft = FTrig(signal="ft-done", userdata="monitor usage", monitor_topic="mysignal")

        await asyncio.sleep(delay=1)
        
        print("monitor_topic: publish")
        Events.publish("mysignal", True)

        await asyncio.sleep(delay=3)

        for x in range(1,10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        Events.publish("mysignal", False)

        for x in range(1,10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        Events.publish("mysignal", True)


        for x in range(1,10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)


        print("monitor_topic test complete")        


    async def run_tests():
        """Run all tests in an async method.
        """

        print( "\n\n\nStart running tests...")

        await test_basic()
        await test_monitor()

        print( "Tests complete")





    try:

        asyncio.run_coroutine_threadsafe(run_tests(), loop)

        print( "Press CTRL-C to stop.")  

        loop.run_forever()

    except KeyboardInterrupt:
        
        print( "Closing from keyboard request.")  


    except Exception as ex:

        print( f"CoreLink exception: {ex}")  
        print(ex)
            
    finally:
        
        loop.stop()

        print( "Goodbye.")
            
