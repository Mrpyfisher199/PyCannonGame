#!/usr/bin/python
#coding: latin-1
import socket, curses, signal, time, sys, os
import getpass;comname = getpass.getuser()
cwd = os.getcwd()
signal.signal(signal.SIGTSTP, signal.SIG_IGN)
file = open(cwd+'/PyCannonGameServer.txt').readlines()
file=file[0].strip('\n').split(':');file[1]=int(file[1]);server=tuple(file)
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(3, curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_WHITE,curses.COLOR_BLACK)
curses.init_pair(5, 9, curses.COLOR_BLACK)
curses.init_pair(6, 227, curses.COLOR_BLACK)
curses.init_pair(7, curses.COLOR_BLACK, 9)
curses.init_pair(8, curses.COLOR_BLACK, 227)
curses.init_pair(9, curses.COLOR_BLACK,curses.COLOR_CYAN)
print "\x1b[8;50;70t"
sl=curses.initscr()
dims = sl.getmaxyx()
window = curses.newwin(dims[0], dims[1], 0, 0)
window.timeout(1)
window.keypad(1)
curses.noecho()
curses.curs_set(0)
window.border(0)
print "\x1b[8;50;70t"
dims = window.getmaxyx()
def end(s, server):
	curses.endwin()
	s.sendto('q', server)
	s.close()
