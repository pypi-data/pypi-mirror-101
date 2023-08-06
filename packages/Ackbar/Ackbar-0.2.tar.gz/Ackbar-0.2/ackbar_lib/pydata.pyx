# distutils: language = c++

###############################################################################
#
#	Copyright 2020 Nelson R. Salinas
#
#
#	This file is part of Ackbar.
#
#   Ackbar is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
#	Ackbar is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Ackbar. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


from cython.operator cimport dereference, postincrement

from pydata cimport Mesh
from pydata cimport Solution 

cdef class Meshpy:
	
	cdef Mesh * thismesh
	
	def __cinit__(self, int size, str inname, str threatCat):

		#cdef string n = inname.encode('utf-8')
		#cdef string tc = threatCat.encode('utf-8')
		self.thismesh = new Mesh(size, inname.encode('utf-8'), threatCat.encode('utf-8'))

	def __dealloc__(self):
		del self.thismesh

	def setValue(self, int index, float theVal):
		if index < 0 or index >= self.thismesh.getSize():
			raise IndexError("Index {0} out of range".format(index))
		else:
			self.thismesh.setValue(index, theVal)
		
	def getValue(self, int index):
		if index < 0 or index >= self.thismesh.getSize():
			raise IndexError("Index {0} out of range".format(index))
		else:
			return self.thismesh.getValue(index)

	def getSize(self):
		return self.thismesh.getSize()

	def setName(self, str newName):
		self.thismesh.setName(newName.encode('utf-8'))

	def getName(self):
		nm = self.thismesh.getName()
		return nm.decode('utf-8')
		
	def setRange(self, float newRange):
		self.thismesh.setRange(newRange)

	def getRange(self):
		return self.thismesh.getRange()
		
	def isNull(self):
		return self.thismesh.isNull()

	def nullMe(self):
		self.thisMesh.nullMe()

	def linkNeighs(self, int indexA, int indexB):
		self.thismesh.linkNeighs(indexA, indexB)

	def setThreatStatus(self, str newStatus):
		self.thismesh.setThreatStatus(newStatus.encode('utf-8'))

	def getThreatStatus(self):
		st = self.thismesh.getThreatStatus()
		return st.decode('utf-8')

	def newThreatSubcriteriaA(self, int subcri):
		self.thismesh.newThreatSubcriteriaA(subcri)

	def getThreatSubcriteriaA(self):
		return self.thismesh.getThreatSubcriteriaA()

	def randomize(self):
		self.thismesh.randomize()


cdef class Solutionpy:
	
	cdef Solution * thissol
	cdef public double originX
	cdef public double originY
	cdef public double cellSize

	def __cinit__(self, Meshpy mother):

		self.thissol = new Solution(mother.thismesh)

	def __dealloc__(self):
		del self.thissol

	@property
	def critA(self):
		return self.thissol.critA

	@critA.setter
	def critA(self, newCritA):
		self.thissol.critA = newCritA


	@property
	def critB(self):
		return self.thissol.critB

	@critB.setter
	def critB(self, newCritB):
		self.thissol.critB = newCritB

	@property
	def score(self):
		return self.thissol.score

	@score.setter
	def score(self, newScore):
		self.thissol.score = newScore

	@property
	def ndmScore(self):
		return self.thissol.ndmScore

	@property
	def aggrScore(self):
		return self.thissol.aggrScore

	@property
	def extent(self):
		return self.thissol.extent

	@property
	def origin(self):
		return self.thissol.origin

	@property
	def spp2crit(self):
		return self.thissol.spp2crit

	def getSize(self):
		return self.thissol.getSize()

	def setValue(self, int index, float theVal):
		if index < 0 or index >= self.thissol.getSize():
			raise IndexError("Index {0} out of range".format(index))
		else:
			self.thissol.setValue(index, theVal)
		
	def getValue(self, int index):
		if index < 0 or index >= self.thissol.getSize():
			raise IndexError("Index {0} out of range".format(index))
		else:
			return self.thissol.getValue(index)

	def isNull(self):
		return self.thissol.isNull()

	def nullMe(self):
		self.thissol.nullMe()

	def randomize(self):
		self.thissol.randomize()

	def toBitList(self):
		out = []
		for c in range(self.getSize()):
			if self.getValue(c) > 0:
				out.append(1)
			elif self.getValue(c) == 0:
				out.append(0)
			else:
				raise ValueError("Solution object has negative values.")
		return out


