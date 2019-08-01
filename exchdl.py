#!/usr/bin/env python3
import subprocess
import json
import sys
from _thread import start_new_thread as thread
from threading import Semaphore
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("<IP address>", username = "<username>", key_filename = "<filepath>")

MAX_THREADS = 10
MAX_INTERNAL_THREADS = 10
MAX_CONNECTIONS = 4

threadlock = Semaphore(MAX_THREADS)
connectionlock = Semaphore(MAX_CONNECTIONS)
error = False

def search(query):
	global ssh, connectionlock, error

	connectionlock.acquire()
	try: channel = ssh.get_transport().open_session()
	except: error = True; exit(1)
	channel.exec_command('/bin/bash -c cat /dev/stdin | xargs -I{} /opt/ldap/ldapsearch -LLL -E pr=1000/noprompt -H <dc_hostname> -D "CN=<the user who query the DC>,OU=<OUinfo1>,OU=<OUinfo2>,OU=<OUinfo3>,OU=<OUinfo4>,DC=<domain>,DC=<domain2>" -b "DC=<domain>,DC=<domain2>" -o ldif-wrap=no -w "<password>" "{}"')
	channel.sendall(query.encode() + b"\n")
	channel.shutdown_write()
	data = b""
	while 1:
		_in = channel.recv(8192)
		if not len(_in): break
		data += _in

	o = data.decode().replace("\r\n", "\n").split("\n\n")
	channel.recv_exit_status()
	channel.close()
	connectionlock.release()

	
	results = []
	for e in o:
		if e.startswith("#"): break
		e = e.split("\n")
		obj = {
			"member": [],
		}
		for _ in e:
			_ = _.split(": ", 1)
			if _[0] == "member":
				obj["member"].append(_[1])
			else:
				try: obj[_[0]] = _[1]
				except Exception as e_:
					print(_, file = sys.stderr)
					print(e_, file = sys.stderr)
		results.append(obj)
	return results

def _search(internallock, out, m):
	cn = m[3:].replace("\\,", ",").split(",OU=", 1)[0]
	res = search('(cn="%s")' % (cn, ))
	if len(res) != 1: exit(1)
	try: out.append(res[0]["mail"])
	except:
		print(cn, res[0], file = sys.stderr)
		raise
	internallock.release()

def expand(mail):
	global MAX_INTERNAL_THREADS, error
	results = search('mail="%s"' % (mail,))
	if len(results) == 0 or results[0]["objectClass"] != "group": return [mail]

	members = results[0]["member"]
	out = []
	ilock = Semaphore(MAX_INTERNAL_THREADS)
	for m in members:
		if not m.startswith("CN="): exit(1)
		ilock.acquire()
		thread(_search, (ilock, out, m))

	for _ in range(MAX_INTERNAL_THREADS):
		if error: break
		ilock.acquire()
	for _ in range(MAX_INTERNAL_THREADS): ilock.release()

	return out

mails = sys.argv[1].split(" ")
out = []

def _thread(m):
	global out, threadlock
	m = expand(m)
	out += m
	threadlock.release()

for m in mails:
	threadlock.acquire()
	thread(_thread, (m,))

for _ in range(MAX_THREADS):
	if error: break
	threadlock.acquire()
for _ in range(MAX_THREADS): threadlock.release()

if not error: print(" ".join(out), end = "", flush = True)

ssh.close()
if error: exit(255)
