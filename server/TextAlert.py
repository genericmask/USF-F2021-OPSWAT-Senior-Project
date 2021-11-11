from twilio.rest import Client

def sendText(phoneNumber, body):
    if phoneNumber != '' and phoneNumber is not None:
        client = Client("ACb4062d2c42e84a87eaef22235fcdcac1", "c196bf3d893442a2da33bb0f87dc2e30")
        message = client.messages.create(
        to=phoneNumber, 
        from_="+12182749208",
        body=body)
        #print(message.sid)