def metasearchAlt(list obs, double eps, int iters, int maxOutSize, double ndmWeight, taxGr = None, spp2gr = None):
	"""	
	KBA search routine. Output is a 2-dimensional list of Solution objects. Lists
	of the first order are non-overlapping sets of areas. Solutions are score 
	ordered.

	Arguments:

	- obs (list): Set of species distributions (pyMesh objects).

	- eps (float): Maximum distance among distributions of the same cluster.

	- iters (int): Number of iterations of to retrieve KBA candidates.

	- maxOutSize (int): Maximum number of solutions to report.

	- ndmWeight (float): Scaling factor of the NDM component for scoring solutions.
	"""
	
	pout = []
	cdef vector[Mesh*] ve
	cdef vector[vesol] out
	cdef cppmap[int, vector[int]] taxGroups
	cdef cppmap[int, int] spp2groups

	if type(taxGr) == dict:
		taxGroups = taxGr	
	elif taxGr is None:
		pass #taxGroups = {}
	else:
		raise ValueError("taxGr is not a dictionary")
	
	if type(spp2gr) == dict:
		spp2groups = spp2gr
	elif spp2gr is None:
		pass #spp2groups = {}
	else:
		raise ValueError("spp2gr is not a dictionary")

	for ob in obs:
		obme = <Meshpy> ob
		ve.push_back(obme.thismesh)

	out = metaAlt(ve, taxGroups, spp2groups, eps, iters, maxOutSize, ndmWeight)

	for i in range(out.size()):
		tmp = []
		for j in range(out[i].size()):
			psol = Solutionpy(obs[0])
			#del psol.thissol
			# For some reason cython now requires dereferencing of Solution pointers
			# in out vector. Should be checked for bugs.
			psol.thissol[0] = out[i][j][0] 
			del out[i][j]
			tmp.append(psol)
		pout.append(tmp)

	return pout


def metasearchAltDry(list obs, double eps, int iters, int maxOutSize, double ndmWeight, taxGr = None, spp2gr = None):
	"""Executes the search but does not converts C++ objects to Python objects."""
	print("In metasearchAlt")

	pout = []
	cdef vector[Mesh*] ve
	cdef vector[vesol] out
	cdef cppmap[int, vector[int]] taxGroups
	cdef cppmap[int, int] spp2groups

	if type(taxGr) == dict:
		taxGroups = taxGr	
	elif taxGr is None:
		pass #taxGroups = {}
	else:
		raise ValueError("taxGr is not a dictionary")

	
	if type(spp2gr) == dict:
		spp2groups = spp2gr
	elif spp2gr is None:
		pass #spp2groups = {}
	else:
		raise ValueError("spp2gr is not a dictionary")

	print(len(taxGroups), len(spp2groups))

	print("read group dicts")

	for ob in obs:
		obme = <Meshpy> ob
		ve.push_back(obme.thismesh)
	
	print("Mesh objects extracted from pymesh objects.")

	out = metaAlt(ve, taxGroups, spp2groups, eps, iters, maxOutSize, ndmWeight)

	for i in range(out.size()):
		for j in range(out[i].size()):
			del out[i][j]

	return pout


def dbscancl(obs, double eps):
	
	pyout = {}
	cdef vector[Mesh*] ve
	cdef cppmap[int, vector[int]] out
	cdef cppmap[int, vector[int]].iterator it

	for ob in obs:
		obme = <Meshpy> ob
		ve.push_back(obme.thismesh)
	
	out = dbscan(ve, eps)
	it = out.begin()

	while(it != out.end()):
		
		pyout[dereference(it).first] = []
		
		for j in range(dereference(it).second.size()):
			pyout[dereference(it).first].append(dereference(it).second[j])

		postincrement(it)
	
	return pyout
