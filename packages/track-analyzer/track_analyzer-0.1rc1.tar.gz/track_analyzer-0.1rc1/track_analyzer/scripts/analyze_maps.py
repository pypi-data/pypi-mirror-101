##########################################################################
# Track Analyzer - Quantification and visualization of tracking data     #
# Authors: Arthur Michaut                                                #
# Copyright 2016-2019 Harvard Medical School and Brigham and             #
#                          Women's Hospital                              #
# Copyright 2019-2021 Institut Pasteur and CNRS–UMR3738                  #
# See the COPYRIGHT file for details                                     #
#                                                                        #
# This file is part of Track Analyzer package.                           #
#                                                                        #
# Track Analyzer is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# Track Analyzer is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
# GNU General Public License for more details .                          #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with Track Analyzer (COPYING).                                   #
# If not, see <https://www.gnu.org/licenses/>.                           #
##########################################################################

import os.path as osp
import sys
import argparse

import matplotlib.pyplot as plt
import seaborn as sns

from track_analyzer import prepare as tpr
from track_analyzer import plotting as tpl
from track_analyzer import calculate as tca

def make_map_config(data_dir=None,export_config=True):
    """
    Generate a list of dictionaries containing the parameters used to run map_analysis.
    """

    # config to create grid using prepare.make_grid()
    grid_param = {'x_num': 10, # number of cells along x axis
                  'y_num': None, # number of cells along y axis
                  'cell_size': None, # size of a cell (=a square) in px or in unit if scaled is True
                  'scaled': False, # boolean to use scaled length of cell_size
                  'origin': None, # position of the grid (that is smaller or equal to image size). can be: 'center',"left-bottom","center-bottom","right-bottom","right-center","right-top","center-top","left-top","left-center"
                  'plot_grid': False # boolean to plot a representation of the grid
                  }

    # general config for plotting maps 
    map_param = { 'no_bkg': False, # boolean to remove background picture
                  'size_factor': 1., # size factor to tune relative size of arrows on vector plots
                  'show_axis': False, # boolean to show plot axes
                  'export_field': False, # export field points to txt files
                  'temporal_average': 0, # number of frame to average map values over 
                  'cmap': "plasma" # color map for scalar fields
                }

    # config of scalar field to plot. Each key is a parameter to plot and it stores a dict containing the plotting config for this specific parameter
    scalar_fields = {'vx': {'vlim': None, # value limits to display on the color map
                            'cmap': "plasma" # color map
                            }
                    }

    # config of vector field to plot. Each key is a parameter to plot and it stores a dict containing the plotting config for this specific parameter
    vector_fields = {'v': {'vlim': None, # value limits to display on the color map
                          'plot_on': 'v', # parameter of the scalar map to plot on. If None, don't plot on scalar map
                          'cmap': "plasma" # color map
                          }
                    }

    # config of vector average. Each key is a parameter to plot and it stores a dict containing the plotting config for this specific parameter
    vector_mean = {'v_mean': {'vlim': None, # value limits to display on the color map
                          'dimensions': ['x', 'y', 'z'], # dimension to compute the average on
                          'cmap': "plasma" # color map
                          }
                  }


    # package all in a dict
    config = {'grid_param': grid_param,
              'map_param': map_param,
              'scalar_fields': scalar_fields,
              'vector_fields': vector_fields,
              'vector_mean': vector_mean
              }

    if export_config:
        if data_dir is None:
            print("ERROR: no data_dir given")
        else:
            config_dir = osp.join(data_dir,'config')
            tpr.safe_mkdir(config_dir)

            for key in config.keys():
                fn = osp.join(config_dir,key+'.csv')
                tpr.write_dict(config[key],fn)

    return config


