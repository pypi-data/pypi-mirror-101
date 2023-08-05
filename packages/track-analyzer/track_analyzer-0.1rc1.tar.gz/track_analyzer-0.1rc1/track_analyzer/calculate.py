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

import sys
import os.path as osp

import numpy as np
import pandas as pd
import scipy.interpolate as sci
import pickle
import matplotlib.tri as tri

from track_analyzer import prepare as tpr


def regularize_traj(df, dimensions=['x', 'y', 'z'], split_traj=False):
    """This function etiher splits traj with time gaps, or fill the gap by linear interpolation (default). 
    This function also renames the traj_id to make sure the format is well handled and ids don't get mixed up when renamed"""

    new_df = pd.DataFrame(columns=list(df.columns) + ['input_track_id'])

    groups = df.groupby(['track'])

    for i, traj_id in enumerate(df['track'].unique()):
        # get traj subdf, sort and check if there is a gap in the frame list
        traj = groups.get_group(traj_id)

        # rename traj
        traj.loc[:,'input_track_id'] = traj_id
        traj.loc[:,'track'] = i

        # sort frames and find gaps
        sorted_traj = traj.sort_values(by='frame')
        frame_list = sorted_traj['frame'].values
        frame_subsets = tpr.group_consecutives(frame_list, step=1)

        if len(frame_subsets) > 1:  # if there is a gap
            # split traj by giving new names
            if split_traj:
                for j, subset in enumerate(frame_subsets):
                    ind = sorted_traj['frame'].isin(subset)
                    sorted_traj.loc[ind, 'track'] = traj_id + '_{}'.format(j)

                new_df = pd.concat([new_df, sorted_traj])

            # or interpolate
            else:
                cont_frame_list = np.arange(frame_list.min(), frame_list.max() + 1)  # frame list with no gap
                new_subdf = pd.DataFrame(columns=df.columns)
                new_subdf['frame'] = cont_frame_list
                new_subdf['track'] = traj_id
                for d in dimensions:
                    interp = sci.interp1d(sorted_traj['frame'], sorted_traj[d])
                    new_subdf[d] = interp(cont_frame_list)

                new_df = pd.concat([new_df, new_subdf])
        else:
            new_df = pd.concat([new_df, sorted_traj])

    new_df.reset_index(inplace=True, drop=True)
    del df #remove memory

    return new_df


def scale_dim(df, dimensions=['x', 'y', 'z'], timescale=1., lengthscale=1., z_step=None, unit='px', invert_axes=[]):
    """This function scales the data depending on the unit of the input data"""

    # time
    df['frame'] -= df['frame'].min()  # ensure frame starts at 0
    df['frame'] = df['frame'].astype(np.int)
    df['t'] = df['frame'] * timescale

    # lengthscale in unit/px
    dimensions_ = dimensions if z_step is None else ['x', 'y']  # if same lengthscale in the z_direction

    for dim in dimensions_:
        if unit == 'px':  # if data are in px in the input file, scale them
            df[dim + '_scaled'] = df[dim] * lengthscale
        else:  # if data are already scaled, copy to scaled columns and back calculate the position in px in the input file, scale them
            df[dim + '_scaled'] = df[dim]
            df[dim] = df[dim + '_scaled'] / lengthscale

    if z_step is not None:  # scale z differently
        if unit == 'px':  # if data are in px in the input file, scale them
            df['z_scaled'] = df['z'] * z_step
        else:  # if data are already scaled, copy to scaled columns and back calculate the position in px in the input file, scale them
            df['z_scaled'] = df['z']
            df['z'] = df['z_scaled'] / z_step

    for ax in invert_axes:
        df[ax + '_scaled'] = -df[ax + '_scaled']


