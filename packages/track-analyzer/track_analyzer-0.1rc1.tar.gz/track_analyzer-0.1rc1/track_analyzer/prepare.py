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

import os
import os.path as osp
import csv

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
import pickle
import seaborn as sns
from lmfit import Parameters, Model
from scipy.optimize import curve_fit
import napari
from skimage import io
from skimage.color import rgb2gray
from skimage.util import img_as_ubyte
import tifffile as tifff

from track_analyzer import plotting as tpl
from track_analyzer import calculate as tca

# Plotting parameters
color_list = [c['color'] for c in list(plt.rcParams['axes.prop_cycle'])] + sns.color_palette("Set1", n_colors=9,
                                                                                             desat=.5)
plot_param = {'figsize': (5, 5), 'dpi': 300, 'color_list': color_list, 'format': '.png', 'despine': True, 'logx': False,
              'logy': False, 'invert_yaxis': True, 'export_data_pts': False}


def show_usage():
    """Print usage (outdated)"""
    usage_message = """Usage: \n- plot cells analysis using cell_analysis(data_dir,refresh,parallelize,plot_traj,hide_labels,transform_coord,no_bkg,linewidth,plot3D,min_traj_len,frame_subset,redchi_th) \t data_dir: data directory, refresh (default False) to refresh the table values, parallelize (default False) to run analyses in parallel, 
    plot_traj (default true) to print the cell trajectories, hide_labels (default True) to hide the cell label, no_bkg (default False) to remove the image background, linewidth being the trajectories width (default=1.0), frame_subset: to plot only on a subset of frames [first,last], transform_coord: transform coordinates using coord_transformation.csv file (default: False),split_MSD_analysis: wraper function to split analysis of MSD in 30 frames chunks (default=True)\n
    - plot maps using map_analysis(data_dir,refresh,parallelize,x_grid_size,no_bkg,z0,dimensions,axis_on,plot_on_mean,black_arrows,export_field) \t data_dir: data directory, refresh (default False) to refresh the table values, parallelize (default False) to run analyses in parallel, 
    x_grid_size: number of columns in the grid (default 10), no_bkg (default False) to remove the image background, z0: altitude of the z_flow surface (default None => center of z axis), dimensions ([row,column] default None) to give the image dimension in case of no_bkg, axis_on: display axes along maps (default False),plot_on_mean: plot vfield on mean_vel map (default=True),
    black_arrows: don't use vz to color code vfield arrows (default=True), export_field: export velocity fields as txt files (default False) \n
    - plot average ROIs using avg_ROIs(data_dir,frame_subset=None,selection_frame=None,ROI_list=None,plot_on_map=True,plot_section=True,cumulative_plot=True,avg_plot=True) \t data_dir: data directory, frame_subset is a list [first,last], default None: open interactive choice \n
    - plot XY flow through a vertical surface defined by a XY line using XY_flow(data_dir,window_size=None,refresh=False,line=None,orientation=None,frame_subset=None,selection_frame=None,z_depth=None) \t data_dir: data directory, frame_subset is a list [first,last], default None: open interactive choice, window_size = rolling average window in um, default None => interactive choice \n
    - plot_centered_traj(data_dir,selection_frame=1,min_traj_len=1,frame_subset=None,force_max_frame=None,dont_center=False,hide_labels=False,transform_coord=False,refresh=False,set_axis_lim=None) \n
    - plot_vx_vs_vy(data_dir,transform_coord=False,refresh=False,select_ROI=True,set_axis_lim=None)"""
    print(usage_message)


def paper_style():
    mpl.rcParams.update(mpl.rcParamsDefault)  # ensure the default params are active
    sns.set_style("ticks")
    sns.set_context("paper", font_scale=2., rc={"lines.linewidth": 2, "lines.markersize": 9})


def get_cmap_color(value, colormap='plasma', vmin=None, vmax=None):
    colormap = plt.get_cmap(colormap)
    norm = plt.Normalize(vmin, vmax)
    return colormap(norm(value))


def listdir_nohidden(path):
    """List a directory without hidden files"""
    dir_list = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            dir_list.append(f)
    return dir_list


def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result


def safe_mkdir(dir_):
    if not osp.isdir(dir_):
        os.mkdir(dir_)
    return dir_


def get_param_time_der(param):
    """Find the time derivative of a parameter based on its name and return the raw param name"""
    if param.endswith('_dot'):
        return [param[:param.find('_dot')], 'first']
    elif param.endswith('_ddot'):
        return [param[:param.find('_ddot')], 'sec']
    else:
        return [param, None]


