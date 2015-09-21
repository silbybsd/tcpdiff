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
# This program generates the different packet drop patterns, given
# the length of the targetted connection in packets

def double_drop(a, b):
	p = []
	for x in xrange(a, b):
		for y in xrange(x + 1, b):
			p.append([x, y])
	return p

def triple_drop(a, b):
	p = []
	for x in xrange(a, b):
		for y in xrange(x + 1, b):
			for z in xrange(y + 1, b):
				p.append([x, y, z])
	return p

def packetpattern(begin, end):
	patterns = []

	# Single packet drops
	for x in xrange(begin, end):
		patterns.append(str(x))

	"""
	# Double packet drop patterns
	patterns.extend(double_drop(1, ends))
	patterns.extend(double_drop(count - ends, count))

	patterns.extend(triple_drop(1, ends))
	patterns.extend(triple_drop(count - ends, count))
	"""

	return patterns

def dual_packetpattern(countA, countB):
	dual_pattern = set()
	patternA = packetpattern(0, 5)
	for pattern in patternA:
		dual_pattern.add((pattern, '0'))
	patternB = packetpattern(0, 5)
	for pattern in patternA:
		dual_pattern.add(('0', pattern))
	for patA in patternA:
		for patB in patternB:
			dual_pattern.add((patA, patB))
	patternA = packetpattern(countA - 6, countA)
	for pattern in patternA:
		dual_pattern.add((pattern, '0'))
	patternB = packetpattern(countB - 6, countB)
	for pattern in patternB:
		dual_pattern.add(('0', pattern))
	for patA in patternA:
		for patB in patternB:
			dual_pattern.add((patA, patB))
	listver = list(dual_pattern)
	listver.sort()
	return listver

def multidrop_packetpattern():
	listver = list()
	listver.extend([('0', '24'), ('0', '24,25'), ('0', '24,25,26')])
	listver.extend([('0', '24,25,26,27'), ('0', '24,25,26,27,28')])
	listver.extend([('0', '24,25,26,27,28,29'), ('0', '24,25,26,27,28,29,30')])
	"""	
	listver.extend([('0', '24,25,26,27,28,29,30,31'), ('0', '24,25,26,27,28,29,30,31,32')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33'), ('0', '24,25,26,27,28,29,30,31,32,33,34')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35'), ('0', '24,25,26,27,28,29,30,31,32,33,34,35,36')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57')])
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58')])
	"""	
	listver.extend([('0', '24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59')])
	return listver