def compute_vel_acc(df, dimensions=['x', 'y', 'z'], timescale=1.):
    """This function computes velocities and acceleration from positions. It assumes that positions are evenly spaced with respect to time"""

    r, c = df.shape
    groups = df.groupby(['track'])

    # components
    for dim in dimensions:
        init = np.empty(r)
        init[:] = np.nan
        df['v' + dim] = init
        df['a' + dim] = init
        for traj_id in df['track'].unique():
            traj = groups.get_group(traj_id)
            if traj.shape[0]>1:  # calculate only if at least to timesteps
                ind = traj.index.values
                # velocity
                vel = np.gradient(traj[dim + '_scaled'].values, timescale)
                df.loc[ind, 'v' + dim] = vel
                # acceleration
                df.loc[ind, 'a' + dim] = np.gradient(vel, timescale)

    # modulus
    sum_v = 0
    sum_a = 0
    for dim in dimensions:
        sum_v += df['v' + dim].values ** 2
        sum_a += df['a' + dim].values ** 2
    df['v'] = np.sqrt(sum_v)
    df['a'] = np.sqrt(sum_a)


def recompute_pos(df, dimensions=['x', 'y', 'z'], lengthscale=1.):
    """This function recomputes positions from velocity data """

    for traj in df['track'].unique():
        traj_frames = sort(df[df['track'] == traj]['frame'].values)
        for i, frame in enumerate(traj_frames[1:]):
            ind_ = ((df['frame'] == traj_frames[i]) & (df['track'] == traj))  # i is the index of the previous frame
            ind = ((df['frame'] == frame) & (df['track'] == traj))
            for dim in dimensions:
                disp = df.loc[ind, 'v' + dim].values[0] * (df.loc[ind, 't'].values[0] - df.loc[ind_, 't'].values[
                    0])  # displacement=v*time_interval which is not necessarily dt
                if np.isfinite(disp):
                    df.loc[ind, dim + '_scaled'] = df.loc[ind_, dim + '_scaled'].values[0] + disp
    for dim in dimensions:
        df[dim] = df[dim + '_scaled'] * lengthscale


def compute_track_prop(df, dimensions=['x', 'y', 'z']):
    """Compute track properties by averaging all data along a traj"""

    groups = df.groupby('track')

    scaled_dimensions = [dim + '_scaled' for dim in dimensions]
    vel = ['v' + dim for dim in dimensions]
    acc = ['a' + dim for dim in dimensions]

    columns = ['track', 'track_length', 't'] + dimensions + scaled_dimensions + vel + acc + ['v', 'a']
    df_out = pd.DataFrame(columns=columns)

    for i, track in enumerate(df['track'].unique()):
        traj = groups.get_group(track)
        track_length = traj['t'].max() - traj['t'].min()
        val = [track, track_length]
        for col in columns[2:]:
            val.append(traj[col].mean())
        df_out.loc[i, columns] = val

    return df_out


def interpolate_field(data_dir, df, groups, grids, frame, field_values=['vx', 'vy', 'vz', 'ax', 'ay', 'az', 'v', 'a'],
                      temporal_average=0, export_field=False, outdir=None):
    """ Interpolate field values over a regular grid at a given frame. 
    A temporal average over several frames can be performed"""

    if outdir is None:
        outdir = osp.join(data_dir, 'field')
    tpr.safe_mkdir(outdir)

    node_grid, center_grid = grids
    X, Y = node_grid
    x, y = center_grid
    data = {'X': X, 'Y': Y, 'x': x, 'y': y}
    # contain data in a list over the frames for each value
    field_dict = {k: [] for k in field_values}

    coord_list = list(df.columns)
    for non_coord in ['track', 'frame', 't', 'input_track_id','Unnamed: 0']:
        coord_list.remove(non_coord)

    frame_l = range(int(frame - temporal_average), int(frame + temporal_average + 1))
    for frame_ in frame_l:
        # interpolate vfield for each frame
        if frame_ in df['frame'].unique():
            group_ = groups.get_group(frame_).reset_index(drop=True)
            print(coord_list)
            print(group_[coord_list])
            no_nan_ = group_[np.isfinite(group_[coord_list])]
            triang = tri.Triangulation(no_nan_['x'].values, no_nan_['y'].values)
            for coord in field_values:
                interpolator = tri.LinearTriInterpolator(triang, no_nan_[coord].values)
                field_dict[coord].append(interpolator(X, Y))
    for coord in field_values:
        # average interpolated vfield over the frame list
        stack = np.ma.stack(field_dict[coord], axis=2)
        field = np.ma.filled(np.sum(stack, axis=2) / len(frame_l), np.nan)
        data[coord] = field

    if export_field:
        export_dir = osp.join(outdir, 'field_export')
        tpr.safe_mkdir(export_dir)
        for k in data.keys():
            f_out = osp.join(export_dir, k + '_t_{:04d}.txt'.format(int(frame)))
            np.savetxt(f_out, data[k], delimiter=',')

    return data