def make_unit_label(dimension='L', l_unit='um', t_unit='min'):
    """Make the Latex label of unit type depending on the dimension formula. Supported: L, LL, L/T, LL/T, L/TT, 1/L, 1/LL, T, 1/T"""
    l_unit_dict = {'um': r'\mu m', 'mm': r'mm', 'px': 'px', 'none': '', 'au': ''}
    t_unit_dict = {'min': r'min', 's': r's', 'frame': 'frame', 'none': '', 'au': ''}

    if dimension == 'L':
        label = l_unit_dict[l_unit]
    elif dimension == 'LL':
        label = l_unit_dict[l_unit] + r'^2'
    elif dimension == 'LL/T':
        label = l_unit_dict[l_unit] + r'^2.' + t_unit_dict[t_unit] + r'^{-1}'
    elif dimension == 'L/TT':
        label = l_unit_dict[l_unit] + r'.' + t_unit_dict[t_unit] + r'^{-2}'
    elif dimension == 'L/T':
        label = l_unit_dict[l_unit] + r'.' + t_unit_dict[t_unit] + r'^{-1}'
    elif dimension == '1/L':
        label = l_unit_dict[l_unit] + r'^{-1}'
    elif dimension == '1/LL':
        label = l_unit_dict[l_unit] + r'^{-2}'
    elif dimension == 'T':
        label = t_unit_dict[t_unit]
    elif dimension == '1/T':
        label = t_unit_dict[t_unit] + r'^{-1}'
    elif dimension == 'none':
        label = ''
    else:
        print('Warning: this unit is not supported')
        label = r''

    return label


def make_param_label(param, l_unit='um', t_unit='min', time_der=None, mean=False, only_symbol=False, only_unit=False):
    """Make a the Latex label of a parameter. The first and second time derivative and the mean symbol can be used."""
    symbol_dict = {'v': 'v', 'a': 'a', 'vx': 'v_x', 'vy': 'v_y', 'vz': 'v_z', 'ax': 'a_x', 'ay': 'a_y', 'az': 'a_z'}

    param_dict = {}
    for p in list('xyz'):
        param_dict[p] = {'sym': p, 'dim': 'L', 'l_unit': 'px', 't_unit': 'none', 'latex': True}
    for p in ['x_scaled', 'y_scaled', 'z_scaled', 'z_rel']:
        param_dict[p] = {'sym': p[0], 'dim': 'L', 'l_unit': l_unit, 't_unit': 'none', 'latex': True}
    for p in ['vx', 'vy', 'vz', 'v']:
        param_dict[p] = {'sym': symbol_dict[p], 'dim': 'L/T', 'l_unit': l_unit, 't_unit': t_unit, 'latex': True}
    for p in ['ax', 'ay', 'az', 'a']:
        param_dict[p] = {'sym': symbol_dict[p], 'dim': 'L/TT', 'l_unit': l_unit, 't_unit': t_unit, 'latex': True}
    param_dict['t'] = {'sym': 't', 'dim': 'T', 'l_unit': 'none', 't_unit': t_unit, 'latex': True}
    param_dict['frame'] = {'sym': 'frame', 'dim': 'T', 'l_unit': 'none', 't_unit': 'none', 'latex': True}
    param_dict['D'] = {'sym': 'D', 'dim': 'LL/T', 'l_unit': l_unit, 't_unit': t_unit, 'latex': True}
    param_dict['div'] = {'sym': 'div', 'dim': '1/T', 'l_unit': l_unit, 't_unit': t_unit, 'latex': True}
    param_dict['curl'] = {'sym': 'curl', 'dim': '1/T', 'l_unit': l_unit, 't_unit': t_unit, 'latex': True}
    param_dict['track_length'] = {'sym': 'track duration', 'dim': 'T', 'l_unit': l_unit, 't_unit': t_unit,
                                  'latex': False}
    param_dict['track'] = {'sym': 'track id', 'dim': 'none', 'l_unit': l_unit, 't_unit': t_unit, 'latex': False}

    # check if mean
    if param.endswith('_mean'):
        param = param[:param.find('_mean')]
        mean = True

    # convert param if it ends by _dot or _ddot
    raw_param, time_der_ = get_param_time_der(param)
    if time_der_ is not None:
        time_der = time_der_
        param = raw_param

    param_ = param_dict[param]['sym']
    dim_der = ''
    if time_der == 'first':
        param_ = r'\dot{' + param_ + r'}'
        dim_der = '/T'
    elif time_der == 'sec':
        param_ = r'\ddot{' + param_ + r'}'
        dim_der = '/TT'
    if mean:
        param_ = r'\langle ' + param_ + r' \rangle'

    unit_ = make_unit_label(param_dict[param]['dim'] + dim_der, l_unit=param_dict[param]['l_unit'],
                            t_unit=param_dict[param]['t_unit'])

    if param_dict[param]['latex']:
        if len(unit_) > 0:
            label = r'$' + param_ + r'$ ($' + unit_ + r'$)'
        else:
            label = r'$' + param_ + r'$'

        if only_symbol:
            return r'$' + param_ + r'$'

        if only_unit:
            return r'$' + unit_ + r'$'
    else:
        if len(unit_) > 0:
            label = param_ + ' (' + unit_ + ')'
        else:
            label = param_

        if only_symbol:
            return param_

        if only_unit:
            return unit_

    return label


def write_dict(dicts, filename, dict_names=None):
    """Write a dict or a list of dict into a csv file."""
    if type(dicts) is dict:
        dicts = [dicts]

    if type(dict_names) is list:
        if len(dicts) != len(dict_names):
            print("Warning: the name list doesn't match the dict list. Not printing names")
            dict_names = None

    with open(filename, "w+") as f:
        w = csv.writer(f)
        for i, d in enumerate(dicts):
            if type(d) is dict:
                if dict_names is not None:
                    f.write(dict_names[i] + '\n')
                for key, val in d.items():
                    w.writerow([key, val])
                f.write('\n')

