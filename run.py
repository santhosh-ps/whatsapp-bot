from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv
from dotenv import load_dotenv
import os
from os.path import expanduser
envPath = str(expanduser("~")) + '/whatsappbot.env'
print(envPath)
load_dotenv(envPath)


UNAME = str(os.environ.get("uname"))
PASS = str(os.environ.get("pass"))

credentials = (UNAME, PASS) # replace with your phone and password

if __name__==  "__main__":
    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()
    print("setting credentials")
    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
    try:
        stack.loop() #this is the program mainloop
    except AuthError as e:
        print("Authentication Error: %s" % e.message)
    
