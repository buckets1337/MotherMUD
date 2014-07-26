# cChat.py
"""
defines the 'say' command, the 'tell' command, the 'shout' command, the 'chat' command, and all individual chat channel commands
"""

class Channel():    # a Chat channel
    def __init__(self):
        pass


def say(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Echo whatever client types after the command 'say' to everyone in the room.
    """

    message = ""
    space = " "
    # for arg in args:
    message = space.join(args)
    clientDataID = str(client.addrport())
    prompt = CLIENT_DATA[clientDataID].prompt

    print '   <%s:%s>%s: %s' % (CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].avatar.currentRoom.name.capitalize(), CLIENT_DATA[clientDataID].name, message)

    for guest in CLIENT_LIST:
        if guest != client:
            if CLIENT_DATA[str(guest.addrport())].avatar.currentRoom == CLIENT_DATA[clientDataID].avatar.currentRoom:
                guest.send_cc('\n^!%s says "%s"^..\n' % (CLIENT_DATA[clientDataID].name, message))
                # guest.send(prompt)
        else:
            guest.send('You say "%s".\n' % message)
            # guest.send(prompt)


def shout(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Echo whatever client types after the command 'shout' to everyone in the region.
    """

    message = ""
    space = " "
    # for arg in args:
    message = space.join(args)
    clientDataID = str(client.addrport())
    prompt = CLIENT_DATA[clientDataID].prompt

    print '   <%s>%s: %s' % (CLIENT_DATA[clientDataID].avatar.currentRoom.region, CLIENT_DATA[clientDataID].name, message)

    for guest in CLIENT_LIST:
        if guest != client:
            if CLIENT_DATA[str(guest.addrport())].avatar.currentRoom.region == CLIENT_DATA[clientDataID].avatar.currentRoom.region:
                guest.send_cc('\n^!%s shouts "%s" from somewhere nearby.^.\n' % (CLIENT_DATA[clientDataID].name, message))
                # guest.send(prompt)
        else:
            guest.send('You shout "%s" for all to hear.\n' % message)
            # guest.send(prompt)


def chat(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Echo whatever client types after the command 'say' to everyone in the room.
    """

    message = ""
    space = " "
    # for arg in args:
    message = space.join(args)
    clientDataID = str(client.addrport())
    prompt = CLIENT_DATA[clientDataID].prompt

    print '   <chat> %s: %s' % (CLIENT_DATA[clientDataID].name, message)

    for guest in CLIENT_LIST:
        if guest != client:
            guest.send_cc('^Y^I<chat>^~ ^W%s^~: "%s"^~\n' % (CLIENT_DATA[clientDataID].name, message))
                # guest.send(prompt)
        else:
            guest.send_cc('^Y^I<chat>^~ ^U%s^~: %s^~\n' % (CLIENT_DATA[clientDataID].name, message))
            # guest.send(prompt)

    CLIENT_DATA[clientDataID].replyTo = None


def tell(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Send args as a message to a specific player specified by the first argument immediately following the command
    """
    who = args[0]
    message = " ".join(args[1:])
    senderName = CLIENT_DATA[str(client.addrport())].name
    success = False
    isSelf = False

    for player in CLIENT_LIST:
        clientDataID = str(player.addrport())
        if CLIENT_DATA[clientDataID].name == who:
            if CLIENT_DATA[clientDataID].name != CLIENT_DATA[str(client.addrport())].name:
                player.send_cc("^W^I" + senderName + " tells you:^~^w " + message +"^~\n")
                CLIENT_DATA[clientDataID].replyTo = client
                CLIENT_DATA[str(client.addrport())].replyTo = player
                success = True
                print "   <" + str(CLIENT_DATA[clientDataID].name) + '>'+ senderName + ": " + message
            else:
                client.send_cc('^wYou mutter "' + message + '" to yourself quietly.^~\n')
                success = True
                isSelf = True
    if success:
        if not isSelf:
            client.send_cc("^W^IYou tell "+ who + ":^~^w "+ message +"^~\n")
        return True
        
    else:
        client.send_cc("^wIt appears "+ who + " isnt around right now.^~\n")
        return False

