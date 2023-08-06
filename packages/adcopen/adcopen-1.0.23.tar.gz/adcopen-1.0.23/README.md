## ADCOpen
### Open-source python libraries for data integration with ADC equipment.

Licensed for use with ADC equipment. 
automateddesign.com


#1.0.23
- Adds CoreLink synchronous connect/disconnect methods to make life easier on
end users integrating streamlit.


#1.0.22
- Updates CoreLink client for additional API features and cleans out depreacted
features. Implements DataStore features.


#1.0.21
- events.py now attempts to create an event loop when subscribing if one does
not already exist. This is contrary to original intention, but makes it easier
for our end-user to integrate scripts.


#1.0.20
- Changes when CoreLink creates client instance. Originally, was creating upon
import, but that caused problems with Streamlit.

#1.0.19
- Adds ONDATACHANGE support to events.py, which is now the default. Option to
always receive the event can be passed as argument to subscribe method.

#1.0.18
- API change to Ton.start() to make it easier to use in state machines.


#1.0.17
- Add Ton and edge trigger classes.


#1.0.16
- Convert to socketio


#1.0.15
- Trying to fix bug where pressing ctrl-c causes hard crash instead of graceful shutdown.



#1.0.13:
- Fix issue with traceback library swallowing ctrl-c events when program interrupted by keyboard
- Add minimal CoreLink client for integration with autocore-js webserver. 