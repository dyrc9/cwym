from threading import Thread
import time
import sys
from utils import *
import random

from TCPclient import client
import PySimpleGUI as sg



#because received message should be print to the gui, I rewrite the receive function
def receive(client, window):
    while True:
        try:
            msg = client.recv(1024).decode()
            
        except:
            print("receive wrong")
            window.write_event_value(
                "-RECEIVEERROR-",
                time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()),
            )
            exit()
        msgtype, room, msgcontent = analysis_msg(msg)
        #print(msg) #for test
        window.write_event_value(
            "-RECEIVE-",
            (
                time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()),
                msgtype,
                room,
                msgcontent
            )
        )

#Here is the code of file transfer
#To Do

def main():
    aclient = client()

    userid = "nobody"
    bg_color_me = "#66FFFF" #color of your own message
    bg_color_sys = "#7CFC00" #color of the system message from server
    bg_color_sqr = "#ffd258"   #color of the message that all the client can see
    bg_color_pri = "#D8BFD8" #color of the message that send to you

    #the gui of client
    theme = random.choice(sg.theme_list())
    sg.theme(theme)
    #roomid = "test"
    layout = [
        [sg.Titlebar("CWYM Chatroom")],
        [
            sg.Text(
                f"Nickname: {userid}", key = "-NAME-", font="Franklin 12 bold", text_color="blue"
            ),
            sg.Push(),
            sg.Combo(  # sg.Combo sg.OptionMenu
                [
                    "Square",
                    "Alice",
                    "Bob",
                    "Carol",
                    "Dave",
                    "Eve",
                ],
                font="Franklin 12",
                size=(13, 10),
                default_value="Square",
                enable_events=True,
                readonly=True,
                background_color='#FFFFFF',
                text_color = "#000000",
                key="-ROOMS_OPTION-",
            ),
         ],
        #the output 
        [
            sg.Multiline(
                f" Hello!\n Welcome to the cwym chat!\n\n",
                font="Franklin 11",
                no_scrollbar=True,
                size=(50, 20),
                text_color="black",
                horizontal_scroll=True,
                autoscroll=True,
                echo_stdout_stderr=True,
                reroute_stdout=True,
                # write_only=True,
                reroute_cprint=True,
                disabled=True,
                # enter_submits=True,
                key="-OUTPUT-",
            ),
        ],
        #the input
        [
            sg.Multiline(
                font="Franklin 11",
                no_scrollbar=True,
                size=(50, 5),
                horizontal_scroll=False,
                autoscroll=True,
                key="-INPUT-",
            )
        ],
        [
            sg.Button("Send", size=(12, 1), key="-SEND-", button_color="#219F94"),
            sg.Button("File transfer", size=(12,1), key="-FILE-"),
            sg.Push(),
            sg.Button("Who are here?", size=(12,1), key="-ANYONE-"),
            sg.Button("Exit", size=(12, 1), key="-EXIT-"),
        ],
    ]

    #init the gui window
    window = sg.Window("", layout, finalize=True)
    sg.cprint_set_output_destination(window, "-OUTPUT-")

    #init receive thread
    Thread(target=receive, args=(aclient.clientSocket, window), daemon=True).start()
    fltransfer = 0

    #the main loop
    while True:
        event, values = window.read()

        #exit the chat room
        if event in [sg.WIN_CLOSED, "-EXIT-"]:
            break

        #receive the message
        if event == "-RECEIVE-":
            val = values[event]
            clock = val[0] #not used yet
            msgtp = val[1] #the type of the message
            room = val[2] #the type of the room
            msg = val[3] #the raw message     

            #The message is normal message, which means it is from other client.                             
            if messagetype[msgtp] == "normal message":
                #The message is for all the user in the chatroom.
                if roomtype[room] == "Square":
                    sg.cprint(
                        f"{msg}\n",
                        c=("#000000", bg_color_sqr),
                    )
                #The message is for only you.
                else:
                    sg.cprint(
                        f"{msg}\n",
                        c=("#000000", bg_color_pri),
                    )

            #the message is from the server for the first time connected
            if messagetype[msgtp] == "connection": #get the username
                userid = msg
                sg.cprint(
                    f"Connect successfully! your name is {userid}\n",
                    c=("#000000", bg_color_sys),
                )
                window["-NAME-"].update(f"Your name: {userid}")

            #the message feedback when you click the botton "Who are here?"
            if messagetype[msgtp] == "askstatus":
                sg.cprint(
                        f"{msg}\n",
                        c=("#000000", bg_color_sys),
                    )

        #send the message
        if event == "-SEND-":
            msg = f"{values['-INPUT-']}"
            room = values["-ROOMS_OPTION-"]
            if room == "Square":
                roomtp = 0
            elif room == "Alice":
                roomtp = 1
            elif room == "Bob":
                roomtp = 2
            elif room == "Carol":
                roomtp = 3
            elif room == "Dave":
                roomtp = 4
            elif room == "Eve":
                roomtp = 5
            msg_send = generate_msg(0, roomtp, msg)
            aclient.sendmsg(msg_send)
            sg.cprint(
                (userid+" "+time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())+"\n"+msg+"\n"),
                c=("#000000", bg_color_me),
            )
            window["-INPUT-"].update("")

        #click the botton "Who are here?"
        if event == "-ANYONE-":
            msg_send = generate_msg(2, 0, 1)
            aclient.sendmsg(msg_send)

        #click to start the file transfer service
        if event == "-FILE-":
            if fltransfer == 0:
                sg.cprint(
                    f"Go into the file transfer successfully!\n",
                    c=("#000000", bg_color_sys),
                )
                fltransfer = 1
                sg.popup("File Transfer haven't be achieved yet.\n")
                fltransfer = 0
            
            else:
                sg.cprint(
                    f"You have open a File Transfer\n",
                    c=("#000000", bg_color_sys),
                )
            
    window.close()
    sys.exit()

if __name__ == "__main__":
    main()