def interpolate_all_fields(data_dir, df, grids, field_values=['vx', 'vy', 'vz', 'ax', 'ay', 'az', 'v', 'a'],
                           temporal_average=0, export_field=False, outdir=None):
    """
    Interpolate field values over a regular grid for all frames.
    A temporal average over several frames can be performed
    :param data_dir:
    :param df:
    :param grids:
    :param field_values:
    :param temporal_average:
    :param export_field:
    :param outdir:
    :return:
    """

    if outdir is None:
        outdir = osp.join(data_dir, 'field')
    tpr.safe_mkdir(outdir)

    groups = df.groupby('frame')

    data_dict = {}

    for frame in df['frame'].unique():
        data = interpolate_field(data_dir, df, groups, grids, frame, field_values=field_values,
                                 temporal_average=temporal_average, export_field=export_field, outdir=outdir)
        data_dict[frame] = data
    print('\n')

    pickle_fn = osp.join(outdir, 'field.p')
    pickle.dump(data_dict, open(pickle_fn, "wb"))

    return data_dict


def compute_div_curl(data_dir, data_dict, frame, lengthscale=1., export_field=False, outdir=None):
    """Compute 2D divergence and curl on a regular grid"""

    if outdir is None:
        outdir = osp.join(data_dir, 'field')
    tpr.safe_mkdir(outdir)

    # get vel field
    X = data_dict[frame]['X']
    Y = data_dict[frame]['Y']
    vx = data_dict[frame]['vx']
    vy = data_dict[frame]['vy']

    dX = (X.max() - X.min()) / (X.shape[1] - 1) * lengthscale  # scaled cell size

    # compute div
    div = np.empty(X.shape)
    div[:] = np.nan
    curl = np.empty(X.shape)
    curl[:] = np.nan
    for j in range(1, X.shape[0] - 1):
        for i in range(1, X.shape[1] - 1):
            # div
            Dx_vx = (vx[j, i + 1] - vx[j, i - 1]) / (2 * dX)
            Dy_vy = (vy[j + 1, i] - vy[j - 1, i]) / (2 * dX)
            div[j, i] = Dx_vx + Dy_vy
            # curl
            Dy_vx = (vx[j + 1, i] - vx[j - 1, i]) / (2 * dX)
            Dx_vy = (vy[j, i + 1] - vy[j, i - 1]) / (2 * dX)
            curl[j, i] = Dx_vy - Dy_vx

    if export_field:
        export_dir = osp.join(outdir, 'field_export')
        tpr.safe_mkdir(export_dir)
        data_name = ['div', 'curl']
        for i, data in enumerate([div, curl]):
            f_out = osp.join(export_dir, data_name[i] + '_t_{:04d}.txt'.format(int(frame)))
            np.savetxt(f_out, data, delimiter=',')

    return div, curl


def compute_all_div_curl(data_dir, df, data_dict, lengthscale=1., outdir=None, export_field=False):
    """Compute 2D divergence and curl on a regular grid for all frames. Requires interpolated field data passed by data_dict."""

    if outdir is None:
        outdir = osp.join(data_dir, 'field')
    tpr.safe_mkdir(outdir)

    groups = df.groupby('frame')

    for frame in df['frame'].unique():
        div, curl = compute_div_curl(data_dir, data_dict, frame, lengthscale=lengthscale, export_field=export_field,
                                     outdir=outdir)
        data_dict[frame]['div'] = div
        data_dict[frame]['curl'] = curl

    pickle_fn = osp.join(outdir, 'field.p')
    pickle.dump(data_dict, open(pickle_fn, "wb"))

    return data_dict