def load_dict(filename):
    """Read a csv file and returns a converted dict"""
    if not filename.endswith('.csv'): 
        raise Exception("ERROR: No csv file passed. Aborting...")

    if not osp.exists(filename): 
        raise Exception("ERROR: File does not exist. Aborting...")

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {}
        for rows in reader:
            if len(rows)>0:
                if rows[1] == '':
                    mydict[rows[0]] = None
                else:
                    try: 
                        mydict[rows[0]] = eval(rows[1]) #if needs conversion
                    except:
                        mydict[rows[0]] = rows[1] #if string

    return mydict


def make_grid(image_size, x_num=None, y_num=None, cell_size=None, scaled=False, lengthscale=1., origin=None, plot_grid=False, save_plot_fn=None):
    """Make two meshgrids: a node_grid with the vertices of cells, and center_grid with the centers of the cells
    The meshsize can be defined by either the number of cells along one dimension (x or y), or the size of a cell (in px or scaled unit if scaled=True).
    If several definitions of meshsize are passed, by default the number of cells is used to ensure there is no conflict between definitons.
    If the grid does not cover the all image size it is cropped and centerd (if origin is None) or tethered to one of 8 positions (left-bottom,center-bottom,etc.)."""

    width, height = image_size

    # ensure there is no conflict by keeping only one definition (priority: x_num,y_num,cell_size)
    if [x_num, y_num, cell_size] == [None, None, None]:  # if no definition passed
        raise Exception("ERROR: cannot generate grids with no information. Aborting...")
    elif x_num is not None and y_num is not None and cell_size is not None:  # if three definitions, use x_num
        y_num = None
        cell_size = None
    elif x_num is not None and y_num is not None and cell_size is None:  # if x_num and y_num, use x_num
        y_num = None
    elif [x_num, y_num] != [None,
                            None] and cell_size is not None:  # if x_num or y_num and cell_size, use x_num or y_num
        cell_size = None

    # find definiton available
    definition = None
    if x_num is not None and y_num is None and cell_size is None:
        definition = 'x_num'
    elif x_num is None and y_num is not None and cell_size is None:
        definition = 'y_num'
    elif x_num is None and y_num is None and cell_size is not None:
        definition = 'cell_size'
    else:
        raise Exception("ERROR: defintion not found. Aborting...")

    # compute cell_size depending on the definition
    if definition == 'x_num':
        x_num = int(x_num)
        if x_num < 1:
            raise Exception("ERROR: x_num needs to be at least 1. Aborting...")
        cell_size_ = float(width) / (x_num + 1)  # so x_num is the number of cells along the dimension
    elif definition == 'y_num':
        y_num = int(y_num)
        if y_num < 1:
            raise Exception("ERROR: y_num needs to be at least 1. Aborting...")
        cell_size_ = float(height) / (y_num + 1)  # so y_num is the number of cells along the dimension
    elif definition == 'cell_size':
        cell_size_ = cell_size if not scaled else cell_size / lengthscale
        if cell_size_ > width or cell_size_ > height:
            raise Exception("ERROR: cell size larger than image size. Aborting...")

    x_array = np.arange(0, width + cell_size_, cell_size_)
    x_array = x_array[x_array < width]
    y_array = np.arange(0, height + cell_size_, cell_size_)
    y_array = y_array[y_array < height]
    x_edge = width - x_array.max()
    y_edge = height - y_array.max()

    if origin is None or origin == 'center':  # center
        x_array = x_array + x_edge / 2
        y_array = y_array + y_edge / 2
    elif origin == "left-bottom":
        pass  # nothing to change
    elif origin == "center-bottom":
        x_array = x_array + x_edge / 2
    elif origin == "right-bottom":
        x_array = x_array + x_edge
    elif origin == "right-center":
        x_array = x_array + x_edge
        y_array = y_array + y_edge / 2
    elif origin == "right-top":
        x_array = x_array + x_edge
        y_array = y_array + y_edge
    elif origin == "center-top":
        x_array = x_array + x_edge / 2
        y_array = y_array + y_edge
    elif origin == "left-top":
        y_array = y_array + y_edge
    elif origin == "left-center":
        y_array = y_array + y_edge / 2

    x_center = x_array + cell_size_ / 2
    y_center = y_array + cell_size_ / 2

    node_grid = np.meshgrid(x_array, y_array)
    center_grid = np.meshgrid(x_center[:-1], y_center[:-1])

    if plot_grid:
        X, Y = node_grid
        x, y = center_grid
        fig, ax = plt.subplots(1, 1, figsize=plot_param['figsize'])
        ax.set_aspect('equal')
        for i in range(len(x_array)):
            plt.plot([X[0, i], X[-1, i]], [Y[0, i], Y[-1, i]], color_list[0])  # plot vertical lines
        for i in range(len(y_array)):
            plt.plot([X[i, 0], X[i, -1]], [Y[i, 0], Y[i, -1]], color_list[0])  # plot horizontal lines
        plt.scatter(x, y, color=color_list[1])  # plot center of cells as dot
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        if save_plot_fn is not None:
            fig.savefig(save_plot_fn, dpi=plot_param['dpi'], bbox_inches='tight')
            plt.close(fig)

    return node_grid, center_grid


