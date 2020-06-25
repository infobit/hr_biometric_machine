import sys
from zklib import zklib
from zklib import zkconst
from zklib import zkuser

zk = zklib.ZKLib("192.168.188.204", 4370)
ret = zk.connect()
print ("connection:", ret)
if ret:
	print ("conectado a 192.168.188.204 ...")
	zk.disableDevice()
	print ("asistencias")
	att = zk.getsAtt("192.168.188.204:80")
	for at in att:
		print (at)
	print ("getAttendace")
	print ("desconectando...")
	zk.enableDevice()

"""zk = zklib.ZKLib("88.27.241.15", 4370)
ret = zk.connect()
print "connection:", ret
if ret:
	print "conectado a 88.27.241.15..."
	zk.disableDevice()
	print "asistencias"
	att = zk.getsAtt("88.27.241.15:81")
	for at in att:
		print at
	print "getAttendace"
	print "desconectando..."
	zk.enableDevice()"""