def compute_vector_mean(data_dir, data_dict, frame, field, dimensions=['x', 'y', 'z'], export_field=False, outdir=None):
    """Compute vector average defined as the modulus of the velocity or acceleration vector field. 
    The average can be in 2D or 3D."""

    if outdir is None:
        outdir = osp.join(data_dir, 'field')
    tpr.safe_mkdir(outdir)

    field_ = field[:field.find('_mean')]  # remove '_mean' from field name

    # ensure coordinate exists
    for d in dimensions:
        if field_ + d not in data_dict[frame].keys():
            dimensions.remove(d)

    # compute modulus
    modulus = 0
    for d in dimensions:
        f_ = field_ + d
        modulus += (data_dict[frame][field_ + d]) ** 2
    modulus = np.sqrt(modulus) / len(dimensions)

    if export_field:
        export_dir = osp.join(outdir, 'field_export')
        tpr.safe_mkdir(export_dir)
        f_out = osp.join(export_dir, field_ + '_mean_t_{:04d}.txt'.format(int(frame)))
        np.savetxt(f_out, modulus, delimiter=',')

    return modulus


def compute_all_vector_mean(data_dir, df, data_dict, field, dimensions=['x', 'y', 'z'], export_field=False,
                            outdir=None):
    """Compute vector average defined as the modulus of the velocity or acceleration vector field, for all frames. Requires interpolated field data passed by data_dict.
    The average can be in 2D or 3D."""

    if outdir is None:
        outdir = osp.join(data_dir, 'field')
    tpr.safe_mkdir(outdir)

    groups = df.groupby('frame')

    for frame in df['frame'].unique():
        data_dict[frame][field] = compute_vector_mean(data_dir, data_dict, frame, field, dimensions=dimensions,
                                                      export_field=export_field, outdir=outdir)

    pickle_fn = osp.join(outdir, 'field.p')
    pickle.dump(data_dict, open(pickle_fn, "wb"))

    return data_dict


def compute_vlim(df, data, field):
    """Compute the min and max values (vlim) over all frames for a specific field"""
    vlim = [None, None]
    for frame in df['frame'].unique():
        frame = int(frame)
        val = data[frame][field]
        val = val[~np.isnan(val)]
        if len(val) > 1:  # at least 2 numbers
            if vlim[0] is None:
                vlim[0] = val.min()
            else:
                vlim[0] = min(val.min(), vlim[0])
            if vlim[1] is None:
                vlim[1] = val.max()
            else:
                vlim[1] = max(val.max(), vlim[1])

    return vlim


def compute_msd(traj, timescale=None, dimensions=['x_scaled', 'y_scaled']):
    '''Compute the MSD of evenly spaced trajectory. By default, it uses scaled data.
    Inspired from _msd_fft function https://github.com/soft-matter/trackpy/blob/master/trackpy/motion.py
    The algorithm is described in this paper: http://dx.doi.org/10.1051/sfn/201112010.'''

    columns = [d + '_sq' for d in dimensions]
    N = traj.shape[0]
    max_lagtime = N - 1
    lags = np.arange(1, max_lagtime + 1)
    

    if timescale is None:
        timescale = np.mean(traj['t'].values / traj['frame'].values)

    # MSD
    r = traj[dimensions].values
    D = r ** 2
    D_sum = D[:max_lagtime] + D[:-max_lagtime - 1:-1]
    S1 = 2 * D.sum(axis=0) - np.cumsum(D_sum, axis=0)
    F = np.fft.fft(r, n=2 * N, axis=0)
    PSD = F * F.conjugate()
    S2 = np.fft.ifft(PSD, axis=0)[1:max_lagtime + 1].real
    squared_disp = S1 - 2 * S2
    squared_disp /= N - lags[:, np.newaxis]

    results = pd.DataFrame(squared_disp, columns=columns)
    results['msd'] = squared_disp.sum(axis=1)
    results['tau'] = lags * timescale
    results = results[np.isfinite(results['msd'])]  # remove nan

    return results


def get_obj_persistence_length(track_groups, track, traj=None, save_plot=False, dim=3):
    '''This function fits an object MSD with a PRW model to extract its persistence length'''
    if traj is None:
        traj = tpr.get_traj(track_groups, track)
    msd = compute_msd(traj)
    best, speed, success = tpr.fit_msd(msd, traj, save_plot=save_plot)
    if success:
        pers_time = best.best_values['P']
        pers_length = pers_time * speed
        return pers_length
    else:
        return np.nan


