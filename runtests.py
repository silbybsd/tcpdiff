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
#
# This program runs the tests to gather tcpdump data
# for analysis by tcpdiff

import commands
import os
import sys
import time

import pexpect

import packetdrops

def setup_me():
	cmd = "sysctl net.inet.ip.dummynet.pipe_slot_limit=150"
	rv = commands.getstatusoutput(cmd)
	print cmd, rv

def setup_dut():
	# Disable inflight, it may make results unpredictable.
	cmd = '"sysctl net.inet.tcp.inflight.enable=0 ; sysctl net.inet.tcp.hostcache.prune=1 ; sysctl net.inet.tcp.hostcache.purge=1 ; sysctl net.inet.tcp.sendspace=512000; sysctl net.inet.tcp.recvspace=512000; sysctl kern.ipc.maxsockbuf=1000000; sysctl net.inet.tcp.delayed_ack=1"'
	rv = commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	cmd = 'scp -r serversend root@%s:' % (dut['mgmt_ip'])
        rv = commands.getstatusoutput(cmd)
	cmd = 'scp -r clientsend root@%s:' % (dut['mgmt_ip'])
        rv = commands.getstatusoutput(cmd)
	# Have to loop until the hostcache has been purged.  This should
	# only take a second, but it may take up to 300 seconds if the system
	# was just booted.
	while True:
		cmd = "sysctl net.inet.tcp.hostcache.purge"
		rv = commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
		if rv == (0, 'net.inet.tcp.hostcache.purge: 0'):
			break
		time.sleep(1)
		print "Waiting for hostcache to purge"
	# Grab and log the uname
	cmd = 'uname -a'
	rv = commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	unamefile = "%s/uname.txt" % (testname)
	fh = open(unamefile, "w")
	fh.write(rv[1])

def update_dut():
	cmd = "sysctl net.inet.tcp.delayed_ack=0"
	rv = commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))

def setup_packetloss(losspattern):
	if str(losspattern[0]) == '0':
		cmd = "ipfw pipe 1 config queue 150"
	else:
		cmd = "ipfw pipe 1 config queue 150 pls %s" % (losspattern[0])
        rv = commands.getstatusoutput(cmd)
	cmd = "ipfw pipe 1 zero"
        rv = commands.getstatusoutput(cmd)
	if str(losspattern[1]) == '0':
		cmd = "ipfw pipe 2 config queue 150"
	else:
		cmd = "ipfw pipe 2 config queue 150 pls %s" % (losspattern[1])
        rv = commands.getstatusoutput(cmd)
	cmd = "ipfw pipe 2 zero"
        rv = commands.getstatusoutput(cmd)
	cmd = "ipfw pipe 3 zero"
        rv = commands.getstatusoutput(cmd)

def report_packetloss(losspattern):
	cmd = "ipfw pipe show > %s/%s.loss" % (testname, losspattern)
        rv = commands.getstatusoutput(cmd)
	print cmd, rv

def start_tcpdump(losspattern):
	cmd = "daemon -f tcpdump -p -n -i em2 -U -w %s/%s%%em2.pcap" % (testname, losspattern)
        rv = commands.getstatusoutput(cmd)
	print cmd, rv
	cmd = "daemon -f tcpdump -p -n -i em1 -U -w %s/%s%%em1.pcap" % (testname, losspattern)
        rv = commands.getstatusoutput(cmd)
	print cmd, rv

def stop_tcpdump():
	cmd = "sleep 1 ; killall tcpdump"
        rv = commands.getstatusoutput(cmd)

def reset_dut():
	cmd = "sysctl net.inet.tcp.hostcache.purge=1"
	commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	# Sleep 1 second for this to take effect.
	time.sleep(1)
	

def setup_serversend():
	# Ping from the host to make sure all arp caches are ready to go
	cmd = "ping -c 2 %s" % (dut['loop_ip'])
	print commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	cmd = "killall python"
	commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	cmd = "daemon -f python serversend/server.py"
	commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	# Sleep 1 second for this to take effect.
	time.sleep(1)

def run_serversend():
	cmd = "python serversend/clientwrapper.py %s" % (dut['loop_ip'])
	rv = commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	print rv

if len(sys.argv) != 3:
	print "Please provide a system to test and a path to store the results in"
	sys.exit(1)

settings = eval(open("testhosts").read())

dut_name = sys.argv[1]
dut = settings.get(dut_name)

testname = sys.argv[2]

if not dut:
	print "System to test not found"
	sys.exit(1)

setup_me()

os.mkdir(testname)
drops = packetdrops.dual_packetpattern(30, 50)
drops.extend(packetdrops.multidrop_packetpattern())

setup_dut()
print "Setup of %s complete" % (dut_name)
setup_packetloss(('0', '0'))
setup_serversend()
for drop in drops:
	start_tcpdump("%s_%s" % (drop[0], drop[1]))
	setup_packetloss(drop)
	reset_dut()
	run_serversend()
	report_packetloss("%s_%s" % (drop[0], drop[1]))
	stop_tcpdump()
update_dut()
setup_packetloss(('0', '0'))
setup_serversend()
print "Running some tests with delayed acks off"
drops = packetdrops.multidrop_packetpattern()
for drop in drops:
	start_tcpdump("%s_%s_nodelay" % (drop[0], drop[1]))
	setup_packetloss(drop)
	reset_dut()
	run_serversend()
	report_packetloss("%s_%s_nodelay" % (drop[0], drop[1]))
	stop_tcpdump()
