messagetype = {
    0: "normal message",
    1: "connection",
    2: "askstatus",
    3: "filetransfer"
}

roomtype = {
    0: "Square",
    1: "Alice",
    2: "Bob",
    3: "Carol",
    4: "Dave",
    5: "Eve",
}

def analysis_msg(msg):
    msgtype = int(msg[0])
    roomid = int(msg[1])
    msgctt = msg[2:]
    return msgtype, roomid, msgctt

def getmsgtype(msg):
    return msg[0]

def generate_msg(msgtype, room, msgctt):
    msg = str(msgtype)+str(room)+str(msgctt)
    return msg

