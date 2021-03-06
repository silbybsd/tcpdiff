# Copyright (c) 2008-2015, Michael J. Silbersack
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import commands
import os
import signal
import socket
import sys
import time

datasize = 2**16
timeout = 90
sock = None

if os.path.exists('/boot/kernel/netstat'):
	ns_path='/boot/kernel/netstat'
else:
	ns_path='netstat'

def alarm_handler(arg1, arg2):
	print timeout, "second timeout; exiting."
	sys.exit(1)

rv = commands.getstatusoutput("%s -na | grep 10000 | grep LISTEN" % (ns_path))
if rv[0] == 256:
	print "Error, either netstat or the server is not working!"
	sys.exit(1)
signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(timeout)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], 10000))
total = 0
# This hangs sometimes with data in the recv-q - probably
#some sort of MSG_WAITALL bug.  Should set an alarm
#to handle this case.
while total < datasize:
	data = sock.recv(datasize, socket.MSG_WAITALL)
	total += len(data)
print "%s bytes received" % (total)
time.sleep(1)
sock.close()
