from twilio.rest import Client

def sendText(phoneNumber, body):
    client = Client("ACb4062d2c42e84a87eaef22235fcdcac1", "029b0411ceb8615d4d769f10b4bc6966")
    message = client.messages.create(
    to=phoneNumber, 
    from_="+12182749208",
    body=body)
    print(message.sid)
