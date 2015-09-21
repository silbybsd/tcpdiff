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

if len(sys.argv) != 2:
	print "Please provide a system to test"
	sys.exit(1)

settings = eval(open("testhosts").read())
settings2 = eval(open("testsettings").read())

dut_name = sys.argv[1]
dut = settings.get(dut_name)

if not dut:
	print "System to test not found"
	sys.exit(1)

# Set up the local directory heirarchy

if not os.path.isdir('results'):
	os.mkdir('results')

tested = os.listdir('results')
tested = set(tested)

# Get the list of kernels to test
cmd = "ls %s/*.tar.bz2" % (dut['kernel_path'])
rv = commands.getstatusoutput("ssh root@%s %s" % (dut['pxe_host'], cmd))
kernels = rv[1].split()
kernels = [x.split('/')[-1] for x in kernels]
kernels = [x.split('.tar.bz2')[0] for x in kernels]
kernels = set(kernels)

kernels = list(kernels - tested)
kernels.sort()
print "kernels to test:", kernels

for kernel in kernels:
	time.sleep(5)
	print "Setting up for test of kernel %s" % (kernel)
	"""
	cmd = "vmware-cmd -H %s -U %s -P %s %s stop hard" % (settings2['vmware_host'], settings2['vmware_user'], settings2['vmware_password'], dut['vmware_path'])
	rv = commands.getstatusoutput("ssh a@%s %s" % (settings2['rcli_host'], cmd))
	print cmd, rv
	"""
	cmd = "rm -rf %s/boot/kernel" % (dut['pxe_path'])
	rv = commands.getstatusoutput("ssh root@%s %s" % (dut['pxe_host'], cmd))
	print cmd, rv
	cmd = "tar xf %s/%s.tar.bz2 --strip-components 2 -C %s/boot" % (dut['kernel_path'], kernel, dut['pxe_path'])
	rv = commands.getstatusoutput("ssh root@%s %s" % (dut['pxe_host'], cmd))
	print cmd, rv
	"""
	cmd = "vmware-cmd -H %s -U %s -P %s %s start hard" % (settings2['vmware_host'], settings2['vmware_user'], settings2['vmware_password'], dut['vmware_path'])
	rv = commands.getstatusoutput("ssh a@%s %s" % (settings2['rcli_host'], cmd))
	print cmd, rv
	"""
	cmd = "shutdown -r now"
	rv = commands.getstatusoutput("ssh root@%s %s" % (dut['mgmt_ip'], cmd))
	time.sleep(80)
	# Create the directory for the test results to go in
	os.mkdir('results/%s' % (kernel))

	# Prime the arp cache
	cmd = "ping -q -c 1 %s" % (dut['mgmt_ip'])
	rv = commands.getstatusoutput(cmd)

	# Verify that the host is up	
	cmd = "ping -q -c 1 %s" % (dut['mgmt_ip'])
	rv = commands.getstatusoutput(cmd)
	if rv[0] != 0:
		print "Kernel %s failed to boot" % (kernel)
		open('results/%s/failed.txt' % (kernel), 'w')
		continue
	
	print "Running test 1 of %s" % (kernel)
	cmd = "python runtests.py %s results/%s/1" % (dut_name, kernel)
	rv = os.system(cmd)
	time.sleep(15)
	print "Running test 2 of %s" % (kernel)
	cmd = "python runtests.py %s results/%s/2" % (dut_name, kernel)
	rv = os.system(cmd)
	time.sleep(15)
	print "Running test 3 of %s" % (kernel)
	cmd = "python runtests.py %s results/%s/3" % (dut_name, kernel)
	rv = os.system(cmd)
print "All kernels tested"
