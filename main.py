import os
import math
from neperparser import NeperParser

# Get input parameters
width = float(input('Please enter the width of the rectangle: '))
height = float(input('Please enter the height of the rectangle: '))
avgGrainArea = float(input('please enter avg area of voronoi cells: '))

# Calculate the number of grains
Ngrains = math.ceil((width * height) / avgGrainArea)

os.system('del *.tess *.inp *.rpy *.rpy.* *.exception')

# Construct Neper command
neper_command = (
    f"cd;"
    f"rm -fr *.tess *.inp;"
    f"neper -T -n {Ngrains} -dim 2 "
    f"-domain 'square({width},{height})' "
    f"-morpho diameq:{avgGrainArea};"
    f"cp n{Ngrains}-id1.tess /mnt/e/university/final/abaqus-2D-voronoi-tesselation;"
    f"exit;"
)

#get current directory
#we will copy *.tess file in current directory
currentDir = os.getcwd()

# Execute Neper command in WSL
wsl_command = f"wsl {neper_command}"
os.system(wsl_command)

tessfilename = "n" + str(Ngrains) + "-id1"

# parse neper .tess file
nepermodel = NeperParser(tessfilename)

nepermodel.ReadEulerAngles()
nepermodel.ReadVertices()
nepermodel.ReadEdges()

# report parameters to file that will be read by abaqus script
fparam = open("Parameters.txt","w")

fparam.write(str(width) + '\n')
fparam.write(str(height) + '\n')
fparam.write(str(Ngrains) + '\n')
fparam.write(os.getcwd())

fparam.close()

# execute abaqus script
os.system('abaqus cae script=GeneratePolycrystal.py')