def game(s, server):
	print "\x1b[8;50;70t"
	dims = window.getmaxyx()
	window.erase()
	window.border(0)
	window.addstr(dims[0]/2, dims[1]/2-4, 'Loading...')
	q=window.getch()
	try:
		s.sendto('r', server)
		for i in range(1111):
			try:
				data, addr=s.recvfrom(1024)
				info=str(data).split(';')
				money=int(info[2])
				break
			except Exception as e:
				s.sendto('r', server)
		else:
			while 1:
				window.erase()
				window.border(0)
				window.addstr(dims[0]/2, dims[1]/2-11, '[!] Server is Down!', curses.color_pair(5))
				q=window.getch()
				time.sleep(1)
				end(s, server)
				sys.exit(0)
		gx1=5
		gx2=6
		gx4=6
		while 1:
			window.erase()
			window.border(0)
			window.addstr(1, dims[1]/2-5, ':'.join(info))
			window.addstr(10, 2, 'Hint: To Battle press Enter, To Upgrade Attack press 1 and To Upgrade Your base press 2')
			window.addstr(dims[0]/2-3, 4, 'BBBBBB        A    TTTTTTTTT TTTTTTTTT  L	      EEEEEEE', curses.color_pair(gx1))
			window.addstr(dims[0]/2-2, 4, 'B    B       A A       T	     T      L	      E', curses.color_pair(gx1))
			window.addstr(dims[0]/2-1, 4, 'BBBBBBB     A   A      T	     T	    L	      EEEEEE', curses.color_pair(gx1))
			window.addstr(dims[0]/2-0, 4, 'B      B    AAAAA      T	     T	    L	      E', curses.color_pair(gx1))
			window.addstr(dims[0]/2+1, 4, 'B      B   A     A     T	     T	    L	      E', curses.color_pair(gx1))
			window.addstr(dims[0]/2+2, 4, 'BBBBBBB    A     A     T	     T	    LLLLLLL   EEEEEEE', curses.color_pair(gx1))
			window.addstr(dims[0]/2+15, 6, 'Upgrade Attack', curses.color_pair(gx2))
			window.addstr(dims[0]/2+15, 8+23+2+17, 'Upgrade Base', curses.color_pair(gx4))
			q=window.getch()
			if q == ord('1') and money>=4:
				s.sendto('up'+':'+info[0]+';'+str(int(info[1])+1)+';'+str(money-4), server)
				info[1]=str(int(info[1])+1)
				info[2]=str(int(info[2])-4)
				money=int(info[2])
			elif q == ord('2') and money>=4:
				s.sendto('up'+':'+str(int(info[0])+1)+';'+info[1]+';'+str(money-4), server)
				info[0]=str(int(info[0])+1)
				info[2]=str(int(info[2])-4)
				money=int(info[2])
			elif q == ord('\n'):
				s.sendto('fig', server)
				while 1:
					window.erase()
					window.border(0)
					window.addstr(dims[0]/2, dims[1]/2-10, 'Waiting for opponent...', curses.color_pair(6))
					q=window.getch()
					if q == ord('\n'):
						s.sendto('fig', server)
						break
					try:
						data, addr=s.recvfrom(1024)
						if 'start' == str(data).split(':')[0]:
							nfosa=str(data).split(':')[1]
							health=info[0]
							c=0
							while 1:
								window.erase()
								window.border(0)
								window.addstr(dims[0]/2+10, dims[1]/2-1, '##', curses.color_pair(3))
								window.addstr(dims[0]/2+11, dims[1]/2-1, '##', curses.color_pair(3))
								window.addstr(dims[0]/2+12, dims[1]/2-(len(health+';'+info[1])/2), health+';'+info[1], curses.color_pair(3))
								window.addstr(dims[0]/2-10, dims[1]/2-1, '##', curses.color_pair(5))
								window.addstr(dims[0]/2-11, dims[1]/2-1, '##', curses.color_pair(5))
								window.addstr(dims[0]/2-12, dims[1]/2-(len(str(nfosa))/2), str(nfosa), curses.color_pair(5))
								q=window.getch()
								if int(health)<1:
									window.erase()
									window.border(0)
									window.addstr(dims[0]/2, dims[1]/2-4, 'You Lost!')
									q=window.getch()
									time.sleep(2)
									break
								elif int(nfosa.split(';')[0]) < 1:
									window.erase()
									window.border(0)
									window.addstr(dims[0]/2, dims[1]/2-4, 'You Won!!!', curses.color_pair(6))
									q=window.getch()
									s.sendto('up'+':'+info[0]+';'+info[1]+';'+str(money+2), server)
									info = [info[0],info[1],str(money+2)]
									time.sleep(2)
									s.sendto('endw', server)
									break
								if q == ord('\n'):
									s.sendto('hit', server)
									xs=35
									for i in range(380):
										window.erase()
										window.border(0)
										if i%20==0:
											window.addstr(xs,dims[1]/2-1,'**',curses.color_pair(9))
											xs-=1
										else:
											window.addstr(xs,dims[1]/2-1,'**',curses.color_pair(9))
										window.addstr(dims[0]/2+10, dims[1]/2-1, '##', curses.color_pair(9))
										window.addstr(dims[0]/2+11, dims[1]/2-1, '##', curses.color_pair(9))
										window.addstr(dims[0]/2+12, dims[1]/2-(len(health+';'+info[1])/2), health+';'+info[1], curses.color_pair(3))
										window.addstr(dims[0]/2-10, dims[1]/2-1, '##', curses.color_pair(7))
										window.addstr(dims[0]/2-11, dims[1]/2-1, '##', curses.color_pair(7))
										window.addstr(dims[0]/2-12, dims[1]/2-(len(str(nfosa))/2), str(nfosa), curses.color_pair(5))
										q=window.getch()
									nfosa = str(int(nfosa.split(';')[0])-int(info[1]))+';'+nfosa.split(';')[1]
								try:
									data, addr=s.recvfrom(1024)
									if str(data) == 'hit':
										hlths=health
										health=str(int(health)-int(nfosa.split(';')[1]))
										xs=19
										for i in range(380):
											window.erase()
											window.border(0)
											if i%20==0:
												window.addstr(xs,dims[1]/2-1,'**',curses.color_pair(7))
												xs+=1
											else:
												window.addstr(xs,dims[1]/2-1,'**',curses.color_pair(7))
											window.addstr(dims[0]/2+10, dims[1]/2-1, '##', curses.color_pair(9))
											window.addstr(dims[0]/2+11, dims[1]/2-1, '##', curses.color_pair(9))
											window.addstr(dims[0]/2+12, dims[1]/2-(len(hlths+';'+info[1])/2), hlths+';'+info[1], curses.color_pair(3))
											window.addstr(dims[0]/2-10, dims[1]/2-1, '##', curses.color_pair(7))
											window.addstr(dims[0]/2-11, dims[1]/2-1, '##', curses.color_pair(7))
											window.addstr(dims[0]/2-12, dims[1]/2-(len(str(nfosa))/2), str(nfosa), curses.color_pair(5))
											q=window.getch()
								except Exception:
									pass

							break
					except Exception as e:
						pass
	except KeyboardInterrupt:
		end(s, server)
		sys.exit(0)