def fit_msd(msd, mean_vel=None, traj=None, dim=2, model_bounds={'P': [0, 300], 'D': [0, 1e8], 'v': [0, 1e8]}, model='biased_diff',fitrange=None, two_param_fit=False, print_traj_info=False):
    """Fit MSD with a random walk model: 'PRW' (persitent random walk), "pure_diff" (pure random walk), 'biased_diff' (biased randow walk for which the mean velocity is used to estimate the drift). 
    The range of the fit is given by fit range which is given in scaled lag times.
    two_param_fit can be used for the 'biased_diff' model but it is not recommended"""

    if fitrange is not None:
        if fitrange[0] is None and fitrange[1] is None:
            pass
        elif fitrange[0] is None or fitrange[1] is None:
            if fitrange[0] is not None:
                msd = msd[msd['tau'] >= fitrange[0]]
            elif fitrange[1] is not None:
                msd = msd[msd['tau'] <= fitrange[1]]
        else:
            msd = msd[((msd['tau'] >= fitrange[0]) & (msd['tau'] <= fitrange[1]))]

    # deprecated: to select with a range in percentage of time axis
    # elif type(fitrange[1]) is float:
    #     m=int(msd.shape[0]*fitrange[0])
    #     n=int(msd.shape[0]*fitrange[1])
    #     msd=msd.loc[range(m,n)]

    # lmfit model
    success = False
    if model is not None:
        if model != "pure_diff" and mean_vel is None:
            raise Exception("Error: mean_vel is required to fit with {}. Aborting...".format(model))
        if model == 'PRW':
            param_list = ['P']
            func = lambda t, P: 2 * (mean_vel ** 2) * P * (t - P * (1 - np.exp(-t / P)))
            func_model = Model(func)
            p = func_model.make_params(P=10)
            p['P'].set(min=model_bounds['P'][0], max=model_bounds['P'][1])
        elif model == 'biased_diff':
            if two_param_fit:  # two-parameter fit on D and v_mean
                param_list = ['D', 'v']
                func = lambda t, D, v: 2 * dim * D * t + v ** 2 * t ** 2
                func_model = Model(func)
                p = func_model.make_params(D=1, v=mean_vel)
                p['D'].set(min=model_bounds['D'][0])
                p['v'].set(min=model_bounds['v'][0])
            else:
                param_list = ['D']
                func = lambda t, D: 2 * dim * D * t + mean_vel ** 2 * t ** 2
                func_model = Model(func)
                p = func_model.make_params(D=1)
                p['D'].set(min=model_bounds['D'][0])
        elif model == "pure_diff":
            param_list = ['D']
            func = lambda t, D: 2 * dim * D * t
            func_model = Model(func)
            p = func_model.make_params(D=1)
            p['D'].set(min=model_bounds['D'][0])
        try:
            # msd['weights']=1./(msd['msd_std']+1) #to ensure no div by 0
            # best=func_model.fit(msd['msd'][0:n],t=msd['tau'][0:n],params=p)
            msd.dropna(inplace=True)
            # best=func_model.fit(msd['msd'][0:n],t=msd['tau'][0:n],params=p,weights=msd['weights'][0:n])
            best = func_model.fit(msd['msd'], t=msd['tau'], params=p)

            if best.success == False:
                print("WARNING: fit_msd failed")
            success = best.success
        except:
            success = False

    if success:
        redchi = best.redchi
        param_val = {param: best.best_values[param] for param in param_list}
        errors = [np.nan] * len(param_list)
        if best.covar is not None:
            errors = list(np.sqrt(best.covar).diagonal())
        fitted = func(msd['tau'], *best.best_values.values())
        fitted_df = pd.DataFrame({'fitted': fitted, 'tau': msd['tau']})
        results = {'success': success, 'param': param_val, 'errors': errors, 'redchi': redchi, 'fitted_df': fitted_df}

        if print_traj_info:
            traj_length = int(traj['t'].max() - traj['t'].min())
            speed_mean = traj['v'].mean()
            speed_std = traj['v'].std()
            print("traj: {:} \n  traj length: {:} min [{:},{:}]\n  traj speed: {:0.2f} +/- {:0.2f} um/min".format(
                int(track), int(traj_length), int(traj['frame'].min()), int(traj['frame'].max()), speed_mean,
                speed_std))
            print("FIT RESULTS:")
            print(param_list, ': ', param_val)
            print(param_list, ' errors: ', errors)
            print(redchi)
    else:
        results = {'success': success, 'param': None, 'errors': None, 'redchi': None, 'fitted_df': None}

    return results


