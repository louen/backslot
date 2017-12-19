#! /usr/bin/python
import time
import sys
from slackclient import SlackClient
import slacktoken

BOT_NAME = "backslot"
DELAY=1 # 1 second delay
bot_master="U4270B8UD"


def accept(item,bot_id):
    """ returns true if the item should be accepted by us"""
    print "accepted"
    for i in item:
        print i, item[i]
    if item and 'text' in item:
        if "<@"+bot_id+">" in item['text'] and item['user']!=bot_id:
            return True
    return False

def parse( slack_output, bot_id ):
    """ Parse a slack message and return the message sender, message text and channel"""
    if slack_output and len (slack_output) > 0:
        for item in slack_output:
            if accept(item, bot_id):
                return item['user'],item['text'], item['channel']
    return None,None,None

def send_msg( sc, channel, text ):
    """ Send a message on the given channel"""
    sc.api_call("chat.postMessage", channel=channel,text=text, as_user=True)

def handle_command(sc, user, command, channel):
    """ Take action with a given command"""
    if (" kill " in command):
        if( user == bot_master):
            send_msg(sc,channel,"OK. bye bye ! :scream:")
            exit()
        else:
            send_msg(sc,channel,"You're not my master !")

def get_id(userlist, name):
    """ Return the user id from its name"""
    users = userlist.get('members')
    for user in users:
        if 'name' in user and user.get('name') == name:
            return user.get('id')
    return ""

if __name__ == "__main__":

    # Initialize slack client
    slack_token =slacktoken.get_token()
    sc = SlackClient(slack_token)
    bot_id = 0
    # Check my id
    userlist = sc.api_call("users.list")
    if userlist.get('ok'):
        bot_id = get_id(userlist, BOT_NAME)
        print "My id is "+bot_id
    else:
        print("Cannot get user list")


    if sc.rtm_connect():
        print("Slack bot connected !")

        ## If the bot was lauched with arguments, we are in "single message mode"
        if len(sys.argv) > 1 :
            message = ""
            # Send a normal message
            if sys.argv[1] == "msg":
                channel = sys.argv[2]
                for w in sys.argv[3:]:
                    message+=w+" "
            # Send a message with a highlight
            elif sys.argv[1] == "hl":
                user = sys.argv[2]
                user_id = get_id(userlist, user)
                if len(user_id) > 0:
                    message = "<@"+user_id+">"
                    channel = sys.argv[3]
                    for w in sys.argv[4:]:
                        message+=w+" "
            if message != "":
                send_msg(sc, channel, message);

            # After sending the message, quit
            exit()


        # If the bot was launched with no argument, we are on bot mode, so we start the main loop
        send_msg(sc, "#random", "Slack bot ready for combat");

        # main loop
        while True:
            user,command,channel = parse( sc.rtm_read(), bot_id)
            if command and channel:
                print("got " +command+" from "+channel)
                handle_command(sc,user, command,channel)
            time.sleep(DELAY)
    else:
        print("Connection  failed")

