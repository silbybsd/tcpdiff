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

if os.path.exists('/boot/kernel/netstat'):
	ns_path='/boot/kernel/netstat'
else:
	ns_path='netstat'

def wait_for_fin_wait():
	# Loop for up to 90 seconds waiting for FIN_WAIT sockets and
	# friends to clear out.
	loops = 0
	while loops < (120 * 2):
		rv = commands.getstatusoutput("%s -na | grep 10000 | grep -v TIME_WAIT | grep -v LISTEN" % (ns_path))
		if rv[0] == 256:
			break
		else:
			time.sleep(.5)
			loops += 1
 
	print "%s loops " % (loops)

rv = commands.getstatusoutput("python serversend/client.py %s" % (sys.argv[1]))
wait_for_fin_wait()
print rv[1]
sys.exit(rv[0])