def fit_lin(data, fitxrange=None, zero_intercept=False):
    """This function performs a linear fit. Some fitting range can be specified with fitxrange. It returns the fir parameters, the error the fitted curve in a list"""
    x0 = data[:, 0]
    # prepare subdata
    if fitxrange:
        if type(fitxrange) is list:
            xmin = fitxrange[0]
            xmax = fitxrange[1]
            if xmin is None:
                xmin = data[0, 0]
            if xmax is None:
                xmax = data[-1, 0]
        elif fitxrange <= 1:
            xmax = fitxrange * data[-1, 0]
            xmin = data[0, 0]
        else:
            print("WARNING: no valid fitxrange provided")
        data = data[(data[:, 0] <= xmax) & (data[:, 0] >= xmin)]

    # fit
    if zero_intercept:
        f = lambda x, a: a * x
    else:
        f = lambda x, a, b: a * x + b

    try:
        parameters, covar = curve_fit(f, data[:, 0], data[:, 1])
        if zero_intercept:
            fitted = f(data[:, 0], parameters[0])  # fitted y-data on the fitxrange interval
            fitted_ = np.array([data[:, 0], fitted]).T
            fitted_tot = f(x0, parameters[0])  # fitted y-data on the total interval
        else:
            fitted = f(data[:, 0], parameters[0], parameters[1])
            fitted_ = np.array([data[:, 0], fitted]).T
            fitted_tot = f(x0, parameters[0], parameters[1])
        # Rsquared
        ymean = 0 if zero_intercept else np.mean(data[:, 1])
        Stot = np.square(data[:, 1] - ymean).sum()
        Sres = np.square(data[:, 1] - fitted).sum()
        Rsq = 1 - Sres / Stot

        return [parameters, np.sqrt(np.diag(covar)), fitted_, Rsq, True]
    except RuntimeError:
        return [np.nan, np.nan, np.nan, False]


def pool_datasets(df_list, name_list):
    """Pool several dataframes together with a column identifying the datasets' names"""
    df_out = pd.DataFrame()

    for i, df in enumerate(df_list):
        if df is None:
            continue
        df['dataset'] = name_list[i]
        df_out = pd.concat([df_out, df])

    return df_out


def get_info(data_dir):
    """info.txt gives the lengthscale in um/px, the frame intervalle delta_t in min and the column names of the table"""
    filename = osp.join(data_dir, "info.txt")
    info = {}

    # list of parameters to grab
    string_list = ['length_unit', 'time_unit', 'table_unit', 'separator']
    int_list = ['image_width', 'image_height']
    float_list = ['lengthscale', 'timescale', 'z_step']

    if osp.exists(filename):
        # get parameters
        with open(filename) as f:
            for line in f:
                for param in string_list + int_list + float_list:
                    if param in line:
                        tokens = line.split(':')
                        if len(tokens) == 2:
                            if len(tokens[1].strip('\n')) > 0:
                                info[param] = tokens[1].strip('\n')
        # convert parameters
        for k in info.keys():
            if k in int_list:
                info[k] = int(info[k])
            elif k in float_list:
                info[k] = float(info[k])

    else:
        raise Exception("ERROR: info.txt doesn't exist or is not at the main data folder")

    mandatory_info = ['timescale', 'lengthscale']
    for mand_info in mandatory_info:
        if mand_info not in info.keys():
            print("ERROR: {} is not in info.txt".format(mand_info))
    return info


def get_data(data_dir, df=None, refresh=False, split_traj=False, set_origin_=False, image=None, reset_dim=['x', 'y'],invert_axes=[]):
    """
    get_data is the main function to import and package data. it can import an existing database or generate it.
    if it generates the database it loads important info with get_info.
    the tracking data are either loaded from a 'positions.txt' or 'positions.csv' file or passed as pd.DataFrame df
    data are scaled and velocities and accelerations are computed
    the coordinates origin and orientation can be reset with set_origin_ and invert_axes
    """
    # load existing database 
    pickle_fn = osp.join(data_dir, "data_base.p")

    if osp.exists(pickle_fn) is False or refresh:   #compute database
        
        # get info
        info = get_info(data_dir)
        lengthscale = info["lengthscale"]
        timescale = info["timescale"]
        table_unit = 'px' if 'table_unit' not in info.keys() else info['table_unit']  # by default positions are in px
        z_step = None if 'z_step' not in info.keys() else info['z_step']
        if z_step == 0:
            z_step = None

        # if no dataframe is passed try to get it from a csv of txt file
        if df is None:
            data_file = osp.join(data_dir, 'positions.csv') 
            sep = info["separator"] if "separator" in info.keys() else ','  # by default comma separated
            sep = '\t' if sep == 'tab' else sep
            df = pd.read_csv(data_file, sep=sep)   #columns must be ['x','y','z','frame','track']

        # check data type
        dimensions = ['x', 'y', 'z'] if 'z' in df.columns else ['x', 'y']
        dim = len(dimensions)
        df['frame'] = df['frame'].astype(np.int)
        for d in dimensions:
            df[d] = df[d].astype(np.float)

        # transform data
        df = tca.regularize_traj(df, dimensions, split_traj)
        tca.scale_dim(df, dimensions=dimensions, timescale=timescale, lengthscale=lengthscale, z_step=z_step,
                      unit=table_unit, invert_axes=invert_axes)
        tca.compute_vel_acc(df, dimensions=dimensions, timescale=timescale)

        # reset coordinates origin
        if set_origin_ is not False:
            if type(set_origin_) is dict:
                orig_coord_ = set_origin_
            else:
                orig_coord_ = None
            df, orig_coord = set_origin(df, image, reset_dim, lengthscale, orig_coord_)

        if 'z' in dimensions:  # relative z: centered around mean
            df['z_rel'] = df['z_scaled'] - df['z_scaled'].mean()

        # update pickle
        data = {'df': df, 'lengthscale': lengthscale, 'timescale': timescale, 'dim': dim, 'dimensions': dimensions}
        pickle.dump(data, open(pickle_fn, "wb"))
    else:
        data = pickle.load(open(pickle_fn, "rb"))

    return data


