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
import copy
import glob
import os
import shutil
import sys
import pprint

directory = sys.argv[1]
files = glob.glob("%s/*.pcap" % (directory))
for file in files:
	rv = commands.getstatusoutput("./tcpdump -ttt -n -r %s ip > %s.txt" % (file, file))
	rv = commands.getstatusoutput("python normalize.py %s.txt %s.norm" % (file, file))
	if rv[1] or rv[0] != 0:
		print rv
		print "Problem with file %s, aborting" % (file)
		sys.exit(1)
	rv = commands.getstatusoutput('grep "client > server" %s.norm > %s.client' % (file, file))
	rv = commands.getstatusoutput('grep "server > client" %s.norm > %s.server' % (file, file))

files = glob.glob("%s/*.loss" % (directory))
basenames = []
for file in files:
	file = file.split(".loss")[0]
	lossparts = file.split('/')[-1]
	lossparts = lossparts.split('_')
	client_loss = lossparts[0].split(',')
	server_loss = lossparts[1].split(',')
	basenames.append((file, client_loss, server_loss))

for file, client_loss, server_loss in basenames:
	def diff_file(a, b, c, loss):
		# Swap around so the A file is the pre-dropped capture
		rv = commands.getstatusoutput('wc -l %s' % (a))
		a_lines = int(rv[1].split()[0])
		rv = commands.getstatusoutput('wc -l %s' % (b))
		b_lines = int(rv[1].split()[0])
		if b_lines > a_lines:
			temp = a
			a = b
			b = temp

		# Preprocess a and b - strip off the timestamps for diffing
		a_tmp = a + '.tmp'
		b_tmp = b + '.tmp'
		fd_a_tmp = open(a_tmp, 'w')
		for line in open(a).readlines():
			parts = line.split("IP")
			fd_a_tmp.write("IP %s" % (parts[1]))
		fd_a_tmp.close()
		fd_b_tmp = open(b_tmp, 'w')
		for line in open(b).readlines():
			parts = line.split("IP")
			fd_b_tmp.write("IP %s" % (parts[1]))
		fd_b_tmp.close()

		a_lines = open(a).readlines()
		b_lines = open(b).readlines()

		truncated_a = copy.copy(a_lines)
		annotated_a = copy.copy(a_lines)
		loss.sort(reverse = True)
		for packetlost in loss:
			packetlost = int(packetlost)
			if packetlost == 0 or packetlost > len(a_lines):
				continue
			annotated_a[packetlost - 1] = annotated_a[packetlost - 1].strip() + " dropped\n"
			truncated_a.pop(packetlost - 1)

		if len(b_lines) != len(truncated_a):
			print a, b
			print "Problem, mismatch between b_lines and truncated_a: %s %s" % (len(b_lines), len(truncated_a))
		else:
			for x in xrange(len(b_lines)):
				if b_lines[x].split('IP')[1] != truncated_a[x].split('IP')[1]:
					print "Problem detected with files", a, b
		fd_c = open(c, 'w')
		for line in annotated_a:
			fd_c.write(line)
		fd_c.close()

		return

		
	file1 = "%s%%em1.pcap" % (file)
	file2 = "%s%%em2.pcap" % (file)
	diff_file(file1 + ".client", file2 + ".client", file + ".client.processed", client_loss)
	diff_file(file1 + ".server", file2 + ".server", file + ".server.processed", server_loss)

