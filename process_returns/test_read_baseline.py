import os, glob, sys
import numpy
import iris

indir = '/ExSamples/netcdf/product'
version = '20210930'
winter = 'WetWinter2068*'
region = 'NAtlanticEurope'
var = 'sfcWind_daily'


files = sorted(glob.glob(os.path.join(indir, version, 'BaselineWinters', region, var, '*.nc')))
a = iris.load(files)


# to concatenate have to remove information that the baseline runs come from different winters, so time, year, season_year coords
# also ensemble_member_id is not monotonic, so have to demote it to auxcoord and replace it with a counter coord that is monotonic
# then concatenate_cube() method works

new_tdim_coord = iris.coords.DimCoord(numpy.arange(a[0].shape[1]), long_name='day_of_season')
cnt = 0
for i in a:
    i.remove_coord('time')
    i.remove_coord('season_year')
    i.remove_coord('year')
    i.add_dim_coord(new_tdim_coord, 1)
    iris.util.demote_dim_coord_to_aux_coord(i, 'ensemble_member_id')
    new_edim_coord = iris.coords.DimCoord(numpy.arange(cnt, cnt + i.shape[0]), long_name='ensemble_counter')
    i.add_dim_coord(new_edim_coord, 0)
    cnt += i.shape[0]

ans = a.concatenate_cube()
print(repr(ans))


