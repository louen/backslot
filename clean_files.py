#! /usr/bin/python
import time
import sys
from slackclient import SlackClient
import slacktoken

USER="U4270B8UD"

def get_files( sc, tok,user ):
    filelist = sc.api_call("files.list", token=tok)
    if filelist.get('ok'):
        count = filelist.get('paging').get('total')
        print "got", count,"files"
        filelist = sc.api_call("files.list", token=tok, count=count)

        return filelist.get('files')
    else:
        print "Cannot get file list"


def rm_file( sc, tok, file ):
    file_id= file.get('id')
    result =sc.api_call("files.delete", token=tok, file=file_id)
    
    if result.get('ok') == False:
        print "ERROR removing "+file.get('name')
        print result

if __name__ == "__main__":
    slack_token = slacktoken.get_token()
    sc = SlackClient(slack_token)

    filelist = get_files(sc, slack_token, USER)

    for f in filelist:
        if f.get('size') > 2 * 1024 * 1024:
            print f.get('name')," ", f.get('size')
            rm_file(sc,slack_token,f)
