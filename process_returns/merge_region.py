# for cube domains, merge batches and concatenate 

import os, sys, glob
import datetime, time
import numpy
import iris
import iris.coord_categorisation
from copy import deepcopy

import matplotlib.pyplot as plt
import iris.quickplot as qplt

def extract_natleur(cube):
#    qumpy.irislib.invert_wrap_lons(cube)
    cube = cube.intersection(longitude=(-80, 45), latitude=(20, 75))
    return cube

def extract_uk(cube):
    return cube.intersection(longitude=(-12.5, 5), latitude=(48, 62))

def save_data_in_chunks(cube, outdir, sbatch, name, region, nchunk=100):
    n = cube.shape[0]
    index = list(range(n))
    nchunks = n // nchunk
    if n % nchunk > 0:
        nchunks += 1
    for i in numpy.array_split(index, nchunks):
        c = cube[i]
        member_str = 'members%.4i-%.4i' % (min(i), max(i))
        outf = os.path.join(outdir, '%s_%s_%s_%s.nc' % (sbatch, name, region, member_str))
        print('Saving to %s' % outf)
        iris.save(c, outf) 
 
def find_duplicates(cube, verbose=False):
    n = cube.shape[0]
    ok = [True] * n
    for i in range(cube.shape[0]-1):
        if verbose:
            print(i)
        if ok[i]:
            i1 = i + 1
#            d = cube.data[i1:,0]
#            diff = numpy.abs(d - cube.data[i,0]).reshape(d.shape[0], -1).ptp(-1)
            d = cube.data[i1:]
            diff = numpy.abs(d - cube.data[i]).reshape(d.shape[0], -1).ptp(-1)
            same = numpy.where(diff == 0.0)[0].tolist()
            if same:
                print(i, [s+i+1 for s in same])
            for s in same:
                ok[s + i + 1] = False
    return ok

def remove_duplicates(cube):
    ok = find_duplicates(cube)
    if cube.shape[0] == sum(ok):
        print('No duplicates')
        return cube
    else:
        print('Reduced from %s to %s' % (cube.shape[0], sum(ok)))
        return cube[ok]

#-------------------------------------------------------------------------------
version = '20220107'

region_dict = {'UK':extract_uk, 'NAtlanticEurope':extract_natleur}
regions_not_to_split = ['UK']

batch_dict = {'2066':('batch_878', 'batch_883', 'batch_896'),
                      '2068':('batch_879', 'batch_886', 'batch_897'),
                      '2072':('batch_887', 'batch_898'),
                      'base':('batch_877', 'batch_882')}
batch_name_dict = {'2066': 'HotWinter2066-r001i1p02868',
                   '2068': 'WetWinter2068-r001i1p02242',
                   '2072': 'HotWinter2072-r001i1p01554',
                   'base': 'BaselineWinters'}
 
#Batch 882 Baseline
#Batches 883 and 896 Future 2066
#Batches 886 and 897 Future 2068
#Batches 887 and 898 Future 2072 
# - Batch 877 -> Baseline          : potentially more corruption
# - Batch 878 -> Future 2066 (hot) : potentially more corruption
# - Batch 879 -> Future 2068 (wet) : potentially more corruption
 
 
batch_type_dict = {'886': 'wet',
              '883': 'hot',
              '887': 'hot',
              '882': 'baseline',
              '877': 'baseline-prototype',
              '878': 'hot-prototype',
              '879': 'wet-prototype',
              '896': 'hot',
              '897': 'wet',
              '898': 'hot'}
  
agg_dict = dict(mean=iris.analysis.MEAN, maximum=iris.analysis.MAX, minimum=iris.analysis.MIN)
 
name_dict = dict(item16222_daily_mean='psl_daily',
               	 item3236_daily_minimum="tasmin_daily",
                 item3249_daily_mean="sfcWind_daily",
                 item5216_monthly_mean="pr_monthly",
                 item3236_daily_maximum="tasmax_daily",
                 item3245_daily_mean="hurs_daily",
                 item5216_6hrly_mean="pr_6hrly",
                 item8234_daily_mean="mrros_daily",
                 item3236_daily_mean="tas_daily",
                 item3249_6hrly_maximum="sfcWindmax_6hrly",
                 item5216_daily_maximum="prmax_daily",
                 item5216_daily_mean="pr_daily",
                 item8235_daily_mean="mrrob_daily",
                 item1_0hrly_mean='ps_6hrinst',
                 item16203_0hrly_mean='ta850_6hrinst',
                 item15201_0hrly_mean='ua850_6hrinst',
                 item15226_0hrly_mean='hus850_7hrinst',
                 item15201_daily_mean='ua250_daily',
                 item16202_daily_mean='zg500_daily',
                 item15202_daily_mean='va850_daily',
                 item4203_daily_mean='prlsa_daily',
                 item2207_daily_mean='rlds_daily',
                 item1235_daily_mean='rsds_daily')

 
if len(sys.argv) == 4:
    region = sys.argv[2]
    batch2merge = sys.argv[1]
    var = sys.argv[3]
else:
    region = 'UK'
#    region = 'NAtlanticEurope'
    batch2merge = '2072'
    var = 'item15202_daily_mean'

