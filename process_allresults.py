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

import os
import sys

if len(sys.argv) != 2:
        print "Please provide a directory to process"
        sys.exit(1)

l1 = os.listdir(sys.argv[1])
l1a = []
for path in l1:
	path = os.path.join(sys.argv[1], path)
	if os.path.isdir(path):
		l1a.insert(0, path)
l2 = []
for path in l1a:
	l2temp = os.listdir(path)
	for path_2 in l2temp:
		path_2 = os.path.join(path, path_2)
		if os.path.isdir(path_2):
			l2.insert(0, path_2)

l3 = []
for path in l2:
	if not os.path.exists(os.path.join(path, "0_0.loss")):
		continue
	if os.path.exists(os.path.join(path, "0_0.client.processed")):
		print "Skipping %s, already processed" % (path)
		continue
	l3.insert(0, path)

for path in l3:
	print "Processing %s" % (path)
	os.system('python process.py %s' % (path))
