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
# This program normalizes tcpdump output

import pprint
import sys

def normalize_isns(lines):
	isnA = None
	isnB = None
	for line in lines:
		if line.find("client > server: S") > 0:
			fields = line.split()
			isnA = fields[6].split(":")[0]
			break

	for line in lines:
		if line.find("server > client: S") > 0:
			fields = line.split()
			isnB = fields[6].split(":")[0]
			isnC = fields[8]
			break
	if isnA and isnB:
		newlines = []
		isnAbefore = "client > server: S %s:%s" % (isnA, isnA)
		isnAafter  = "client > server: S 0:0"
		isnBbefore = "server > client: S %s:%s(0) ack %s" % (isnB, isnB, isnC)
		isnBafter  = "server > client: S 0:0(0) ack 0"
		for line in lines:
			line = line.replace(isnAbefore, isnAafter)
			line = line.replace(isnBbefore, isnBafter)
			newlines.append(line)
		lines = newlines
	return lines

def normalize_ips(lines):
	# Turn IP/port into client and server, remove packets
	# not from this connection.
	for line in lines:
		fields = line.split()
		if fields[5].find('S') == 0:
			ipA = fields[2]
			ipB = fields[4]
			ipB = ipB[:-1]
			portA = ipA.split(".")[-1]
			portB = ipB.split(".")[-1]
			break
	else:
		print "Could not find a syn packet!"
		sys.exit(-1)
	newlines = []
	for line in lines:
		line = line.replace(ipA, 'client')
		line = line.replace(ipB, 'server')
		if not (line.find('client > server') > 0 or line.find('server > client') > 0):
			print "Found extra packet in the stream, aborting!"
			sys.exit(1)
		newlines.append(line)
	return newlines

def normalize_timestamps(lines):
	fields = lines[0].split('timestamp')
	fields = fields[1].split('>')
	fields = fields[0].split()
	clientTS = int(fields[0])
	fields = lines[1].split('timestamp')
	fields = fields[1].split('>')
	fields = fields[0].split()
	serverTS = int(fields[0])

	newlines = []
	for line in lines:
		if line.find('timestamp') == -1:
			newlines.append(line)
			continue
		fields = line.split('timestamp')
		fields = fields[1].split()
		tsA = int(fields[0])
		tsB = int(fields[1][:-1])
		if line.find('client > server') != -1:
			newtsA = tsA - clientTS
			if tsB != 0:
				newtsB = tsB - serverTS
			else:
				newtsB = tsB
		else:
			newtsA = tsA - serverTS
			newtsB = tsB - clientTS
		line = line.replace(str(tsA), str(newtsA))
		line = line.replace(str(tsB), str(newtsB))
		newlines.append(line)
	return newlines

def strip_timestamps(lines):
	newlines = []
	for line in lines:
		if line.find('timestamp') == -1:
			newlines.append(line)
			continue
		options = line.split('<')[1].split('>')[0].split(',')
		for opt in options:
			if opt.startswith('timestamp'):
				line = line.replace(opt, 'timestamp 0 0')
				break
		newlines.append(line)
	return newlines

def normalize_time(lines):
	newlines = []
	for line in lines:
		fields = line.split('IP')
		thistime = int(fields[0].replace('. ', ''))
		thistime = thistime - (thistime % 10000)
		thistime = float(thistime) / 1000000
		line = "%s IP%s" % (thistime, fields[1])
		newlines.append(line)
	return newlines

def strip_time(lines):
	newlines = []
	for line in lines:
		fields = line.split('IP')
		line = "00:00:00.000000 IP%s" % (fields[1])
		newlines.append(line)
	return newlines

if len(sys.argv) != 3:
	print "Please provide a file to normalize"
	sys.exit(1)

file = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')
lines = file.readlines()

lines = normalize_ips(lines)
# Just strip timestamps for now; timestamps differ based on tick
# rate and other things and should be checked last.
lines = strip_timestamps(lines)
lines = normalize_time(lines)
lines = normalize_isns(lines)
for line in lines:
	outfile.write(line)
