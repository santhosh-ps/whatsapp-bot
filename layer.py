from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

import requests 
class EchoLayer(YowInterfaceLayer):
    hnApi = "http://hn.algolia.com/api/v1/search"

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
       if messageProtocolEntity.getType() == 'media':
          self.sendMsg(messageProtocolEntity,"")
       else:
            incomingMsg = messageProtocolEntity.getBody()
            sender = messageProtocolEntity.getFrom()
            print(sender+" says "+incomingMsg)
            if  incomingMsg== "hn" or incomingMsg == "Hn" or incomingMsg == "HN":
                payload = {'tags':'front_page'}
                r = requests.get(self.hnApi,params=payload)
                response = r.json()
                if r.status_code == 500:
                    msg = response.get('error')
                else:
                    posts = response.get('hits')
                    msg='*Hacker News For the day* \n\n'
                    for post in posts:
                        msg+=''+post.get('title')+'\n'+'*points :* '+str(post.get('points'))+'\n\n Url : '+post.get('url')+'\n ------------------------------------------------- \n\n'
                self.sendMsg(messageProtocolEntity,msg)
            else:
                self.sendMsg(messageProtocolEntity,"")
               

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
 
    def sendMsg(self,messageProtocolEntity,message):
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(),
         messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
        if message=="":
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                    "Welcome to hacker news bot, try sending 'hn' for *hacker-news*",
                to = messageProtocolEntity.getFrom())
        else:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                    message,
                to = messageProtocolEntity.getFrom())
        self.toLower(receipt)
        self.toLower(outgoingMessageProtocolEntity)