def get_traj(track_groups, track, min_frame=None, max_frame=None):
    '''gets the trajectory of an object. track_groups is the output of a groupby(). A subpart of the traj can be gotten by using min_frame and max_frame'''
    group = track_groups.get_group(track)
    if min_frame is not None:
        group = group[group['frame'] >= min_frame]
    if max_frame is not None:
        group = group[group['frame'] <= max_frame]
    return group.reset_index(drop=True)


def init_filters():
    """ Initialize filters """
    filters = {'xlim' : None,
                'ylim' : None,
                'zlim' : None,
                'min_traj_len' : None,
                'max_traj_len' : None,
                'frame_subset' : None,
                'ROI' : None,
                'name' : '' #custom name to identify the subset
                }
    return filters


def filter_by_traj_len(df, min_traj_len=1, max_traj_len=None):
    """Filter data by the minimum of maximum length (in frames) of trajectories"""
    df_ = pd.DataFrame()
    if max_traj_len is None:  # assign the longest possible track
        max_traj_len = df['frame'].max() - df['frame'].min() + 1
    min_traj_len = 1 if  min_traj_len is None else min_traj_len # assign 1, if not given

    tracks = df.groupby('track')
    for t in df['track'].unique():
        track = tracks.get_group(t)
        if track.shape[0] >= min_traj_len and track.shape[0] <= max_traj_len:
            df_ = pd.concat([df_, track])
    return df_


def filter_by_frame_subset(df, frame_subset=None):
    """Filter data by extracting a subset of frames"""
    if frame_subset is None:
        return df
    elif frame_subset[0] is None and frame_subset[1] is None:
        return df
    elif frame_subset[0] is None or frame_subset[1] is None:
        if frame_subset[0] is not None:
            df_ = df[df['frame'] >= frame_subset[0]]
        elif frame_subset[1] is not None:
            df_ = df[df['frame'] <= frame_subset[1]]
    else:
        df_ = df[((df['frame'] >= frame_subset[0]) & (df['frame'] <= frame_subset[1]))]

    if df_.shape[0] == 0:
        print("WARNING: no data for this frame subset. Returning unfiltered database")
        return df
    return df_


def region_filter(df, xlim=None, ylim=None, zlim=None):
    """Extract data within a box given by xlim, ylim and zlim in px"""
    df_ = df.copy()

    dims = list('xyz')
    for i, lim_ in enumerate([xlim, ylim, zlim]):
        if lim_ is not None:
            if lim_[0] is None and lim_[1] is None:
                pass
            elif lim_[0] is None or lim_[1] is None:
                if lim_[0] is not None:
                    df_ = df_[df_[dims[i]] >= lim_[0]]
                elif lim_[1] is not None:
                    df_ = df_[df_[dims[i]] <= lim_[1]]
            else:
                df_ = df_[((df_[dims[i]] >= lim_[0]) & (df_[dims[i]] <= lim_[1]))]

    if df_.shape[0] == 0:
        print("WARNING: no data for this frame subset. Returning unfiltered database")
        return df
    return df_


def get_coordinates(image):
    """Interactive selection of coordinates on an image by hand-drawing. Selection supported: points and rectangle. It can be a 2D, 3D, or 4D image.
    image is a dict containing the image path in 'image_fn', and 't_dim' and 'z_dim' which are the respective column index of time and z of the nd-image. If None, this dimension doesn't exist"""

    image_fn = image['image_fn']
    t_dim = image['t_dim']
    z_dim = image['z_dim']

    im = io.imread(image_fn)

    selecting = True
    while selecting:
        # create a list to be modified in get_coord so it is not deleted when get_coord ends
        shape_list = []
        points_list = []
        with napari.gui_qt():
            viewer = napari.view_image(im)
            print("Draw points or rectangles, then press ENTER and close the image viewer")

            @viewer.bind_key('Enter')
            def get_coord(viewer):
                for layer in viewer.layers:
                    if type(layer) is napari.layers.shapes.shapes.Shapes:
                        shape_list.append(layer)
                    if type(layer) is napari.layers.points.points.Points:
                        points_list.append(layer.data)

        # inspect selected layers
        rectangle_list = []
        if len(shape_list) > 0:
            for i, shape_type_ in enumerate(shape_list[0].shape_type):
                if shape_type_ == 'rectangle':
                    rectangle_list.append(shape_list[0].data[i])
        points = np.array([])
        if len(points_list) > 0:
            points = points_list[0]

        print('You have selected {} point(s) and {} rectangle(s)'.format(points.shape[0], len(rectangle_list)))
        finished = input('Is the selection correct? [y]/n: ')
        if finished != 'n':
            selecting = False
            del viewer

    coord_dict = {'points': [], 'rectangle': []}
    # get rectangle
    for rect in rectangle_list:
        # if 4D stack
        if t_dim is not None and z_dim is not None:
            frame = int(rect[0, t_dim])
            z = int(rect[0, z_dim])
            xmin, xmax = [rect[:, 3].min(), rect[:, 3].max()]
            ymin, ymax = [rect[:, 2].min(), rect[:, 2].max()]
        # if 3D (3rd dim being time or z)
        elif t_dim is not None or z_dim is not None:
            frame = int(rect[0, t_dim]) if t_dim is not None else None
            z = int(rect[0, z_dim]) if z_dim is not None else None
            xmin, xmax = [rect[:, 2].min(), rect[:, 2].max()]
            ymin, ymax = [rect[:, 1].min(), rect[:, 1].max()]
        # if 2D
        else:
            frame = None
            z = None
            xmin, xmax = [rect[:, 1].min(), rect[:, 1].max()]
            ymin, ymax = [rect[:, 0].min(), rect[:, 0].max()]

        coord_dict['rectangle'].append({'frame': frame, 'z': z, 'coord': [xmin, xmax, ymin, ymax]})

    for i in range(points.shape[0]):
        # if 4D stack
        if t_dim is not None and z_dim is not None:
            frame = int(points[i, t_dim])
            z = int(points[i, z_dim])
            x, y = [points[i, 3], points[i, 2]]
        # if 3D (3rd dim being time or z)
        elif t_dim is not None or z_dim is not None:
            frame = int(points[i, t_dim]) if t_dim is not None else None
            z = int(points[i, z_dim]) if z_dim is not None else None
            x, y = [points[i, 2], points[i, 1]]
        # if 2D
        else:
            frame = None
            z = None
            x, y = [points[i, 1], points[i, 0]]

        coord_dict['points'].append({'frame': frame, 'x': x, 'y': y, 'z': z})

    return coord_dict


