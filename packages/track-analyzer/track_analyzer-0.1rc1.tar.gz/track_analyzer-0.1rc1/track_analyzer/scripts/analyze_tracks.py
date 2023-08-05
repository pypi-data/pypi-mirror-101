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

from track_analyzer import prepare as tpr
from track_analyzer import plotting as tpl
from track_analyzer import calculate as tca


def make_traj_config(data_dir=None,export_config=True):
    """
    Generate a list of dictionaries containing the parameters used to run traj_analysis.
    """

    traj_config_ = {'run': True,  # run plot_traj
                   'color_code': 'z',  # color code: 'z', 'ROI', 'random', 'none'
                   'cmap' : 'plasma', # colormap to be used if color_code is 'z' 
                   'cmap_lim': None,  # pass custom colormap limits (useful for getting coherent boundaries for all frames)
                   'show_tail': True,  # show trajectory tail
                   'hide_labels': True,  # hide trajectory ID
                   'lab_size': 6,  # label size in points if hide_labels is False
                   'no_bkg': False,  # don't show background image if an image is passed
                   'size_factor': 1.,  # to multiply the default size of markers and lines
                   'show_axis': False,  # to show the plot axes (by default just image)
                   'plot3D': False,  # plot in 3D
                   'elevation': None,  # 3D paramater
                   'angle': None  # 3D paramater
                   }

    MSD_config = {'run': True,  # run plot_all_MSD
                  'MSD_model': "biased_diff",  # fitting model: 'PRW', 'biased_diff', "pure_diff", None (if not fitting)
                  'dim': 2,  # dimension to compute MSD (doesn't have to match the data dimensions)
                  'fitrange': None,  # fitrange list boundaries of the fit: [low_bound,high_bound]. If a bound is
                  # None, the extremum is taken
                  'plot_all_MSD': True,  # plot MSD altogether
                  'plot_single_MSD': False,  # plot MSD individually
                  'logplot_x': True,  # plot in log along x axis
                  'logplot_y': True,  # plot in log along y axis
                  'alpha': 0.2  # transparency of individual plots when all plotted together
                  }

    scatter_config = {'run': True,  # run param_vs_param
                      'couple_list': [['x', 'v'], ['y', 'v']],
                      # list of [x,y] couples of variables to be plotted in scatter
                      'mean_couple_list': [['x', 'v'], ['y', 'v']]
                      # list of [x,y] couples of variables averaged along the whole track to be plotted in scatter
                      }

    hist_config = {'run': True,  # run plot_param_hist
                   'var_list': ['v'],  # list of variables to be plotted in histogram
                   'mean_var_list': ['v']
                   # list of variables averaged along the whole track to be plotted in histogram
                   }

    centered_traj_config = {'run': True,  # run plot_centered_traj
                            'hide_labels': False,  # hide trajectory ID
                            'label_size': 5,  # label size in points if hide_labels is False
                            'dont_center': False,  # to keep initial position at its true position
                            'set_axis_lim': None,  # custom axis limites: [xmin,xmax,ymin,ymax]
                            'equal_axis' : True, # set x and y axes' scaling equal 
                            'color_code': 'random',  # color code: 'z', 'ROI', 'random', 'none'
                            'cmap' : 'plasma', # colormap to be used if color_code is 'z' 
                            'z_lim' : None      # z limits to be used if color_code is 'z'
                            }

    # package all in a dict
    config = {'traj_config_': traj_config_,
              'MSD_config': MSD_config,
              'scatter_config': scatter_config,
              'hist_config': hist_config,
              'centered_traj_config': centered_traj_config
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


def traj_analysis(data_dir, data=None, image=None, refresh=False, parallelize=False, filters=None, plot_config=None,
                  traj_config=None):
    """Container method to run analysis related to cell trajectories."""

    traj_dir = osp.join(data_dir, 'traj_analysis')
    tpr.safe_mkdir(traj_dir)

    ### Get data

    data = tpr.get_data(data_dir, refresh=refresh) if data is None else data
    image = tpr.get_image(data_dir) if image is None else image

    df = data['df']
    dim = data['dim']
    dimensions = data['dimensions']

    ### Get config

    plot_config = tpl.make_plot_config() if plot_config is None else plot_config

    traj_config_default = make_traj_config(data_dir=data_dir,export_config=False)
    traj_config = traj_config_default if traj_config is None else traj_config
    
    # check that all configs are in traj_confign, if not load default
    for key in ["traj_config_","MSD_config","scatter_config","hist_config","centered_traj_config"]:
        if key not in traj_config.keys():
            traj_config[key] = traj_config_default[key]

    traj_config_ = traj_config["traj_config_"]
    MSD_config = traj_config["MSD_config"]
    scatter_config = traj_config["scatter_config"]
    hist_config = traj_config["hist_config"]
    centered_traj_config = traj_config["centered_traj_config"]

    ### Filter data

    filters = tpr.init_filters() if filters is None else filters
    filters = [filters] if type(filters) is dict else filters  # if only one set of filters make it a list
    df_list, ROI_list = tpr.select_sub_data(df, image=image, filters=filters)

    ### Run analysis
    for i, df in enumerate(df_list):
        dir_name = '_' + filters[i]['name'] if filters[i]['name'] != '' else ''
        dir_name_ = '{}{}'.format(len(tpr.listdir_nohidden(traj_dir)) + 1, dir_name)

        print(r"Analyzing subset #{}, named: {}".format(i + 1, dir_name_))
        sub_dir = osp.join(traj_dir, dir_name_)
        sub_dir = sub_dir + '_1' if osp.exists(sub_dir) else sub_dir  # dont overwrite existing dir
        tpr.safe_mkdir(sub_dir)

        # export data
        # export filtered positions
        csv_fn = osp.join(sub_dir, 'all_data.csv')
        df.to_csv(csv_fn)

        # compute mean track properties
        mean_fn = osp.join(sub_dir, 'track_prop.csv')
        df_prop = tca.compute_track_prop(df, dimensions)
        df_prop.to_csv(mean_fn)

        # save pipeline parameters
        filename = osp.join(sub_dir, 'analysis_parameters.csv')
        if filters[i]['ROI'] is not None:
            filters[i]['ROI']['coord'] = ROI_list[i]
        params_d = [filters[i], traj_config_, MSD_config, plot_config]
        params_n = ['filters', 'traj parameters', 'MSD parameters', 'plotting parameters']
        tpr.write_dict(params_d, filename, dict_names=params_n)

        if traj_config_['run']:
            print("Plotting trajectories...")
            tpl.plot_all_traj(data_dir, df, image=image, traj_parameters=traj_config_, parallelize=parallelize,
                              dim=dim, plot_dir=sub_dir, plot_config=plot_config)

        if MSD_config['run']:
            print("MSD analysis...")
            MSD_dir = tpr.safe_mkdir(osp.join(sub_dir, 'MSD'))
            df_prop = tpl.plot_all_MSD(data_dir, df, df_out=df_prop, fit_model=MSD_config['MSD_model'],
                                       MSD_parameters=MSD_config, plot_config=plot_config, plot_dir=MSD_dir)
            df_prop.to_csv(mean_fn)

        if hist_config['run']:
            if len(hist_config['var_list']) > 0:
                print("Plotting parameters histograms...")
            for p in hist_config['var_list']:
                tpl.plot_param_hist(data_dir, p, df, plot_config=plot_config, plot_dir=sub_dir)

            if len(hist_config['mean_var_list']) > 0:
                print("Plotting whole-track histograms...")
            for p in hist_config['mean_var_list']:
                tpl.plot_param_hist(data_dir, p, df_prop, plot_config=plot_config, plot_dir=sub_dir, prefix='track_')

        if scatter_config['run']:
            if len(scatter_config['couple_list']) > 0:
                print("Plotting couples of parameters...")
            for param_vs_param in scatter_config['couple_list']:
                x_param, y_param = param_vs_param
                tpl.plot_param_vs_param(data_dir, x_param, y_param, df, plot_dir=sub_dir, plot_config=plot_config)

            if len(scatter_config['mean_couple_list']) > 0:
                print("Plotting couples of whole-track parameters...")
            for param_vs_param in scatter_config['mean_couple_list']:
                x_param, y_param = param_vs_param
                tpl.plot_param_vs_param(data_dir, x_param, y_param, df_prop, plot_dir=sub_dir, plot_config=plot_config,
                                        prefix='track_')

        if centered_traj_config['run']:
            print("Plotting centered trajectories")
            tpl.plot_centered_traj(data_dir, df, dim=dim, plot_dir=sub_dir, plot_config=plot_config,
                                   specific_config=centered_traj_config)

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
    traj_config = {}
    for key in ["traj_config_","MSD_config","scatter_config","hist_config","centered_traj_config"]:
        if key in config.keys():
            traj_config[key] = config[key]

    # run analysis
    traj_analysis(data_dir, 
                refresh=refresh,
                parallelize=parallelize,
                filters=config["filters"],
                plot_config=config["plot_config"],
                traj_config=traj_config)

if __name__ == '__main__':
    main()
