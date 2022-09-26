import os, sys, glob
import datetime, time
import numpy
import iris
import iris.coord_categorisation
from copy import deepcopy


def decode(s):
    digits='0123456789abcdefghijklmnopqrstuvwxyz'
    n = len(digits)
    items = [digits.index(i) for i in s[1:]]
    items = [items[0] * n * n , items[1] * n, items[2]]
    return sum(items)



version = '20220107'

batch_dict = {'886': 'wet',
              '883': 'hot',
              '887': 'hot',
              '882': 'baseline',
              '877': 'baseline-prototype',
              '878': 'hot-prototype',
              '879': 'wet-prototype',
              '896': 'hot',
              '897': 'wet',
              '898': 'hot'}


#item16222_daily_mean	item3236_daily_minimum	item3249_daily_mean	item5216_monthly_mean
#item3236_daily_maximum	item3245_daily_mean	item5216_6hrly_mean	item8234_daily_mean
#item3236_daily_mean	item3249_6hrly_maximum	item5216_daily_maximum	item8235_daily_mean

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

if len(sys.argv) == 3:
   indir = '/ExSamples/netcdf/%s/region/%s' % (sys.argv[1], sys.argv[2])
else:
    indir = '/ExSamples/netcdf/batch_878/region/item1235_daily_mean'
outdir = os.path.join(os.path.dirname(indir), 'merged', version)
#collection = 'land-gcm'
domain = 'global'
resolution = '60km'
#frequency = 'mon'
scenario = 'RCP85'
#time_period = '189912-209911'
ukcp18_version = 'v20180825'


if not os.path.exists(outdir):
    try:
        os.makedirs(outdir)
    except:
        pass                 # probably been made by another parallel batch job

f = glob.glob(os.path.join(indir, '*.nc'))
f = sorted(f)     #[:1000]

#raise Exception('stop here')

batch = [i[-3:] for i in os.path.dirname(indir).split('/') if 'batch' in i][0]

a = iris.load(f)
a.sort(key=lambda x: decode(x.attributes['exptid']))
#print(a)

#raise Exception('stop here')





ans_ = iris.cube.CubeList()
for i in a:
    ii = iris.util.new_axis(i)
    ensemble_member_dimcoord = iris.coords.DimCoord(numpy.array([decode(i.attributes['exptid'])]), long_name='ensemble_member_id')
    exptid_auxcoord = iris.coords.AuxCoord([str(i.attributes['exptid'])], long_name='exptid')
    expturl_auxcoord = iris.coords.AuxCoord([str(i.attributes['EXPTURL'])], long_name='expturl')
    workunit_auxcoord = iris.coords.AuxCoord([str(i.attributes['workunit_name'])], long_name='workunit_name')
    file_atmos_auxcoord = iris.coords.AuxCoord([str(i.attributes['file_atmos'])], long_name='file_atmos')
    file_pert_auxcoord = iris.coords.AuxCoord([str(i.attributes['file_pert'])], long_name='file_pert')
    file_sst_auxcoord = iris.coords.AuxCoord([str(i.attributes['file_sst'])], long_name='file_sst')
    file_sice_auxcoord = iris.coords.AuxCoord([str(i.attributes['file_sice'])], long_name='file_sice')
    file_ozone_auxcoord = iris.coords.AuxCoord([str(i.attributes['file_ozone'])], long_name='file_ozone')
    file_so2dms_auxcoord = iris.coords.AuxCoord([str(i.attributes['file_so2dms'])], long_name='file_so2dms')
    rip = str(i.attributes['file_sst']).split('_')[1]
    rip_auxcoord = iris.coords.AuxCoord([rip], long_name='rip_code')
    ii.add_dim_coord(ensemble_member_dimcoord, 0)
    ii.add_aux_coord(exptid_auxcoord, 0)
    ii.add_aux_coord(expturl_auxcoord, 0)
    ii.add_aux_coord(file_atmos_auxcoord, 0)
    ii.add_aux_coord(file_pert_auxcoord, 0)
    ii.add_aux_coord(file_sst_auxcoord, 0)
    ii.add_aux_coord(file_sice_auxcoord, 0)
    ii.add_aux_coord(file_so2dms_auxcoord, 0)
    ii.add_aux_coord(file_ozone_auxcoord, 0)
    ii.add_aux_coord(rip_auxcoord, 0)
    ii.add_aux_coord(workunit_auxcoord, 0)
    ans_.append(ii)
    del ii.attributes['exptid'], ii.attributes['workunit_name'], ii.attributes['EXPTURL'], ii.attributes['file_atmos']
    del ii.attributes['file_sst'], ii.attributes['file_sice'], ii.attributes['file_pert']
    del ii.attributes['file_so2dms'], ii.attributes['file_ozone']