indir = '/ExSamples/netcdf/'
outdir = '/ExSamples/netcdf/product'
extractfn = region_dict[region]

outdir = os.path.join(outdir, version)

if batch2merge == 'base':
# first work out 30 combinations
    ftest = sorted(glob.glob(os.path.join(indir, batch_dict[batch2merge][-1], 'region', 'merged', version, '*%s*.nc' % name_dict[var])))
    combos = [os.path.basename(f).split('_')[0] for f in ftest]
    years = list(range(2007, 2017))
    for combo in combos:
        all_files = list()
        all_cubes = iris.cube.CubeList()
        for ib, b in enumerate(batch_dict[batch2merge]):
            ibatch = int(b.replace('batch_', ''))
            sstring = os.path.join(indir, b, 'region', 'merged', version, '%s*%s*.nc' % (combo, name_dict[var]))
            files = sorted(glob.glob(sstring))
            all_files += files
            cubes = iris.cube.CubeList([extractfn(c) for c in iris.load(files)])
            for c in cubes:
                ecoord = c.coord('ensemble_member_id')
                new_coord = ecoord.copy(points=ecoord.points + ibatch * 10000)
                c.replace_coord(new_coord)
                batchid_auxcoord = iris.coords.AuxCoord([str(c.attributes['batchid'])] * c.shape[0], long_name='batchid')
                c.add_aux_coord(batchid_auxcoord, 0)
                del c.attributes['batchid'], c.attributes['creation_date']
                c.coord('file_pert').points = c.coord('file_pert').points.astype(numpy.dtype('<U27'), casting='safe')

            if cubes:
                cube = cubes.concatenate_cube()
                all_cubes.append(cube)

        single_cube = all_cubes.concatenate_cube()
        sbatch = batch_name_dict[batch2merge]
        outf = os.path.join(outdir, sbatch, region, name_dict[var], '%s_%s_%s_%s.nc' % (sbatch, combo, name_dict[var], region))
        print(outf)
        outd = os.path.dirname(outf)
        if not os.path.exists(outd):
            os.makedirs(outd)
# remove duplicates across batches here for monthly precip as will be used later for other variables
        if var == 'item5216_monthly_mean':
            single_cube = remove_duplicates(single_cube)
        else:
            fprmon = os.path.join(outdir, sbatch, 'UK', name_dict['item5216_monthly_mean'], '%s_%s_%s_%s.nc' % (sbatch, combo, name_dict['item5216_monthly_mean'], 'UK'))
            ok_ids = iris.load_cube(fprmon).coord('ensemble_member_id').points.tolist()
            single_cube = single_cube.extract(iris.Constraint(ensemble_member_id=ok_ids))
        iris.save(single_cube, outf)

else:
    all_files = list()
    all_cubes = iris.cube.CubeList()
    for ib, b in enumerate(batch_dict[batch2merge]):
        ibatch = int(b.replace('batch_', ''))
        sstring = os.path.join(indir, b, 'region', 'merged', version, '*%s*.nc' % name_dict[var])
        files = sorted(glob.glob(sstring))
        all_files += files
        cubes = iris.cube.CubeList([extractfn(c) for c in iris.load(files)])
        for c in cubes:
            ecoord = c.coord('ensemble_member_id')
            new_coord = ecoord.copy(points=ecoord.points + ibatch * 10000)
            c.replace_coord(new_coord)
            batchid_auxcoord = iris.coords.AuxCoord([str(c.attributes['batchid'])] * c.shape[0], long_name='batchid')
            c.add_aux_coord(batchid_auxcoord, 0)
            del c.attributes['batchid'], c.attributes['creation_date']
            c.coord('file_pert').points = c.coord('file_pert').points.astype(numpy.dtype('<U27'), casting='safe')

        cube = cubes.concatenate_cube()
        all_cubes.append(cube)

    single_cube = all_cubes.concatenate_cube()

    sbatch = batch_name_dict[batch2merge]
    if var == 'item5216_monthly_mean':
        single_cube = remove_duplicates(single_cube)
    else:
        fprmon = os.path.join(outdir, sbatch, 'UK', name_dict['item5216_monthly_mean'], '%s_%s_%s_members*.nc' % (sbatch, name_dict['item5216_monthly_mean'], 'UK'))
        ok_ids = iris.load_cube(fprmon).coord('ensemble_member_id').points.tolist()
        single_cube = single_cube.extract(iris.Constraint(ensemble_member_id=ok_ids))

    outf = os.path.join(outdir, sbatch, region, name_dict[var], '%s_%s_%s.nc' % (sbatch, name_dict[var], region))
    outd = os.path.dirname(outf)
    if not os.path.exists(outd):
        os.makedirs(outd)
    if region in regions_not_to_split:
        outf = outf.replace('.nc', '_members0000-%.4i.nc' % (single_cube.shape[0] - 1))
        iris.save(single_cube, outf)
    else:
        save_data_in_chunks(single_cube, outd, sbatch, name_dict[var], region, nchunk=100)

    print(outf)

#raise Exception('need to sort out rip_code and season_year')

print('Completed')

    

