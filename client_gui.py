from threading import Thread
import time
import sys
from utils import *
import string

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



def main():
    aclient = client()

    userid = "nobody"
    cncted = 0 #make sure only connect once

    #the gui of client
    sg.theme("BlueMono")
    #roomid = "test"
    layout = [
        [sg.Titlebar("Chat Client")],
        [
            sg.Text(
                f"Nickname: {userid}", font="Franklin 12 bold", text_color="blue"
            ),
            sg.Push(),
            sg.Combo(  # sg.Combo sg.OptionMenu
                [
                    "Square",
                    "Private Room 1",
                    "Private Room 2",
                    "Private Room 3",
                    "Private Room 4",
                    "Private Room 5",
                ],
                font="Franklin 12",
                size=(13, 10),
                default_value="Square",
                enable_events=True,
                readonly=True,
                background_color='#FFFFFF',
                key="-ROOMS_OPTION-",
            ),
         ],
        #the output 
        [
            sg.Multiline(
                f" Hello {userid}!\n Welcome to the cwym chat!\n\n",
                font="Franklin 11",
                no_scrollbar=True,
                size=(50, 20),
                text_color="black",
                # background_color=rooms_color[current_room_name],
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
            sg.Push(),
            # sg.Button("Save Chat As...", key="-SAVE_LOG-"),
            sg.Button("Exit", size=(12, 1), key="-EXIT-"),
        ],
    ]
    window = sg.Window("", layout, finalize=True)
    sg.cprint_set_output_destination(window, "-OUTPUT-")

    #init receive thread
    Thread(target=receive, args=(aclient.clientSocket, window), daemon=True).start()

    while True:
        event, values = window.read()

        if event in [sg.WIN_CLOSED, "-EXIT-"]:
            break
        
        if event == "-RECEIVE-":
            val = values[event]
            clock = val[0]
            msgtp = val[1] #the type of the message
            room = val[2]
            msg = val[3]
            bg_color = "#ffd258"
            # sg.cprint(
            #             f"{msg}\n",
            #             c=("#000000", bg_color),
            #         )
            if messagetype[msgtp] == "normal message":
                if roomtype[room] == "Square" or roomtype[room] == values["-ROOMS_OPTION-"]:
                    sg.cprint(
                        f"{msg}\n",
                        c=("#000000", bg_color),
                    )
            if messagetype[msgtp] == "connection":
                if cncted == 0:
                    cncted = 1
                    userid = msg       

        if event == "-SEND-":
            msg = f"{values['-INPUT-']}"
            room = values["-ROOMS_OPTION-"]
            if room == "Square":
                roomtp = 0
            else:
                roomtp = int(room[-1])
            msg_send = generate_msg(0, 0, msg)
            aclient.sendmsg(msg_send)
            bg_color = "#66FFFF"
            sg.cprint(
                (userid+time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())+"\n"+msg+"\n"),
                c=("#000000", bg_color),
            )
            window["-INPUT-"].update("")

    window.close()
    sys.exit()

if __name__ == "__main__":
    main()
