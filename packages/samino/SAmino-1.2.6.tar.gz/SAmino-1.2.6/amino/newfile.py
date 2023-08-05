import amino
from amino.Local import LocalClient
import os


num = 0
lines = []
c = amino.GlobalClient('', '')
email = input('email : ')
password = input('password : ')
com = input('chat or blog url from community : ')
print("paste your message here :\n\nif you finish type : /end")

while True:
    line = input()
    if line.strip() == "/end":
        break
    else:
        lines.append(line)

message = "\n".join(lines)
message = message.strip()

login = c.login(email, password)
link = c.get_from_link(com)
client = amino.LocalClient('x'+str(link.ndcId), login.sid, login.uid)
client2 = LocalClient('x'+str(link.ndcId), login.sid, login.uid)
#http://aminoapps.com/p/pml2jk
os.system('clear')

while True:
    onlineList = client.get_online_members(start=num, size=100)
    for userId, name in zip(onlineList.uid, onlineList.nickname):
        s = client2.start_chat(userId=[userId, login.uid], message=message, title='مهم!!!')
        print(s.apiMessage)
    num = num + 100