def login(s, server):
	print "\x1b[8;50;70t"
	dims=window.getmaxyx()
	try:
		while 1:
			window.erase()
			window.border(0)
			window.addstr(dims[0]/2, dims[1]/2-20, 'Enter 1 to login or enter 2 to create new account.')
			q=window.getch()
			if q == ord('q'):
				end(s, server)
				sys.exit(0)
			elif q == ord('1'):
				s.sendto('join', server)
				name=[]
				while 1:
					window.erase()
					window.border(0)
					window.addstr(dims[0]/2, dims[1]/2-5, 'Enter Name: '+''.join(name))
					q=window.getch()
					if q == 127:
						try:
							name.pop()
						except Exception:
							pass
					elif q != ord('\n') and q < 127 and q > 31 and q != -1:
						try:
							name.append(chr(q))
						except Exception as e:
							pass
					elif q == ord('\n'):
						break
				s.sendto(''.join(name), server)
				for i in range(1111):
					try:
						data, addr=s.recvfrom(1024)
						if str(data) == 'True':
							window.erase()
							window.border(0)
							window.addstr(dims[0]/2, dims[1]/2-10, '[!] Invalid Username! Exiting...', curses.color_pair(5))
							q=window.getch()
							time.sleep(1)
							end(s, server)
							sys.exit(0)
						else:
							break
					except Exception as e:
						s.sendto(''.join(name), server)
				else:
					while 1:
						window.erase()
						window.border(0)
						window.addstr(dims[0]/2, dims[1]/2-11, '[!] Server is Down!', curses.color_pair(5))
						q=window.getch()
						time.sleep(1)
						end(s, server)
						sys.exit(0)
				passs=[]
				while 1:
					window.erase()
					window.border(0)
					window.addstr(dims[0]/2, dims[1]/2-5, 'Enter Password: '+''.join(passs))
					q=window.getch()
					if q == 127:
						try:
							passs.pop()
						except Exception as e:
							pass
					elif q != ord('\n')  and q < 127 and q > 31 and q != -1:
						try:
							passs.append(chr(q))
						except Exception:
							pass
					elif q == ord('\n'):
						break
				s.sendto(''.join(passs), server)
				for i in range(1111):
					try:
						data, addr=s.recvfrom(1024)
						if str(data) == 'True':
							window.erase()
							window.border(0)
							window.addstr(dims[0]/2, dims[1]/2-10, '[!] Wrong Credentials! Exiting...', curses.color_pair(5))
							q=window.getch()
							time.sleep(1)
							end(s, server)
							sys.exit(0)
						else:
							break
					except Exception as e:
						s.sendto(''.join(passs), server)
				else:
					while 1:
						window.erase()
						window.border(0)
						window.addstr(dims[0]/2, dims[1]/2-11, '[!] Server is Down!', curses.color_pair(5))
						q=window.getch()
						time.sleep(1)
						end(s, server)
						sys.exit(0)
				game(s,server)
			elif q == ord('2'):
				s.sendto('Join', server)
				name=[]
				while 1:
					window.erase()
					window.border(0)
					window.addstr(dims[0]/2, dims[1]/2-5, 'Enter Name: '+''.join(name))
					q=window.getch()
					if q == 127:
						try:
							name.pop()
						except Exception:
							pass
					elif q != ord('\n') and q < 127 and q > 31 and q != -1:
						try:
							name.append(chr(q))
						except Exception as e:
							pass
					elif q == ord('\n'):
						break
				s.sendto(''.join(name), server)
				for i in range(1111):
					try:
						data, addr=s.recvfrom(1024)
						if str(data) == 'True':
							break
						elif str(data) == '1':
							window.erase()
							window.border(0)
							window.addstr(dims[0]/2, dims[1]/2-10, '[!] Invalid Username! Exiting...', curses.color_pair(5))
							q=window.getch()
							time.sleep(1)
							end(s, server)
							sys.exit(0)
					except socket.error:
						s.sendto(''.join(name), server)
				else:
					while 1:
						window.erase()
						window.border(0)
						window.addstr(dims[0]/2, dims[1]/2-11, '[!] Server is Down!', curses.color_pair(5))
						q=window.getch()
						time.sleep(1)
						end(s, server)
						sys.exit(0)
				passs=[]
				while 1:
					window.erase()
					window.border(0)
					window.addstr(dims[0]/2, dims[1]/2-5, 'Enter Password: '+''.join(passs))
					q=window.getch()
					if q == 127:
						try:
							passs.pop()
						except Exception:
							pass
					elif q != ord('\n') and q < 127 and q > 31 and q != -1:
						try:
							passs.append(chr(q))
						except Exception:
							pass
					elif q == ord('\n'):
						break
				time.sleep(0.02)
				s.sendto(''.join(passs), server)
				game(s,server)
	except KeyboardInterrupt:
		end(s, server)
		sys.exit(0)
def start(server, dims):
	print "\x1b[8;50;70t"
	dims = window.getmaxyx()
	print "\x1b[8;50;70t"
	dims = window.getmaxyx()
	try:
		host = '0.0.0.0'
		port = 0
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind((host, port))
		s.settimeout(0.01)
		s.sendto(' ', server)
		for i in range(1111):
			window.erase()
			window.border(0)
			window.addstr(dims[0]/2, dims[1]/2-11, '[+] Loading Login Screen...', curses.color_pair(6))
			q=window.getch()
			dims = window.getmaxyx()
			if q == ord('q'):
				end(s, server)
				return
			try:
				data,server=s.recvfrom(1024)
				break
			except Exception as e:
				s.sendto(' ', server)
		else:
			while 1:
				window.erase()
				window.border(0)
				window.addstr(dims[0]/2, dims[1]/2-11, '[!] Server is Down!', curses.color_pair(5))
				q=window.getch()
				time.sleep(1)
				end(s, server)
				return
		login(s, server)
	except KeyboardInterrupt:
		end(s, server)
		return
start(server, dims)