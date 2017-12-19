#! /usr/bin/python
import time
import sys
from slackclient import SlackClient
import slacktoken

##sc.api_call(
#  "chat.postMessage",
#  channel="#random",
#  text="Hello World :tada:"
#)

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
    if slack_output and len (slack_output) > 0:
        for item in slack_output:
            if accept(item, bot_id):
                return item['user'],item['text'], item['channel']
    return None,None,None


def send_msg( sc, channel, text ):
    sc.api_call("chat.postMessage", channel=channel,text=text, as_user=True)



def handle_command(sc, user, command, channel):
    if (" kill " in command):
        if( user == bot_master):
            send_msg(sc,channel,"OK. bye bye ! :scream:")
            exit()
        else:
            send_msg(sc,channel,"You're not my master !")

def get_id(userlist, name):
    users = userlist.get('members')
    for user in users:
        if 'name' in user and user.get('name') == name:
            return user.get('id')
    return ""

if __name__ == "__main__":

    slack_token =slacktoken.get_token()
    sc = SlackClient(slack_token)
    bot_id = 0
    userlist = sc.api_call("users.list")
    if userlist.get('ok'):
        bot_id = get_id(userlist, BOT_NAME)
        print "My id is "+bot_id
    else:
        print("Cannot get user list")


    if sc.rtm_connect():
        print("Slack bot connected !")

        if len(sys.argv) > 1 :
            message = ""
            if sys.argv[1] == "msg":
                channel = sys.argv[2]
                for w in sys.argv[3:]:
                    message+=w+" "

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

            exit()


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