def map_analysis(data_dir, data=None, image=None, refresh=False,parallelize=False,filters=None,
                 plot_config=None, map_config=None):
    """Container method to plot a series of maps given by field_values. Manual vlim to colormap can be passed."""

    map_dir = osp.join(data_dir, 'map_analysis')
    tpr.safe_mkdir(map_dir)

    ### Get data

    data = tpr.get_data(data_dir, refresh=refresh) if data is None else data
    image = tpr.get_image(data_dir) if image is None else image

    df = data['df']
    dim = data['dim']
    dimensions = data['dimensions']
    lengthscale = data['lengthscale']
    timescale = data['timescale']

    ### Get config

    plot_config = tpl.make_plot_config() if plot_config is None else plot_config

    map_config_default = make_map_config(data_dir=data_dir,export_config=False)
    map_config = map_config_default if map_config is None else map_config
    
    # check that all configs are in map_confign, if not load default
    for key in ["grid_param","map_param","scalar_fields","vector_fields","vector_mean"]:
        if key not in map_config.keys():
            map_config[key] = map_config_default[key]

    grid_param = map_config["grid_param"]
    map_param = map_config["map_param"]
    scalar_fields = map_config["scalar_fields"]
    vector_fields = map_config["vector_fields"]
    vector_mean = map_config["vector_mean"]

    ### Filter data

    filters = tpr.init_filters() if filters is None else filters
    filters = [filters] if type(filters) is dict else filters  # if only one set of filters make it a list
    df_list, ROI_list = tpr.select_sub_data(df, image=image, filters=filters)


    ### Make grid
    image_size = [image['image_size'][1], image['image_size'][0]] #image width,image height in px
    grids = tpr.make_grid(image_size, 
                          x_num=grid_param['x_num'], 
                          y_num=grid_param['y_num'],
                          cell_size=grid_param['cell_size'], 
                          scaled=grid_param['scaled'], 
                          lengthscale=lengthscale, 
                          origin=grid_param['origin'], 
                          plot_grid=grid_param['plot_grid'],
                          save_plot_fn=osp.join(map_dir,'grids{}'.format(plot_config['format'])))

    ### compute fields
    for i, df in enumerate(df_list):
        print(r"Analyzing subset {}  ".format(i))
        sub_dir = osp.join(map_dir, '{}'.format(len(tpr.listdir_nohidden(map_dir)) + 1))
        tpr.safe_mkdir(sub_dir)
        # export data
        csv_fn = osp.join(sub_dir, 'all_data.csv')
        df.to_csv(csv_fn)

        # list required fields to interpolate
        all_fields = list(set(list(scalar_fields.keys()) + list(vector_fields.keys()) + list(vector_mean.keys())))
        interp_fields = [f for f in all_fields if f not in ['div', 'curl', 'v_mean', 'a_mean']]  # fields to interpolate
        vel_fields = ['v' + d for d in dimensions]
        acc_fields = ['a' + d for d in dimensions]

        if 'div' in all_fields or 'curl' in all_fields or 'v_mean' in all_fields or 'v' in vector_fields.keys():  # add all velocity fields
            for vf in vel_fields:
                if vf not in interp_fields:
                    interp_fields.append(vf)
        if 'a_mean' in all_fields or 'a' in vector_fields.keys():  # add all acceleration fields
            for af in acc_fields:
                if af not in interp_fields:
                    interp_fields.append(af)

        # compute data
        field_data = tca.interpolate_all_fields(data_dir, df, grids, field_values=interp_fields,
                                                temporal_average=map_param['temporal_average'],
                                                export_field=map_param['export_field'], outdir=sub_dir)
        if 'div' in all_fields or 'curl' in all_fields:
            field_data = tca.compute_all_div_curl(data_dir, df, field_data, lengthscale,
                                                  export_field=map_param['export_field'], outdir=sub_dir)
        for mf in ['v_mean', 'a_mean']:
            if mf in all_fields:
                field_data = tca.compute_all_vector_mean(data_dir, df, field_data, mf,
                                                         dimensions=vector_mean[mf]['dimensions'],
                                                         export_field=map_param['export_field'], outdir=sub_dir)

        # plot data
        scalar_fields_ = {**scalar_fields, **vector_mean}  # merge scalar data in one single dict
        for field in scalar_fields_.keys():
            plot_dir = osp.join(sub_dir, field)
            tpr.safe_mkdir(plot_dir)
            map_param_ = dict(map_param)
            map_param_['vlim'] = scalar_fields_[field]['vlim']
            map_param_['cmap'] = scalar_fields_[field]['cmap']
            tpl.plot_all_scalar_fields(data_dir, df, field_data, field, image=image, map_param=map_param_,
                                       plot_dir=plot_dir, plot_config=plot_config, dont_print_count=False)
        for field in vector_fields.keys():
            plot_dir = osp.join(sub_dir, field)
            tpr.safe_mkdir(plot_dir)
            map_param_ = dict(map_param)
            map_param_['vlim'] = vector_fields[field]['vlim']
            tpl.plot_all_vector_fields(data_dir, df, field_data, field, image=image, plot_on_field=vector_fields[field],
                                       dim=3, map_param=map_param_, plot_dir=plot_dir, plot_config=plot_config,
                                       dont_print_count=False)

    return df_list

def parse_args(args=None):
    """
    parse arguments for main()
    """

#    description = """Analyze trajectories 
#                Argument : 
#                - 
#                """

#    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=description)
    parser = argparse.ArgumentParser()

    parser.add_argument('data_dir',
                        help='path of the data directory')

    parser.add_argument('-r','--refresh',
                        action="store_true",
                        default=False,
                        help='refresh database')

    parser.add_argument('-p','--parallelize',
                        action="store_true",
                        default=False,
                        help=argparse.SUPPRESS)

    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='Increase verbosity of output')
    
    parsed_args = parser.parse_args(args)

    return parsed_args


def main(args=None):
    """ main function to run traj_analysis from command line"""

    args = sys.argv[1:] if args is None else args
    parsed_args = parse_args(args)

    data_dir = osp.realpath(parsed_args.data_dir)
    refresh = parsed_args.refresh
    parallelize = parsed_args.parallelize

    if not osp.exists(data_dir):
        raise Exception("ERROR: the passed data directory does not exist. Aborting...")

    if not osp.isdir(data_dir): 
        raise Exception("ERROR: the passed data directory is not a directory. Aborting...")

    # Load config
    config = tpr.load_config(data_dir,verbose=parsed_args.verbose)

    # Check config
    mandatory_config = ["filters","plot_config"]
    for key in mandatory_config:
        if key not in config.keys():
            config[key] = None

    # get traj_config
    map_config = {}
    for key in ["grid_param","map_param","scalar_fields","vector_fields","vector_mean"]:
        if key in config.keys():
            map_config[key] = config[key]

    # run analysis
    map_analysis(data_dir, 
                refresh=refresh,
                parallelize=parallelize,
                filters=config["filters"],
                plot_config=config["plot_config"],
                map_config=map_config)

if __name__ == '__main__':
    main()
