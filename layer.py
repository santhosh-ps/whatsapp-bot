from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from Bevco import Bevco
import requests 
class EchoLayer(YowInterfaceLayer):
    hnApi = "http://hn.algolia.com/api/v1/search"
    bevco = Bevco()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
       if messageProtocolEntity.getType() == 'media':
          self.sendMsg(messageProtocolEntity,"")
       else:
            incomingMsg = messageProtocolEntity.getBody().strip().lower()
            sender = messageProtocolEntity.getFrom()
            print(sender+" says "+incomingMsg)
            if  incomingMsg== "hn":
                payload = {'tags':'front_page'}
                r = requests.get(self.hnApi,params=payload)
                msg = self.getMsgFromPosts(r)
                self.sendMsg(messageProtocolEntity,msg)
            elif incomingMsg.startswith("hn ") and len(incomingMsg)>3:
                searchTerm = incomingMsg.split("hn ",1)[1]
                payload= {"query":searchTerm,"tags":"story"}
                r = requests.get(self.hnApi,params=payload)
                msg = self.getMsgFromPosts(r,searchTerm)
                self.sendMsg(messageProtocolEntity,msg)
            elif incomingMsg.startswith("bevco") and len(incomingMsg) > 6:
                searchTerm = incomingMsg.split("bevco ", 1)[1]
                msg = self.getMsgForBottles(searchTerm)
                self.sendMsg(messageProtocolEntity, msg)
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
                "Welcome to hacker news bot, try sending *_hn_* for *hacker-news for the day*\n To search hackernews try sending *_hn<space><search-keyword>_* \n\nOn another note, search Kerala beverages for all available brands and prices \n *bevco<space><brand-name/type>* \nbecause code+drinks = innovation 😉🍻🍻 ",
                to = messageProtocolEntity.getFrom())
        else:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                    message,
                to = messageProtocolEntity.getFrom())
        self.toLower(receipt)
        self.toLower(outgoingMessageProtocolEntity)

    def getMsgFromPosts(self,r,type="normal"):
        response = r.json()
        if r.status_code == 500:
            msg = response.get('error')
        else:
            posts = response.get('hits')
            msg='*Hacker News For the day* \n\n'
            if type!="normal":
                msg='*Hacker News search results for _'+type+'_:* \n\n'
            for post in posts:
                rTitle = post.get('_highlightResult').get('title').get("value").replace("<em>","*").replace("</em>","*")
                #print(rTitle)
                msg+=str(rTitle)+'\n\n*points :* '+str(post.get('points'))+'\n\n Url : '+str(post.get('url'))+'\n ------------------------------------------------- \n\n'
        return msg

    def getMsgForBottles(self,term):
        term = term.upper()
        searchBottles = self.bevco.getBottlesByName(term)
        msg = "🍺 *Bevco Price List for _"+term+"_:* \n\n"
        if len(searchBottles) is 0:
            msg = "No bottles found.."
            return msg
        for bottle in searchBottles:
            msg += "🍻 *"+bottle.get("brand")+"* vol : *"+bottle.get("size") + \
                "*  Rs *"+bottle.get("amount")+"*\n\n"
        return msg