global_attrs = dict(contact='david.sexton@metoffice.gov.uk',
#                    collection=collection,
                    domain=domain,
#                            frequency=frequency,
                    institution='climatepredicton.net / Met Office Hadley Centre',
                    institution_id='climateprediction.net / MOHC',
                    project='ExSamples',
                    references='None yet',
                    resolution=resolution,
                    scenario=scenario,
#                    source='Realisations of future winters conditioned on SSTs and sea ice from UKCP18 Global projections',
#                    title='ExSamples realisations',
                    ukcp18_version=ukcp18_version,
#                    plot_label=plot_label,
#                    label_units=label_units,
#                    description=description,
                    creation_date=datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S'))

def get_ukcp_description(cube):
    rip = str(cube.coord('file_sst').points[0]).split('_')[1]
    syr = cube.coord('season_year').points[0]
    if 'baseline' in batch_dict[cube.attributes['batchid']]:
        return '%s-%.4i' % (rip, syr)
    else:
        return '%s-%.4i' % (rip, syr)

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

def save_data_in_chunks(cube, outdir, var, batch, nchunk=20, replace=None):
    reduced = remove_duplicates(cube)
    n = reduced.shape[0]
    name = name_dict[var]
    if replace is not None:
        name = name.replace(*replace)
    if n < (2 * nchunk):
        outf = os.path.join(outdir, '%s_%s_%s.nc' % (get_ukcp_description(reduced), batch_dict[batch], name))
        print('Saving to %s' % outf)
        iris.save(reduced, outf) #, zlib=True, complevel=3, shuffle=True)
    else:
        index = list(range(n))
        nchunks = n // nchunk
        if n % nchunk > 0:
            nchunks += 1
        for i in numpy.array_split(index, nchunks):
            c = reduced[i]
            member_str = 'members%.4i-%.4i' % (min(i), max(i))
            outf = os.path.join(outdir, '%s_%s_%s_%s.nc' % (get_ukcp_description(c), batch_dict[batch], name, member_str))
            print('Saving to %s' % outf)
            iris.save(c, outf) #, zlib=True, complevel=3, shuffle=True)
 
            
var = os.path.basename(indir)
if '6hrly' in var:
    NCHUNK = 10
elif 'daily' in var:
    NCHUNK = 20
else:
    NCHUNK = 250


if batch in ['877', '882']:
    sstv = [str(i.coord('file_sst').points[0]).split('_')[1] for i in ans_]
    uv = numpy.unique(sstv)
    for v in uv:
        ans__ = iris.cube.CubeList([i for i, sstv_ in zip(ans_, sstv) if sstv_ == v])
        for i in ans__:
            i.attributes.update(global_attrs)
# in the baseline, this should be length 10, one for each year of the baseline
        ans__ = ans__.concatenate()
        for i in ans__:
            iris.coord_categorisation.add_day_of_month(i, 'time')
            iris.coord_categorisation.add_day_of_year(i, 'time')
            iris.coord_categorisation.add_season_year(i, 'time')
            iris.coord_categorisation.add_year(i, 'time')
            iris.coord_categorisation.add_month_number(i, 'time')
            iris.coord_categorisation.add_hour(i, 'time')
        ans = ans__


        for c in ans:
            save_data_in_chunks(c, outdir, var, batch, nchunk=NCHUNK)

        if '6hrly' in var:
            print('Making daily from 6-hourly as well...')
            aggregator = agg_dict[var.split('_')[-1]]
            ans2 = iris.cube.CubeList([i.aggregated_by('day_of_year', aggregator) for i in ans])
            for c in ans2:
                save_data_in_chunks(c, outdir, var, batch, nchunk=NCHUNK, replace=('6hrly', 'daily'))

else:

    if var != 'item5216_monthly_mean':

        monthly_files = sorted(glob.glob('/ExSamples/netcdf/batch_%s/region/merged/%s/*_pr_monthly*.nc' % (batch, version)))


        monthly_cubes = iris.load(monthly_files)
        monthly_cube = monthly_cubes.concatenate_cube()
        usable_member_ids = monthly_cube.coord('ensemble_member_id').points.tolist()

    # remove need for duplication check by using ids that were valid for monthly data
        ans_ = ans_.extract(iris.Constraint(ensemble_member_id=usable_member_ids))
    
# now loop in chunks, concatenate and write file and calculate daily while at it and write that out
#    raise Exception('pause')

    n = len(ans_)
    index = list(range(n))
    nchunks = n // NCHUNK
    if n % NCHUNK > 0:
        nchunks += 1
    for ind in numpy.array_split(index, nchunks):
        print(ind)
        ans__ = iris.cube.CubeList([ans_[i] for i in ind])
        try:
            ans = ans__.concatenate_cube()
        except:
            ans = ans__.merge_cube()
        ans.attributes.update(global_attrs)

        iris.coord_categorisation.add_day_of_month(ans, 'time')
        iris.coord_categorisation.add_day_of_year(ans, 'time')
        iris.coord_categorisation.add_season_year(ans, 'time')
        iris.coord_categorisation.add_year(ans, 'time')
        iris.coord_categorisation.add_month_number(ans, 'time')
        iris.coord_categorisation.add_hour(ans, 'time')

        member_str = 'members%.4i-%.4i' % (min(ind), max(ind))
        outf = os.path.join(outdir, '%s_%s_%s_%s.nc' % (get_ukcp_description(ans), batch_dict[batch], name_dict[var], member_str))
        print('Saving to %s' % outf)
        iris.save(ans, outf)

        if '6hrly' in var:
            aggregator = agg_dict[var.split('_')[-1]]
            ans2 = ans.aggregated_by('day_of_year', aggregator)
            outf2 = outf.replace('6hrly', 'daily')
            iris.save(ans2, outf2)
            print('Writing to %s' % outf2) 




print('Completed')


