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
import glob
import os
import shutil
import sys

directory = sys.argv[1]
directory2 = sys.argv[2]
files = glob.glob("%s/*.processed" % (directory))
files.sort()
total = 0
changed = 0
unchanged = 0
for file in files:
	total += 1
	filepart = file.split(directory)[1]
	dirpart = file.split("/")[0]
	packetpart = filepart.split(".")[0]
	packetpart2 = packetpart + "%em1.pcap.txt"
	rv = commands.getstatusoutput("diff -u %s/%s %s/%s" % (directory, filepart, directory2, filepart))
	if rv[0] != 0:
		rv = commands.getstatusoutput("tkdiff -u %s/%s %s/%s" % (directory, filepart, directory2, filepart))
		changed += 1
		print "Differences found in", packetpart
	else:
		unchanged += 1
print "%s total files, %s changed, %s unchanged" % (total, changed, unchanged)

