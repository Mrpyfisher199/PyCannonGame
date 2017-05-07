#!/usr/bin/python
#coding: latin-1
import socket, curses, signal, time,os
cwd = os.getcwd()
signal.signal(signal.SIGTSTP, signal.SIG_IGN)
port = 5000
try:
	users=open(cwd+'/Users.txt').readlines()
except Exception as e:
	users=open(cwd+'/Users.txt', 'a')
	users.close()
	users=open(cwd+'/Users.txt').readlines()
for ii,i in enumerate(users):
	users[ii]=i.strip('\n').split(':')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host=s.getsockname()[0]
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
print 'Hosting On: '+host+':'+str(port)
jhg=raw_input('Enter Any Key to Continue\n> ')
s.settimeout(0.01)
def end(s):
	s.close()
def Main(s, users):
	try:
		waitfor={}
		waiter=[]
		fight=[]
		waitfor1={}
		clientyuser={}
		while 1:
			try:
				data, addr = s.recvfrom(1024)
				if str(data) == 'q':
					try:
						del clientyuser[addr]
					except Exception as e:
						pass
					try:
						del waitfor[addr]
					except Exception:
						pass
					try:
						del waitfor1[addr]
					except Exception as e:
						pass
					try:
						del waiter[waiter.index(addr)]
					except Exception:
						pass
				elif str(data) == 'fig' and addr not in waiter:
					waiter.append(addr)
				elif str(data) == 'fig' and addr in waiter:
					waiter.remove(addr)
				elif str(data) == 'join' and addr not in waitfor:
					waitfor[addr]=''
				elif addr in waitfor and waitfor[addr]=='':
					for i in users:
						if i[0] == str(data):
							waitfor[addr]=i
							s.sendto('uhgur', addr)
							break
					else:
						s.sendto('True', addr)
				elif addr in waitfor and len(waitfor[addr])==3:
					if str(data) == waitfor[addr][1]:
						s.sendto(waitfor[addr][2], addr)
						clientyuser[addr]=[waitfor[addr][0], waitfor[addr][1],waitfor[addr][2]]
						del waitfor[addr]
					else:
						s.sendto('True', addr)
						clientyuser[addr]=[waitfor[addr][0], waitfor[addr][1]]
						del waitfor[addr]
				elif str(data) == 'Join' and addr not in waitfor1:
					waitfor1[addr]=''
				elif addr in waitfor1 and len(waitfor1[addr])==1:
					waitfor1[addr].append(str(data))
					waitfor1[addr].append('10;5;10')
					users=open('Users.txt', 'a')
					txtx=':'.join(waitfor1[addr])
					users.write(txtx+'\n')
					users.close()
					users=open('Users.txt').readlines()
					for ii,i in enumerate(users):
						users[ii]=i.strip('\n').split(':')
					clientyuser[addr]=[waitfor1[addr][0], waitfor1[addr][1], waitfor1[addr][2]]
					del waitfor1[addr]
				elif addr in waitfor1 and waitfor1[addr]=='':
					for i in users:
						print i[0]
						print str(data)
						if i[0] == str(data):
							s.sendto('1', addr)
					else:
						waitfor1[addr]=[str(data)]
						s.sendto('True', addr)
				elif 'up' in str(data):
					userss=open('Users.txt', 'w')
					txtx=':'.join(clientyuser[addr])
					for i in users:
						if i[0] != clientyuser[addr][0]:
							txtx=':'.join(i)
							userss.write(txtx+'\n')
						else:
							txtx=clientyuser[addr][0]+':'+clientyuser[addr][1]+':'+str(data).split(':')[1]
							userss.write(txtx+'\n')
					userss.close()
					users=open('Users.txt').readlines()
					for ii,i in enumerate(users):
						users[ii]=i.strip('\n').split(':')
					for i in users:
						if i[0] == clientyuser[addr][0]:
							nfo=i[2]
					clientyuser[addr]=[clientyuser[addr][0], clientyuser[addr][1], nfo]
				elif str(data) == ' ':
					s.sendto('fish', addr)
				elif str(data) == 'r':
					s.sendto(clientyuser[addr][2], addr)
				elif str(data) == 'hit':
					for i in fight:
						if i[0] == addr:
							s.sendto('hit',i[1])
							break
						if i[1] == addr:
							s.sendto('hit',i[0])
							break
				elif str(data) == 'endw':
					for ii,i in enumerate(fight):
						if addr in i:
							del fight[ii]
							break
				if len(waiter) > 1:
					for ii,i in enumerate(waiter):
						if ii % 2 == 0:
							lts=i
						else:
							waiter.remove(lts)
							waiter.remove(i)
							fight.append([i, lts])
							s.sendto('start:'+clientyuser[lts][2].split(';')[0]+';'+clientyuser[lts][2].split(';')[1], i)
							s.sendto('start:'+clientyuser[i][2].split(';')[0]+';'+clientyuser[i][2].split(';')[1], lts)
			except socket.error:
				pass
	except KeyboardInterrupt:
		end(s)
		return
Main(s, users)