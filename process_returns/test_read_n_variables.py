import os, glob, sys
import numpy
import iris

indir = '/ExSamples/netcdf/product'
version = '20210930'
winter = 'WetWinter2068*'
region = 'NAtlanticEurope'
variables = ['pr_daily', 'tasmax_daily', 'hurs_daily', 'sfcWind_daily']

files = list()
cubes = iris.cube.CubeList()
for var in variables:
    files = sorted(glob.glob(os.path.join(indir, version, winter, region, var, '*.nc')))
    toadd = iris.load(files).concatenate_cube()
    cubes.append(toadd)

ecoord = cubes[0].coord('ensemble_member_id')
for c in cubes:
    ecoord = ecoord.intersect(c.coord('ensemble_member_id'))

cubes = iris.cube.CubeList([c.subset(ecoord) for c in cubes])

print(cubes)


