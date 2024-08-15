import math


#get width and height of regtangle from user
width = float(input('please enter you regtangle width: '))
height = float(input('please enter height of you regtnale: '))
avg_area = float(input('please enter average area of voronoi cells: '))
Ngrains = math.ceil((width * height) / avg_area)


neperCommand = "neper -T -n " + str(Ngrains)
neperCommand = neperCommand + " -dim 2"
neperCommand = neperCommand + " -domain 'square(" + str(width) + "," + str(height) + ")' "
neperCommand = neperCommand + "-morpho diameq:"+ str(avg_area)
print('---------------------------------------')
print(neperCommand)
print('---------------------------------------')
print(f'this command generate {Ngrains} cells with equvalence diameter {avg_area}')