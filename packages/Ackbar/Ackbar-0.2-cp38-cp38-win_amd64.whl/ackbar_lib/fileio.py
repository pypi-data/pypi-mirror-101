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


import sys
import csv
import re

from math import ceil, floor, sin, cos, atan2, pi

import fiona
from fiona.crs import from_epsg
from shapely.geometry import Point, Polygon, MultiPolygon, mapping

from ackbar_lib import pydata, shapes
from ackbar_lib.B2_recommended_thresholds import groups as iucn_groups


class InputData(object):
	"""
	Input data processor class. Class constructor requires a csv file (str) with
	three columns: longitude, latitude, and taxon name.
	"""
	def __init__(self, infile, csv_pars = None):
		self.points = {} # values are population fractions
		self.totPops = {} # total populations per taxon
		self.iucn = {} # taxon to (Category, subcriteriaA)
		self.minLatitude = 91.0
		self.maxLatitude = -91.0
		self.minLongitude = 181.0
		self.maxLongitude = -181.0
		self.originN = None
		self.cellSize = None
		self.rows = None
		self.cols = None
		self.geometry = None
		self.csvfile = infile
		self.presence_grid = []
		self.index_reg = {}
		self.taxonGroups = {}
		self.taxonGroupsInfo = {}
		self.groupDict = {}
		self.spp2groupDict = {}
		self.csv_params = {}
		lineCounter = 0
		latCol = None
		lonCol = None
		taxCol = None

		if type(csv_pars) == dict:

			if "delimiter" in csv_pars:
				self.csv_params["delimiter"] = csv_pars["delimiter"]

			if "lineterminator" in csv_pars:
				self.csv_params["lineterminator"] = csv_pars["lineterminator"]
			
			if "quotechar" in csv_pars:
				self.csv_params["quotechar"] = csv_pars["quotechar"]

		with open(infile,'r') as fil:
			
			table = csv.reader(fil, **self.csv_params)

			for lineCounter, row in enumerate(table):

				if lineCounter == 0:

					for icol , col in enumerate(row):

						if re.search("lon(gitude)*", col, flags=re.I):
							lonCol = icol
							continue

						elif re.search("lat(titude)*", col, flags=re.I):
							latCol = icol
							continue

						elif re.search("taxon", col, flags=re.I):
							taxCol = icol
							continue

					if lonCol is None or latCol is None or taxCol is None:

						raise IOError("Input file `{0}`: column labels do not follow the required format (`Taxon`, `Longitude`, `Latitude`).".format(infile))

				else:
				
					row[latCol] = re.sub(r"[\s\'\"]","",row[latCol])
					row[lonCol] = re.sub(r"[\s\'\"]","",row[lonCol])
					lat = None
					lon = None

					try:
						lat = float(row[latCol])

						if lat < -90 or lat > 90:
							raise ValueError('Distribution file error: {2} is not a valid latitude value (line {0} in file `{1}`).'.format(lineCounter, infile, row[latCol]))
					
					except ValueError as te:
						mess = str(te)

						if mess.startswith('could not convert string to float'):
							raise ValueError('Distribution file error: {2} is not a valid latitude value (line {0} in file `{1}`).'.format(lineCounter, infile, row[latCol]))

						else:
							raise
					
					try:
						lon = float(row[lonCol])
						
						if lon < -180 or lon > 180:
							raise ValueError('Distribution file error: {2} is not a valid longitude value (line {0} in file `{1}`).'.format(lineCounter, infile, row[lonCol]))
					
					except ValueError as te:
						mess = str(te)

						if mess.startswith('could not convert string to float'):
							raise ValueError('Distribution file error: {2} is not a valid longitude value (line {0} in file `{1}`).'.format(lineCounter, infile, row[lonCol]))
						
						else:
							raise					
					
					if len(row[taxCol]) > 105:
						raise IOError("Distribution file error: `{0}` exceeds the maximum taxon name size, 105 chars (line {1} in file `{2}`)".format(row[taxCol],lineCounter, infile))


					#############################################################
					#															#
					# 			Reproject data if user wishes to				#
					#															#
					#############################################################


					if row[taxCol] in self.points:
						self.points[row[taxCol]][(lon,lat)] = 1

					else:
						self.points[row[taxCol]] = { (lon,lat) : 1 }

					if self.minLatitude > lat:
						self.minLatitude = lat

					if self.maxLatitude < lat:
						self.maxLatitude = lat

					if self.minLongitude > lon:
						self.minLongitude = lon

					if self.maxLongitude < lon:
						self.maxLongitude = lon

		if len(self.points) < 3:
			raise ValueError("Input file only contain distribution data from {0} species (at least three are required).".format(len(self.points)))

		return None


	def groupFiles(self, assignments_file, diversity_file):
		"""
		Process information from files and store it in data structures.
		Only stores data of taxa included in distribution file.
		"""
		log = '' # log buffer
		assignments = False
		taxonCol = None
		groupCol = None
		rangeCol = None
		groupBisCol = None
		globsppCol = None
		minsppCol = None
		rangeThresCol = None
		self.taxonGroups = {}
		self.taxonGroupsInfo = {}

		with open(assignments_file, 'r') as afile:
			
			table = csv.reader(afile, **self.csv_params)
			
			for irow , row in enumerate(table):
				
				if irow == 0:

					for ic , cell in enumerate(row):

						if re.search('group', cell, flags=re.I):
							groupCol = ic
							continue

						if re.search('taxon', cell, flags=re.I):
							taxonCol = ic
							continue

						if re.search('range_size', cell, flags=re.I):
							rangeCol = ic
							continue

					if groupCol is None or taxonCol is None:
						raise IOError("Input file `{0}`: column labels do not follow the required format (headers should be `Group`, `Taxon`, and `Range_size`).".format(assignments_file))

				else:
					rangeS = None

					if not rangeCol is None:
						rangeS = re.sub(r'^\s+', '', row[rangeCol])
						rangeS = re.sub(r'\s+$', '', row[rangeCol])

						if len(rangeS) > 0:
							rangeS = float(rangeS)
								
							if rangeS <= 0:
								raise IOError("Invalid range size provided (`{0}`)".format(rangeS))

						else:
							rangeS = None

					group = re.sub(r'^\s+', '', row[groupCol])
					group = re.sub(r'\s+$', '', row[groupCol])

					#############################################################
					#															#
					# 	 	Does this threshold make sense???					#
					#															#
					#############################################################

					if len(group) < 4:
						raise IOError("`{0}` does not seem an actual taxonomic membership".format(group))

					taxon = re.sub(r'^\s+', '', row[taxonCol])
					taxon = re.sub(r'\s+$', '', row[taxonCol])

					if taxon in self.taxonGroups:
						raise IOError("Taxon duplicated in group file (`{0}`)".format(taxon))

					else:
						self.taxonGroups[taxon] = {'group': group, 'range_size': rangeS}

						if rangeS is None and taxon in self.points:
						
							point_list = [x for x in self.points[taxon].keys()]
							tarea = shapes.area_estimator(point_list)
							self.taxonGroups[taxon]['range_size'] = tarea


		if not diversity_file is None:

			with open(diversity_file, 'r') as dhandle:

				table = csv.reader(dhandle, **self.csv_params)
				
				for irow , row in enumerate(table):
					
					if irow == 0:

						for ic , cell in enumerate(row):

							if re.search('group', cell, flags=re.I):
								groupBisCol = ic
								continue

							if re.search('global_species', cell, flags=re.I):
								globsppCol = ic
								continue

							if re.search('min_species', cell, flags=re.I):
								minsppCol = ic
								continue

							if re.search('range_threshold', cell, flags=re.I):
								rangeThresCol = ic
								continue

						if groupBisCol is None or (globsppCol is None and minsppCol is None):
							raise IOError("Input file `{0}`: column labels do not follow the required format (headers should be `Group`, `Global_species`, `Min_species`, and `Range_threshold`).".format(assignments_file))

					else:

						tgroup = row[groupBisCol]
						tsp = row[globsppCol]
						range_thr = None
						min_spp = None

						if rangeThresCol:
							range_thr = row[rangeThresCol]
							if len(range_thr) > 0:
								range_thr = int(range_thr)
							else:
								range_thr = 10000

						if minsppCol:
							min_spp = row[minsppCol]
							if len(min_spp) > 0:
								min_spp = int(min_spp)

						if len(tsp) > 0:
							tsp = int(tsp)

						else:
							tsp = None

						if tgroup in self.taxonGroupsInfo:
							raise IOError("Group duplicated in group diversity file (`{0}`)".format(tgroup))

						else:
							self.taxonGroupsInfo[tgroup] = {
								'range_threshold': range_thr,
								'global_species': tsp,
								'min_spp' : min_spp}

		for taxon in self.points:

			if taxon not in self.taxonGroups:
				raise IOError("`{0}` not included in taxonomic group assignment file".format(taxon))

		
	def groups2search(self):
		"""Set dictionaries of taxonomic group info required for search function."""
		self.groupDict = {}
		self.spp2groupDict = {}

		# Append groups from recommended IUCN list to group dictionaries
		for taxon in self.points:

			if taxon in self.taxonGroups:

				tgroup = self.taxonGroups[taxon]['group']

				if not tgroup in self.taxonGroupsInfo:

					if tgroup in iucn_groups:

						thres = None

						if iucn_groups[tgroup]['range_threshold'] is None:
							thres = 10000

						else:
							thres = iucn_groups[tgroup]['range_threshold']

						self.taxonGroupsInfo[tgroup] = {
							'range_threshold': thres, 
							'global_species': None, 
							'min_spp': iucn_groups[tgroup]['min_spp']}

					else:

						raise IOError("Taxonomic group `{0}` included in neither the group diversity file nor the official IUCN taxonomic group list.".format(tgroup))
			
			else:

				raise IOError("Taxon `{0}` not included in taxonomic group assignment file.".format(taxon))

		for ita, taxon in enumerate(self.points):

			tgr = self.taxonGroups[taxon]['group']
			grouppy = None

			for igr, gr in enumerate(sorted(self.taxonGroupsInfo.keys())):
				
				if tgr == gr:
					
					grouppy = igr
					break
			
			if grouppy is None:
				print('{0} not in self.points'.format(taxon))

			else:
				self.spp2groupDict[ita] = grouppy

		for igr, gr in enumerate(sorted(self.taxonGroupsInfo.keys())):
		
			mspp = None
			mran = self.taxonGroupsInfo[gr]['range_threshold']

			if self.taxonGroupsInfo[gr]['min_spp']:
				mspp = self.taxonGroupsInfo[gr]['min_spp']

			else:
				mspp = int(self.taxonGroupsInfo[gr]['global_species'] * 0.0002)
		
			if mspp < 2:
				mspp = 2
		
			self.groupDict[igr] = (mran, mspp)


	def iucnFile(self, filename):
		"""
		Process IUCN categories and subcriteria for criterion A from a csv file.
		"""
		lineCounter = 0
		nameCol = None
		categCol = None
		criterCol = None
		validCats = ['CR', 'EN', 'VU', 'NT', 'LC', 'DD', 'NE']

		with open(filename,'r') as fil:
			table = csv.reader(fil, **self.csv_params)
			for row in table:
				lineCounter += 1
				if lineCounter == 1:
					
					for ic, cell in enumerate(row):
						if re.search("taxon",row[ic],flags=re.I):
							nameCol = ic
							continue
		
						if re.search("categor",row[ic],flags=re.I):
							categCol = ic
							continue

						if re.search("criter",row[ic],flags=re.I):
							criterCol = ic
							continue

					if nameCol is None or categCol is None or criterCol is None:
						raise IOError("Input file `{0}`: column labels do not follow the required format (`Taxon`, `Category`, `Criteria`).".format(filename))
				
				else:
					
					cat = row[categCol]

					isvalid = False
					if type(cat) == str:
						
						for vc in validCats:
							cat = re.sub(r'^\s+','',cat)
							cat = re.sub(r'\s+$','',cat)
							if vc == cat.upper():
								isvalid = True

					if not isvalid:
						raise IOError("{0} has a non valid IUCN category code (`{1}`)".format(row[nameCol], cat))

					if cat == '' or re.search(r'^\s+$', cat): 
						cat = 'NE'



					subcrA = []
					if type(row[criterCol]) == str:
						
						if not re.search(r'[BCDE]', row[criterCol]) and re.search(r'A', row[criterCol]):

							digits = re.findall(r'\d', row[criterCol])

							if len(digits) >= 1:

								for dig in digits:

									if dig == '1':
										subcrA.append(1)

									elif dig == '2':
										subcrA.append(2)

									elif dig == '4':
										subcrA.append(4)

									elif dig != '3':
										raise IOError("{0} has non valid subcriteria A (`{1}`)".format(row[nameCol], row[criterCol]))

					self.iucn[row[nameCol]] = {'category': cat, 'subcritA': subcrA}
		
			for na in [x for x in self.points if not x in self.iucn]:

				self.iucn[na] = {'category': 'NE', 'subcritA': []}


	def mergePoints(self, taxonName, maxDist):
		"""
		Merge points using DBSCAN. Cluster scheme is store in values of points
		dictionary.
		"""
		clusters = self.dbscan(taxonName, maxDist)

		totPops = len(clusters)
		for cl in clusters:
			factor = 1 / len(clusters[cl])
			for loc in clusters[cl]:
				self.points[taxonName][loc] = factor

		return totPops


	def mergePointsAllTaxa(self, maxDist):
		"""
		Merge points of all taxa; wrapper to self.mergePoints.
		"""
		for taxon in self.points:
			# Join points that are too close to be different populations
			self.totPops[taxon] = self.mergePoints(taxon, maxDist)


	def reduceArea(self, shapefile):
		"""
		Reduce the spatial scope of the dataset by removing all points that lie outside a provided set of polygons.   
		"""
		self.points = shapes.filter_points(self.points, shapefile)
		oldTotPops = self.totPops
		self.totPops = {}

		for tax in self.points:
			self.totPops[tax] = oldTotPops[tax]
		

	def dbscan(self, taxon, eps):
		"""
		DBSCAN-like algorithm to cluster points. There is not minimum cluster 
		size and, therefore, no noise list.

		- eps: maximum distance among cluster members.  
		"""
		clusters = {}
		visited = {x:0 for x in self.points[taxon]}
		for pivot in self.points[taxon]:
			if visited[pivot] == 0:
				visited[pivot] = 1
				clusters[pivot] = [pivot]
				self.expand(taxon, clusters, pivot, pivot, visited, eps)

		#########################################################################
		#																		#
		# 					Is the following loop necessary?					#
		#																		#
		#########################################################################

		for q in self.points[taxon]:
			qIsAlone = 1
			for key in clusters:
				if q in clusters[key]:
					qIsAlone = 0
			if qIsAlone:
				clusters[q] = [q]
				
		return clusters


	def expand(self, taxon, clusters, pivot, border, visited, eps):
		for newborder in self.points[taxon]:
			if visited[newborder] == 0:
				if border != newborder:
					td = self.haversine(border, newborder)
					if td < eps:
						clusters[pivot].append(newborder)
						visited[newborder] = 1
						self.expand(taxon, clusters, pivot, newborder, visited, eps)


	def haversine(self, pointA, pointB, radius = 6371):
		phi1 = pointA[1] * pi / 180 # in radians
		phi2 = pointB[1] * pi / 180
		phiDelta = (pointB[1] - pointA[1]) * pi / 180
		lambdaDelta = (pointB[0] - pointA[0]) * pi / 180
		a = sin(phiDelta / 2) ** 2 + cos(phi1) * cos(phi2) * sin(lambdaDelta / 2) ** 2
		c = 2 * atan2(a ** 0.5, (1-a) ** 0.5)
		d = radius * c
		return d


	def filter_nulls(self, tiles):
		"""
		Filters out tiles that are null and update the species-to-group dictionary.
		Null tiles occur often after clearing data point container from localities
		within previously delimited KBAs.

		Arguments:

		- tiles (list): Tiles output by `getlist` method.
		"""

		newlist = []
		newdict = {}
		counter = 0
		
		for it, ti in enumerate(tiles):
			
			if not ti.isNull():
		
				newlist.append(ti)

				if len(self.spp2groupDict) > 0:
					newdict[counter] = self.spp2groupDict[it]

				counter +=1
		
		if len(self.spp2groupDict) > 0:
			self.spp2groupDict = newdict

		return newlist


	def getTiles(self, cellSize, offsetLat = 0, offsetLon = 0):
		"""
		Create basic data structures required for the analysis from a collection
		of distributional points. Returns a list of data.Tile objects.

		Arguments:

		- cellSize (int or float): Size of the cells making up the lattice. If
		the grid is made up of squares, `cellSize` will be the side of the square.

		"""
		if cellSize > (self.maxLatitude - self.minLatitude) or cellSize > (self.maxLongitude - self.minLongitude):
			raise ValueError("Grid cell size (`cellSize`) is larger than the extent of the input distributions.")

		self.cellSize = float(cellSize)
		tileStack = []
		self.rows, self.cols = 0, 0
		offsetLat = float(offsetLat)
		offsetLon = float(offsetLon)
		
		self.originN = ((self.minLongitude - offsetLon), (self.maxLatitude + offsetLat))
		span = [max((self.maxLongitude - self.originN[0]), self.cellSize), max((self.originN[1] - self.minLatitude), self.cellSize)]
		totCols = int(ceil(span[0] / self.cellSize))
		totRows = int(ceil(span[1] / self.cellSize))
		span[0] = totCols * self.cellSize
		span[1] = totRows * self.cellSize
		self.rows, self.cols = totRows, totCols
		self.presence_grid = [[0 for x in range(totCols)] for x in range(totRows)]
		grid_coll = []

		for taxon in self.points:



			grid = [[0 for x in range(totCols)] for x in range(totRows)]

			for lon,lat in self.points[taxon]:
				apprindx = ceil( ( (lon - self.originN[0]) / span[0]) * totCols)
				apprindy = ceil( ( (self.originN[1] - lat) / span[1]) * totRows)
				
				x = apprindx - 1
				y = apprindy - 1

				if x < 0:
					x += 1

				if y < 0:
					y += 1

				#th = self.points[taxon][lon,lat] / totPops
				th = self.points[taxon][lon,lat]
				th /= self.totPops[taxon]								
				grid[y][x] += th
				self.presence_grid[y][x] += th
				
			grid_coll.append(grid)


		self.index_reg = {}

		act_size = 0
		for ir, row in enumerate(self.presence_grid):
			for ic, cel in enumerate(row):
				if cel > 0:
					self.index_reg[(ir, ic)] = act_size
					act_size += 1

		for it, taxon in enumerate(self.points):
			
			cat = self.iucn[taxon]['category']
			tile = pydata.Meshpy(act_size, taxon, cat)
			
			for sca in self.iucn[taxon]['subcritA']:
				tile.newThreatSubcriteriaA(sca)

			if len(self.taxonGroups) > 0 and taxon in self.taxonGroups and self.taxonGroups[taxon]['range_size']:
				tile.setRange(self.taxonGroups[taxon]['range_size'])
		
			for r in range(self.rows):
				for c in range(self.cols):
					if self.presence_grid[r][c] > 0:
						
						rowNeighs = [r]
						colNeighs = [c]
						
						if grid_coll[it][r][c] > 0:
							
							tile.setValue(self.index_reg[(r, c)], grid_coll[it][r][c])

						if r > 0:
							rowNeighs.append(r-1)

						if r < (self.rows - 1):
							rowNeighs.append(r+1)

						if c > 0:
							colNeighs.append(c-1)

						if c < (self.cols - 1):
							colNeighs.append(c+1)

						for nr in rowNeighs:
							if r != nr and self.presence_grid[nr][c] > 0:
								tile.linkNeighs(self.index_reg[(r, c)], self.index_reg[(nr, c)])

						for nc in colNeighs:
							if c != nc and self.presence_grid[r][nc] > 0:
								tile.linkNeighs(self.index_reg[(r, c)], self.index_reg[(r, nc)])

			tileStack.append(tile)

		return tileStack


	def tile2str(self, tile):
		"""
		Get string of Tile given a encodification scheme. Only for testing.
		"""
		if tile.getSize() == len(self.index_reg):		
			ms = ''

			for r in range(self.rows):

				for c in range(self.cols):

					if self.presence_grid[r][c] > 0:
						val = tile.getValue(self.index_reg[(r, c)])

						if val > 0:
							ms += '1 '

						else:
							ms += '0 '

					else:
						ms += '- '

				ms += '\n'

			return ms


	def grid2shape(self, filename):
		"""
		Saves the grid into a shapefile.
		"""
		counter = 0
		wrtMode = None

		schema = {
			'geometry': 'Polygon',
			'properties': {'id': 'int', 'x': 'int', 'y': 'int', 'xBase': 'float', 'yBase': 'float'},
			}

		for y, x in self.index_reg:
			xBase = self.originN[0] + self.cellSize * (x + 1)
			yBase = self.originN[1] - self.cellSize * (y + 1)
			ocor = [(xBase, yBase + self.cellSize),
				(xBase - self.cellSize, yBase + self.cellSize),
				(xBase - self.cellSize, yBase),
				(xBase, yBase)]
			pol = Polygon(ocor)
			
			if counter == 0:
				wrtMode = 'w'
			else:
				wrtMode = 'a'

			with fiona.open(filename, wrtMode, 'ESRI Shapefile', schema, from_epsg(4326)) as fhandle:
				fhandle.write({'geometry': mapping(pol), 'properties': 
					{'id': counter, 'x': x, 'y': y, 'xBase': xBase, 'yBase': yBase}})

			counter += 1

		return None


