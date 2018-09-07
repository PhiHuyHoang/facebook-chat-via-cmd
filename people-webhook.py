from fbchat import Client
from fbchat.models import *
from os import system, name
from time import sleep
import getpass
import sys

# Subclass fbchat.Client and override required methods
class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # If you're not the author, echo
        if author_id != self.uid:
            self.send(message_object, thread_id=thread_id, thread_type=thread_type)

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def search_friend():
    try:
        search_user = input("Search friend: ")
        if search_user == "stop chat":
            clear()
            sys.exit(0)
        else:
            users = client.searchForUsers(search_user)
            user = users[0]
            print("User's ID: {}".format(user.uid))
            print("User's name: {}".format(user.name))
            print("User's profile picture url: {}".format(user.photo))
            print("User's main url: {}".format(user.url))
            return user.uid
    except Exception as e:
        print(e)
        print("Error")


def show_message(id_user,limit_mess):
    try:
        messages = client.fetchThreadMessages(thread_id=id_user, limit=limit_mess)
        # # Since the message come in reversed order, reverse them
        messages.reverse()
        #
        # # Prints the content of all the messages
        for message in messages:
            print("Message:",message.text)
    except:
        print("No message found")

def send_message(id_user):
    continues = "ok"

    while continues == "ok":
        # Gets the last 10 messages sent to the thread
        clear()

        show_message(id_user,10)

        thread_id = id_user
        thread_type = ThreadType.USER
        send_message = input("Send message? ...")
        if send_message == 'ok':
            text = input("Message: ")
            # Will send a message to the thread
            client.send(Message(text=text), thread_id=thread_id, thread_type=thread_type)
        continues = input("Keep loading? ...")
    menu()

def thread_list():
    clear()
    threads = client.fetchThreadList()
    # Fetches the next 10 threads
    threads += client.fetchThreadList(before=5, limit=5)

    for thread in range(10):
        print("Friend:",threads[thread].name)
        show_message(threads[thread].uid,1)

def menu():
    start = "ok"
    thread_list()
    while start == "ok":
        id_user = str(search_friend())
        chat_connect = input("Do you want to chat with him/her? ")
        if chat_connect == "ok":
            send_message(id_user)
        else:
            menu()


username = input("Username: ")
password = getpass.getpass('Password:')

client = EchoBot(username, password)
menu()

print("You arre login out ...")


