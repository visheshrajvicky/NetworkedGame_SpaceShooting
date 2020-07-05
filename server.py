import socket                
from _thread import *
import random
import hashlib
#from player import Player
import pygame
from os import path

server = "127.0.0.1"
port = 12345
s = socket.socket()          
print ("Socket successfully created")              
  
try:
	s.bind((server, port))         
	print ("socket binded to %s" %(port)) 
except socket.error as e:
    str(e)

s.listen(2)      
print ("socket is listening")

def check_if_string_in_file(file_name,string_to_search):
	with open(file_name, "r") as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return True
	return False

def add_new_user(file_name, user_info):
	f = open(file_name,"a")
	print(user_info)
	f.write("\n")
	f.write(user_info)
	f.close()
	return True

#print(check_if_string_in_file("user_detail.txt","vishesh 372021838013568126"))


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])
#def mob(c):
#	return c.send(str(random.randrange(-100, -40))+","+str(random.randrange(1, 8))+","+str(random.randrange(400-112)))
pos = [(240,590),(100,590)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player]) + "," + "Null"))
    reply = ""
    '''if player == 0:
    	c1 = addr_lst[0]
    	print(c1)
    elif player == 1:
    	c2 = addr_lst[1]
    	print(c2)'''
    while True:
        try:
            bullet = ""
            data = conn.recv(2048).decode()
            if data == "shoot":
                bullet = "shoot"
                print("Bullet shots by Player ", player)
                '''if player == 0:
        	    	c2.send("True")
        	    elif player == 1:
        	    	c1.send("True")'''
            else:
                bullet = "shoot"
                data = read_pos(data)
                #data = read_pos(conn.recv(2048).decode())
                pos[player] = data
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received Position for Player : ", player , data)
                print("Sending Position for Player : ", player, reply)
                #print(reply+","+str(random.randrange(-100, -40)))
            #print(bullet)
            conn.sendall(str.encode(make_pos(reply) + "," + bullet))
        except:
            break

    print("Lost connection")
    conn.close()

addr_lst = []
currentPlayer = 0
while True:
	c,addr = s.accept()
	addr_lst.append(c)
	print("Got connection from", addr)

	#print(addr_lst)

	auth = True
	while auth:
		mesg = c.recv(1024).decode("utf-8")
		#print(mesg)
		user_info = mesg.split()
		#print(user_info)
		if(user_info[0] == "1"):
			pswd = user_info[2].encode('utf-8')
			string = user_info[1] +" "+hashlib.sha256(pswd).hexdigest()
			c.send(str(add_new_user("user_detail.txt", string)).encode("utf-8"))
		elif(user_info[0] == "2"):
			pswd = user_info[2].encode('utf-8')
			string = user_info[1] +" "+hashlib.sha256(pswd).hexdigest()
			print(string)
			check = check_if_string_in_file("user_detail.txt", string)
			c.send(str(check).encode("utf-8"))
			if check == False:
				continue
			else:
				auth = False

	start_new_thread(threaded_client,(c, currentPlayer))
	currentPlayer +=1
