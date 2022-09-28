import json

# this is going to be what all of our consumers inherit from
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync


# create your 1st consumer
# inherit from WebsocketConsumer object
# its going to be responsible for incoming messages from the client and
# broadcasting them to anybody that has a connection to this consumer all in 
# real time
class ChatConsumer(WebsocketConsumer):

    # consumers structure are code into a series of functions

    # for the initial request that comes in from the client
    def connect(self):
        # set a group name
        # this would be a dynamic value from our url
        self.room_group_name = 'test'
        # we access the channel layer and call the group_add()
        async_to_sync(self.channel_layer.group_add)(
            # to add a users channel to the group
            # specify group name and users channel name
            self.room_group_name,
            self.channel_name
            # for channel_name, we dont need to create this
            # it will create automatically for each user

        )

        #create connection from the client
        self.accept()
        # send a message back, notifying the client that connection was made

        # # just receive the message on the client side and console out just to
        # # make sure that the connetion was established.
        # self.send(text_data=json.dumps({
        #     # the data we send back will just be a stringified object with a type
        #     #  and a msg value
        #     # these values are completely upto us
        #     # this is just to know for me, just to see in front-end
        #     'type': 'connection_established',
        #     'message': 'you are now connected!'
        # }))



    # when we recieve messages from the client
    # will listen for incoming msgs from the client
    def receive(self,text_data):
        # parse the data and handle the response
        text_data_json = json.loads(text_data)
        # now text_data_json contains json value,
        
        # to change above value to text format
        # set the message variable to data that was send from the client
        message = text_data_json['message']

        # print('message:', message)

        # # use send method to send  a message back to client whenever we receive
        # # a message
        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message':message
        # }))
        # # using send method, we want to stringify the data and add in the type of
        # # chat, so we can use the information in the front end and pass in the actual
        # # msg value

        # use group_send() to broadcaste the msg to every specific user in the
        # group
        async_to_sync(self.channel_layer.group_send)(
            # specify group name
            self.room_group_name,
            # along with the msg , name of the function that we want to handle
            # this event
            {
                'type' : 'chat_message',
                'message' : message
            }
        )
        

    def chat_message(self, event):
        # use the event object to retrieve the msg
        message = event['message']

        # because this msg was send to a group
        # every user that has a channel in this group will receive this msg and 
        # this will be broadcasted out in real time
        self.send(text_data=json.dumps({
            'type' :'chat',
            'message' : message
        }))

    # to handle what happens when a client disconnects from this consumer
    # def disconnect(self, close_code):
    #     pass