def filter_by_ROI(df, image, filter_all_frames=False, return_ROIs=False):
    """Function used to choose subsets of trajectories which are within ROIs eiher: at a given frame (if filter_all_frames is False), or at all frame (if filter_all_frames is True).
    The selection is made by means of a rectangle tool on the image. It can be a 2D, 3D, or 4D image.
    t_dim and z_dim give the dimension index of time and z of the nd-image. If None, this dimension doesn't exist """

    if image is None:
        raise Exception("ERROR: no image provided. Aborting...")

    tracks = df.groupby('track')
    df_out = pd.DataFrame()

    selection = get_coordinates(image)
    ROI_list = selection['rectangle']

    for i, ROI in enumerate(ROI_list):
        xmin, xmax, ymin, ymax = ROI['coord']
        frame = ROI['frame']

        subdf = pd.DataFrame()
        if filter_all_frames:
            for fr in df['frame'].unique():
                # the subset at the given frame
                ind = ((df['frame'] == fr) & (df['x'] >= xmin) & (df['x'] <= xmax) & (df['y'] >= ymin) & (
                            df['y'] <= ymax))
                subdf = pd.concat([subdf, df[ind]])
        else:
            # the subset at the given frame
            ind = ((df['frame'] == frame) & (df['x'] >= xmin) & (df['x'] <= xmax) & (df['y'] >= ymin) & (
                        df['y'] <= ymax))
            subdf_frame = df[ind]

            # get the subset in the whole dataset
            for t in subdf_frame['track'].unique():
                track = tracks.get_group(t)
                subdf = pd.concat([subdf, track])

        # remove empty ROI
        if subdf.shape[0] == 0:
            print("Warning: ROI #{} doesn't contain any trajectory. ROI skipped...".format(i))
        else:
            subdf['group'] = i
            df_out = pd.concat([df_out, subdf])

    if return_ROIs:
        return df_out, ROI_list
    else:
        return df_out


def set_origin(df, image=None, reset_dim=['x', 'y'], lengthscale=1., orig_coord=None):
    """Set the origin of coordinates by selecting a point through a viewer. 
    Only some dimensions can be reset by reset_dim, the other are left unchanged.
    If no image is provided, the origin coordinates can be manually passed by orig_coord"""

    if orig_coord is None:
        # draw origin on image
        if image is not None:
            selection = get_coordinates(image)
            if len(selection['points']) != 1:
                raise Exception("ERROR: you need to select exactly one point to set the origin. Aborting...")

            origin = dict.fromkeys(reset_dim)

            for d in reset_dim:
                coord = selection['points'][0][d]
                if coord is not None:
                    coord *= lengthscale  # scale coordinate
                origin[d] = coord
        else:
            raise Exception("ERROR: no image nor origin coordinates provided. Aborting...")
    else:
        reset_dim = list(orig_coord.keys())
        origin = {d: orig_coord[d] * lengthscale for d in reset_dim}

    for d in reset_dim:
        if origin[d] is not None:
            df[d + '_scaled'] = df[d + '_scaled'] - origin[d]

    return df, origin


def select_sub_data(df, image=None, filters=[]):
    """Select with sets of filters given a list (or as a single if only one set). Each set of filter given as a dict {'frame_subset','min_traj_len','filter_by_ROI'}
    Each set generates a subet of df. A list of subsets is returned. 
    """

    df_list = []
    ROI_list = []

    if len(filters) == 0:
        return [df]

    if type(filters) is dict:  # if only one set of filters
        filters = [filters]

    for filt in filters:
        df_ = region_filter(df, xlim=filt['xlim'], ylim=filt['ylim'], zlim=filt['zlim'])
        df_ = filter_by_frame_subset(df_, frame_subset=filt['frame_subset'])
        df_ = filter_by_traj_len(df_, min_traj_len=filt['min_traj_len'], max_traj_len=filt['max_traj_len'])
        if filt['ROI'] is not None:
            df_, ROIs = filter_by_ROI(df_, image, filter_all_frames=filt['ROI']['filter_all_frames'], return_ROIs=True)
            ROI_list.append(ROIs)
        else:
            ROI_list.append(None)
        df_list.append(df_)

    return df_list, ROI_list