####### to be sorted ########

def get_transf_coord(data_dir, timescale, lengthscale, dim):
    """Gets the trajectory of the shifting reference. Should be a cvs table with coordinates in px and frame definition: first=0 (can start at any moment though) """

    filename = osp.join(data_dir, "coord_transformation.csv")
    if osp.exists(filename):
        df_transf = pd.read_csv(filename)
        col = list(df_transf.columns)
        col.pop(col.index('frame'))

        # interpolate frame if not int (data generated by a kymograph)
        df_transf2 = pd.DataFrame(columns=df_transf.columns)
        if not df_transf['frame'].dtype == int:
            frame_list = np.arange(df_transf['frame'].min(), df_transf['frame'].max())
            df_transf2['frame'] = frame_list
            for d in col:
                interp = sci.interp1d(df_transf['frame'], df_transf[d])
                df_transf2[d] = interp(frame_list)
            df_transf = df_transf2.copy()

        if 'angle' in col:
            col_ = col[:col.index('angle')] + col[col.index('angle') + 1:]
        else:
            col_ = col
        scale_dim(df_transf, col_, timescale, lengthscale, unit='px')

        return df_transf, col, col_

    else:
        print("Warning: no coord_transformation file")


def transf_coord(df, data_dir, timescale, lengthscale, dim, transf_type='center-rotate', calculate_transf=False):
    """ Apply a coordinate transformation (shift and/or rotation) along time. The new data can be centered (if transf_type=center) or can be shifted to the initial position (if transf_type=shift)
    The transformation can be computed using a tracked position from the coord_transformation.csv file, or computed using the 2nd centered moments calculations. The rotation is only supported in the XY plane."""

    dimensions = ['x', 'y', 'z'] if dim == 3 else ['x', 'y']

    if not calculate_transf:
        df_transf, col, col_ = get_transf_coord(data_dir, timescale, lengthscale, dim)
        min_frame = max(df_transf['frame'].min(), df['frame'].min())
        max_frame = min(df_transf['frame'].max(), df['frame'].max())
        df = df[((df['frame'] >= min_frame) & (df['frame'] <= max_frame))]  # ensure working on same frame subset

    groups = df.groupby(['frame'])

    df_ = pd.DataFrame(columns=df.columns)

    first_frame = True
    for frame in df['frame'].unique():
        group = groups.get_group(frame)
        if group.shape[0] == 0:  # dont process if empty frame
            continue

        if calculate_transf:
            x_mean = group['x'].mean()
            y_mean = group['y'].mean()
            z_mean = group['z'].mean()
            m20 = ((group['x'] - x_mean) ** 2).mean()
            m02 = ((group['y'] - y_mean) ** 2).mean()
            m11 = (group['x'] * group['y'] - x_mean * y_mean).mean()
            phi = 0.5 * np.arctan(2 * m11 / (m20 - m02))

        # shift
        shifts_init = dict.fromkeys(dimensions)  # shift at the first non-empty frame

        if transf_type in ['center-rotate', 'shift-rotate', 'center', 'shift']:
            for d in dimensions:
                if calculate_transf:
                    shift = group[d].mean()
                else:
                    if d not in col_:
                        continue
                    shift = df_transf.loc[df_transf['frame'] == frame, d].values[0]
                if first_frame:
                    shifts_init[d] = shift

                group[d] -= shift
                if transf_type in ['shift-rotate', 'shift']:  # shift to the initial position
                    group[d] += shifts_init[d]

            first_frame = False

        # rotation
        if transf_type in ['center-rotate', 'shift-rotate', 'rotate']:
            if calculate_transf:
                angle_ = -phi
            else:
                if 'angle' not in col:
                    print("WARNING: no angle data in coord_transformation.csv")
                    continue
                angle = df_transf.loc[df_transf['frame'] == frame, 'angle'].values[0]
                angle_ = angle * 2 * np.pi / 360. + np.pi
            group['x_'] = group['x'] * np.cos(angle_) - group['y'] * np.sin(angle_)
            group['y_'] = group['x'] * np.sin(angle_) + group['y'] * np.cos(angle_)
            group['x'] = group['x_']
            group['y'] = group['y_']
            del group['x_']
            del group['y_']

        for d in dimensions:
            group[d + '_scaled'] = group[d] / lengthscale
        df_ = pd.concat([df_, group])

    compute_vel_acc(df_, dimensions)

    return df_


