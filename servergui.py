from TCPserver import sever
import PySimpleGUI as sg
from threading import Thread
import sys

def main():
    asever = sever()
    sg.theme("Black")

    layout = [
        [sg.Titlebar("Chat Server")],
        [sg.Text("Network Log")],
        [
            sg.Multiline(
                "Server Side Network Sniffing!\n\n",
                font="Franklin 11",
                no_scrollbar=True,
                size=(120, 30),
                horizontal_scroll=True,
                echo_stdout_stderr=True,
                reroute_stdout=True,
                # write_only=True,
                reroute_cprint=True,
                disabled=True,
                autoscroll=True,
                key="-OUTPUT-",
            ),
        ],
        [
            sg.Button("Status", key="-GET_STATUS-"),
            sg.Push(),
            sg.Button("Save Log As...", key="-SAVE_LOG-"),
            sg.Text(" "),
            sg.Button("Exit", size=(12, 1), key="-EXIT-"),
        ],
    ]

    window = sg.Window("", layout, finalize=True)
    sg.cprint_set_output_destination(window, "-OUTPUT-")

    #start the service
    Thread(target=asever.connect, args=(), daemon=True).start()

    while True:
        event, values = window.read()
        if event in [sg.WIN_CLOSED, "-EXIT-"]:
            break
        if event == "-GET_STATUS-":
            for i in asever.clients:
                sg.cprint(asever.cAccount[i])

    window.close()
    sys.exit()

if __name__ == "__main__":
    main()