def get_background(image=None, frame=None, df=None, no_bkg=False, image_size=None, orig=None, axis_on=False,
                   dpi=plot_param['dpi'],figsize=(5,5)):
    """Get image background or create white backgound if no_bkg. The image can be a time nd stack or a single image."""
    if orig is None:
        # orig = 'lower' if image_dir is None else 'upper' #trick to plot for the first time only inverting Yaxis: not very elegant...
        orig = 'lower'

    if image is None:
        no_bkg = True
    else:
        if image['image_fn'] is None:
            no_bkg = True

    if no_bkg:
        if image_size is not None:
            xmin, xmax, ymin, ymax = [0, image_size[0], 0, image_size[1]]
            figsize = ((xmax - xmin) / dpi, (ymax - ymin) / dpi)
        else:
            if df is None:
                print("WARNING: no image nor data provided")
                figsize = figsize
            else:
                xmin = df['x'].min() - 0.05 * (df['x'].max() - df['x'].min())
                xmax = df['x'].max() + 0.05 * (df['x'].max() - df['x'].min())
                ymin = df['y'].min() - 0.05 * (df['y'].max() - df['y'].min())
                ymax = df['y'].max() + 0.05 * (df['y'].max() - df['y'].min())
                figsize = ((xmax - xmin) / dpi, (ymax - ymin) / dpi)

        fig = plt.figure(frameon=False, figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_aspect('equal')

    else:
        # extract frame if image is nd stack
        z_dim = image['z_dim']
        t_dim = image['t_dim']
        image_fn = image['image_fn']
        if z_dim is not None:  # if z stack, make a max_proj
            fn, file_ext = osp.splitext(image_fn)
            image_fn_ = fn + '_maxproj.tif'
            if not osp.exists(image_fn_):
                tpl.stack_max_proj(image_fn, z_dim, t_dim)
            image_fn = image_fn_
        im = io.imread(image_fn)
        if t_dim is not None:
            im = im[frame]

        im = img_as_ubyte(im)  # 8bit conversion
        n = im.shape[0]
        m = im.shape[1]
        fig = plt.figure(frameon=False, figsize=(m / dpi, n / dpi))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(im, aspect='equal', origin=orig, cmap='gray', vmin=0, vmax=255)
        xmin, xmax, ymin, ymax = ax.axis()
    
    if axis_on:
        ax.axis('on')
    else:
        ax.axis('off')
    
    return fig, ax, xmin, ymin, xmax, ymax, no_bkg


def load_config(data_dir,verbose=False):
    """ Import all existing config from the config directory. Each csv file is loaded in a dict """

    config_dir = osp.join(data_dir,'config')

    out_dict = {}

    if osp.exists(config_dir):
        if osp.isdir(config_dir):
            for f in listdir_nohidden(config_dir):
                if f.endswith('.csv'):
                    out_dict[f[:-4]] = load_dict(osp.join(config_dir,f))
        else:
            if verbose:
                print("WARNING: config is not a directory. Config not loaded.")
    else: 
        if verbose:
            print("WARNING: no config directory. Config not loaded.")

    return out_dict

def get_image(data_dir,filename=None,verbose=False):
    """ Get image named 'stack.tif' if exists """
    
    filename = osp.join(data_dir,'stack.tif') if filename is None else filename

    if osp.exists(filename):
        im = io.imread(filename)
        
        #convert RGB image to grayscale
        if im.shape[-1]==3:
            print("WARNING! RGB image, converting to grayscale")
            # change name RGB file
            dir_,fn = osp.split(filename)
            new_fn = osp.splitext(fn)[0]+'_RGB.tif'
            tifff.imsave(osp.join(dir_,new_fn), im)

            #convert to grayscale
            im = rgb2gray(im)
            im = img_as_ubyte(im) #8bit conversion
            tifff.imsave(filename, im)
        
        #
        image_dim = len(im.shape)
        if image_dim == 2:
            y_size,x_size = im.shape
            z_dim,t_dim = [None,None] #axes of z and t data 
            if verbose:
                print("You have loaded a {}D image: ({}x{}) pixels".format(image_dim,x_size,y_size))
        elif image_dim == 3:
            t_size,y_size,x_size = im.shape
            z_dim,t_dim = [None,0] #axes of z and t data 
            if verbose:
                print("You have loaded a {}D image: ({}x{}) pixels with {} time steps".format(image_dim,x_size,y_size,t_size))
        elif image_dim == 4:
            t_size,z_size,y_size,x_size = im.shape
            z_dim,t_dim = [1,0] #axes of z and t data 
            if verbose:
                print("You have loaded a {}D image: ({}x{}) pixels with {} time steps and {} z slices".format(image_dim,x_size,y_size,t_size,z_size))
                print("If the time and z dimensions are mixed up, you can swap them.")

        image_dict = {'image_fn': filename, 't_dim': t_dim, 'z_dim': z_dim, 'image_size': im.shape[-2:]}
    else:
        image_dict = {'image_fn': None, 't_dim': None, 'z_dim': None, 'image_size': None}
    
    return image_dict