def get_neighbors(df_frame, track, kernel_radius, dim=3):
    """ Find the neighbors of a track within a radius"""
    neighbors = []
    dimensions = ['x_scaled', 'y_scaled', 'z_scaled'] if dim == 3 else ['x_scaled', 'y_scaled']

    if df_frame[df_frame['track'] == track].shape[0] == 0:
        return []
    else:
        track_coord = df_frame[df_frame['track'] == track][dimensions].values[0]
        distance_df = df_frame[dimensions + ['track']]
        distance_df['sq_distance'] = 0
        for i, d in enumerate(dimensions):
            distance_df[d] -= track_coord[i]
            distance_df['sq_distance'] += distance_df[d] ** 2

        neighbors = list(distance_df[distance_df['sq_distance'] <= kernel_radius ** 2]['track'].values)
        return neighbors


def average_local_vel(df, kernel_radius, dim=3):
    frame_groups = df.groupby(['frame'])
    new_df = pd.DataFrame()
    coordinates = ['vx', 'vy', 'vz'] if dim == 3 else ['vx', 'vy']
    for i in df['frame'].unique():
        sys.stdout.write('\033[2K\033[1G')
        print('\rcomputing local average on frame ' + str(i), end='\r')

        df_frame = frame_groups.get_group(i)
        for coordinate in coordinates:
            df_frame[coordinate + '_loc'] = np.nan
        for track in df_frame['track']:
            neighbors = get_neighbors(df_frame, track, kernel_radius, dim=dim)
            sub_df = df_frame[df_frame['track'].isin(neighbors)]
            for coordinate in coordinates:
                df_frame.loc[df_frame['track'] == track, coordinate + '_loc'] = sub_df[coordinate].mean()
        sum_ = 0
        for coordinate in coordinates:
            sum_ += df_frame[coordinate + '_loc'] ** 2
        df_frame['v_loc'] = np.sqrt(sum_)
        new_df = pd.concat([new_df, df_frame])
    return new_df


def subtract_vfield_(df, params, dimensions=['x', 'y', 'z'], lengthscale=1., recompute_pos_=True):
    """Subtract velocities to a velocities field given by params:"""

    data = tpr.get_data(params["data_dir"])
    df_ = data['df']
    groups_ = df_.groupby('frame')
    coord_list = ['vx', 'vy', 'vz'] if dim_ == 3 else ['vx', 'vy']

    groups = df.groupby('frame')
    for frame in df['frame'].unique():
        group = groups.get_group(frame).reset_index(drop=True)
        vfield = interpolate_vfield(df_, groups_, params["grid"], params["temporal_average"], frame,
                                    coord_list)  # compute vfield to subtract
        r, c = params["grid"][0].shape
        X = params["grid"][0].reshape(r * c, )
        Y = params["grid"][1].reshape(r * c, )
        triang = tri.Triangulation(X, Y)
        interpol_dict = {k: [] for k in coord_list}
        for i, coord in enumerate(coord_list):
            z = vfield[i].reshape(r * c, )
            interpol_dict[coord] = tri.LinearTriInterpolator(triang,
                                                             z)  # interpolate vfield to subtract and compute velocities at the positions to make the subtraction
            ind = df['frame'] == frame
            x, y = [df.loc[ind, 'x'].values, df.loc[ind, 'y'].values]
            df.loc[ind, coord] = df.loc[ind, coord] - interpol_dict[coord](x, y)

    # recalculate positions and velocities
    sum_ = 0
    for dim in dimensions:
        sum_ += df['v' + dim] ** 2
    df['v'] = np.sqrt(sum_)

    if recompute_pos_:
        recompute_pos(df, dimensions, lengthscale)

    return df
