messagetype = {
    0: "normal message",
    1: "connection",
    2: "change name"
}

roomtype = {
    0: "Square",
    1: "Private Room 1",
    2: "Private Room 2",
    3: "Private Room 3",
    4: "Private Room 4",
    5: "Private Room 5",
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

