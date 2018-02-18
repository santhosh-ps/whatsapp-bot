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
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(),messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                msg,
               to = messageProtocolEntity.getFrom())
           
            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)
     
        else:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
           
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                messageProtocolEntity.getBody(),
               to = messageProtocolEntity.getFrom())
           
            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
 