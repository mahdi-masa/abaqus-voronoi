# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2017 replay file
# Internal Version: 2016_09_27-22.54.59 126836
# Run by engs1992 on Tue Jun 16 14:20:49 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
import math
import random
import numpy as np
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=218.485397338867, 
	height=100.585189819336)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
	referenceRepresentation=ON)
Mdb()

# parse geometrical parameters from file
fparam = open("Parameters.txt","r")

pwidth = float(fparam.readline())
pheight = float(fparam.readline())
pdepth = 1
Ngrains = int(fparam.readline())
caepath = fparam.readline()

fparam.close()

#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
	sheetSize=200.0)
g, vertex, datum, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)

# draw rectangle
s.rectangle(point1=(0.0, 0.0), point2=(pwidth,pheight))

part = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, 
	type=DEFORMABLE_BODY)
part = mdb.models['Model-1'].parts['Part-1']

# extrude to create parallelepiped
part.BaseShell(sketch=s)

s.unsetPrimaryObject()
part = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=part)
del mdb.models['Model-1'].sketches['__profile__']

part = mdb.models['Model-1'].parts['Part-1']

# name of files with Euler angles, vertices and edges
euleranglesfilename = "n" + str(Ngrains) + "-id1-eulerangles.tess"
datumpointsfilename = "n" + str(Ngrains) + "-id1-datumpoints.tess"
edgesfilename = "n" + str(Ngrains) + "-id1-edges.tess"

# read external datum points file and add datum points to cae model
datumPointFile = open(datumpointsfilename,"r")

# arrays of x, y, z coordinates of vertices
arrx = np.zeros(shape=(0)) 
arry = np.zeros(shape=(0))

count = 1
for line in datumPointFile:
	tempdata = line.split()
	# get x and y coordinate of datum point
	tempx = float(tempdata[1])
	tempy = float(tempdata[2])
	arrx = np.append(arrx,tempx)
	arry = np.append(arry,tempy)
	part.DatumPointByCoordinate(coords=(tempx, tempy, 0))
	count = count + 1

datumPointFile.close()

part = mdb.models['Model-1'].parts['Part-1']
partFaces = part.faces
# define boundingbox to pick the entire upper face
BoundBox1 = np.zeros(shape=(3))
BoundBox2 = np.zeros(shape=(3))

BoundBox1[0] = -0.1*pwidth
BoundBox1[1] = -0.1*pheight
# BoundBox1[2] = 0.9*pdepth

BoundBox2[0] = 1.1*pwidth
BoundBox2[1] = 1.1*pheight
pickedFaces = partFaces.getByBoundingBox(BoundBox1[0],BoundBox1[1], -1,BoundBox2[0],BoundBox2[1], +1)
part.Set(faces= pickedFaces, name='part faces')
vertex, edge, datum = part.vertices, part.edges, part.datums

# array that contains point at the boundary of edges
# using .tess file numbering
edgepoint1 = np.array([],dtype='uint64')
edgepoint2 = np.array([],dtype='uint64')
# array with the edge indices
# counting only edges defined on the upper surface
# and leaving 0 the ones on the corner edges
edgeindex = np.array([],dtype='uint64')

edgeFile = open(edgesfilename,"r")

count = 1

for line in edgeFile:
	InnerEdge = True # flag to indicate that this is not an edge at the boundary of the surface 
	part = mdb.models['Model-1'].parts['Part-1']
	partFaces = part.faces
	pickedFaces = partFaces.getByBoundingBox(xMin=BoundBox1[0], yMin=BoundBox1[1], zMin=-1, xMax=BoundBox2[0], yMax=BoundBox2[1], zMax=1)
	vertex, edge, datum = part.vertices, part.edges, part.datums
	tempdata = line.split()
	# get indices of the datum points bounding the edge
	# indices start from 1
	# these are indices in the .tess file, not abaqus
	temppoint1 = int(tempdata[1]) # corresponds to abaqus datum point number - 1
	temppoint2 = int(tempdata[2]) # corresponds to abaqus datum point number - 1
	edgepoint1 = np.append(edgepoint1,np.uint64(temppoint1))
	edgepoint2 = np.append(edgepoint2,np.uint64(temppoint2))
	# is this an edge at the boundary?
	if (arrx[temppoint1-1] == arrx[temppoint2-1]):
		if (arrx[temppoint1-1] == 0.0 or arrx[temppoint1-1] == pwidth):
			InnerEdge = False
	if (arry[temppoint1-1] == arry[temppoint2-1]):
		if (arry[temppoint1-1] == 0.0 or arry[temppoint1-1] == pheight):
			InnerEdge = False
	if (InnerEdge):
		# find abaqus indices
		abqindex1 = temppoint1+1
		abqindex2 = temppoint2+1	
		part.PartitionFaceByShortestPath(point1=datum[abqindex1], point2=datum[abqindex2], 
			faces=pickedFaces)
		edgeindex = np.append(edgeindex,np.uint64(count))
		count = count + 1
	else:
		edgeindex = np.append(edgeindex,np.uint64(0))
edgeFile.close()

mdb.models['Model-1'].Material(name='phaze-one')
mdb.models['Model-1'].materials['phaze-one'].Elastic(table=((2000.0, 0.3), ))

mdb.models['Model-1'].Material(name='phaze-two')
mdb.models['Model-1'].materials['phaze-two'].Elastic(table=((5000.0, 0.3), ))

mdb.models['Model-1'].HomogeneousSolidSection(name='phaze-one-section', 
    material='phaze-one', thickness=None)

mdb.models['Model-1'].HomogeneousSolidSection(name='phaze-two-section', 
    material='phaze-two', thickness=None)

face20Percent = math.ceil(Ngrains*0.20)
print(face20Percent)
face80Percent = Ngrains - face20Percent
part = mdb.models['Model-1'].parts['Part-1']
print(face80Percent)
# Create a set for the 20% of faces
setOne = part.Set(faces = partFaces[0:(face20Percent-1)], name='Set_20percent')

# Create a set for the remaining 80% of faces
setTwo = part.Set(faces = partFaces[(face20Percent-1):], name='Set_80percent')

part.SectionAssignment(region=setTwo, sectionName='phaze-one-section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

part.SectionAssignment(region=setOne, sectionName='phaze-two-section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)