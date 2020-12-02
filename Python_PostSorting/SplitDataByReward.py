import numpy as np
import pandas as pd
import Python_PostSorting.Create2DHistogram
import os
import matplotlib.pylab as plt
from scipy import signal
import Python_PostSorting.ConvolveRates_FFT



def remove_low_speeds(rates, speed, position,trials, types ):
    data = np.vstack((rates, speed, position, trials, types))
    data=data.transpose()
    data_filtered = data[data[:,1] >= 3,:]
    return data_filtered


def split_time_data_by_reward(spike_data, prm):
    spike_data["spikes_in_time_rewarded"] = ""
    spike_data["spikes_in_time_failed"] = ""
    spike_data["spikes_in_time_rewarded_b"] = ""
    spike_data["spikes_in_time_failed_b"] = ""
    spike_data["spikes_in_time_rewarded_p"] = ""
    spike_data["spikes_in_time_failed_p"] = ""
    spike_data["spikes_in_time_rewarded_nb"] = ""
    spike_data["spikes_in_time_failed_nb"] = ""
    spike_data["averaged_rewarded_b"] = ""
    spike_data["averaged_failed_b"] = ""
    spike_data["averaged_rewarded_nb"] = ""
    spike_data["averaged_failed_nb"] = ""
    spike_data["averaged_rewarded_p"] = ""
    spike_data["averaged_failed_p"] = ""

    for cluster in range(len(spike_data)):
        rewarded_trials = np.array(spike_data.loc[cluster, 'rewarded_trials'])
        rewarded_trials = rewarded_trials[~np.isnan(rewarded_trials)]
        rates=np.array(spike_data.iloc[cluster].spike_rate_in_time[0].real)*10
        speed=np.array(spike_data.iloc[cluster].spike_rate_in_time[1].real)
        position=np.array(spike_data.iloc[cluster].spike_rate_in_time[2].real)
        types=np.array(spike_data.iloc[cluster].spike_rate_in_time[4].real, dtype= np.int32)
        trials=np.array(spike_data.iloc[cluster].spike_rate_in_time[3].real, dtype= np.int32)
        data = remove_low_speeds(rates, speed, position, trials, types )

        ## for all trials
        rates = data[:,0]
        speed = data[:,1]
        position = data[:,2]
        trials = data[:,3]
        types = data[:,4]

        rewarded_rates = rates[np.isin(trials,rewarded_trials)]
        rewarded_speed = speed[np.isin(trials,rewarded_trials)]
        rewarded_position = position[np.isin(trials,rewarded_trials)]
        reward_trials = trials[np.isin(trials,rewarded_trials)]
        reward_types = types[np.isin(trials,rewarded_trials)]
        failed_rates = rates[np.isin(trials,rewarded_trials, invert=True)]
        failed_speed = speed[np.isin(trials,rewarded_trials, invert=True)]
        failed_position = position[np.isin(trials,rewarded_trials, invert=True)]
        failed_trials = trials[np.isin(trials,rewarded_trials, invert=True)]
        failed_types = types[np.isin(trials,rewarded_trials, invert=True)]

        spike_data = drop_all_data_into_frame(spike_data, cluster, rewarded_rates, rewarded_speed , rewarded_position, reward_trials, reward_types, failed_rates, failed_speed, failed_position, failed_trials , failed_types)

        ## for beaconed trials
        data_filtered = data[data[:,4] == 0,:] # filter data for beaconed trials
        rates = data_filtered[:,0]
        speed = data_filtered[:,1]
        position = data_filtered[:,2]
        trials = data_filtered[:,3]
        types = data_filtered[:,4]

        rewarded_rates = rates[np.isin(trials,rewarded_trials)]
        rewarded_speed = speed[np.isin(trials,rewarded_trials)]
        rewarded_position = position[np.isin(trials,rewarded_trials)]
        reward_trials = trials[np.isin(trials,rewarded_trials)]
        reward_types = types[np.isin(trials,rewarded_trials)]
        failed_rates = rates[np.isin(trials,rewarded_trials, invert=True)]
        failed_speed = speed[np.isin(trials,rewarded_trials, invert=True)]
        failed_position = position[np.isin(trials,rewarded_trials, invert=True)]
        failed_trials = trials[np.isin(trials,rewarded_trials, invert=True)]
        failed_types = types[np.isin(trials,rewarded_trials, invert=True)]

        spike_data = drop_data_into_frame(spike_data, cluster, rewarded_rates, rewarded_speed , rewarded_position, reward_trials, reward_types, failed_rates, failed_speed, failed_position, failed_trials , failed_types)

        ## for probe trials
        data_filtered = data[data[:,4] == 2,:] # filter data for probe trials & nonbeaconed
        rates = data_filtered[:,0]
        speed = data_filtered[:,1]
        position = data_filtered[:,2]
        trials = data_filtered[:,3]
        types = data_filtered[:,4]

        rewarded_rates = rates[np.isin(trials,rewarded_trials)]
        rewarded_speed = speed[np.isin(trials,rewarded_trials)]
        rewarded_position = position[np.isin(trials,rewarded_trials)]
        reward_trials = trials[np.isin(trials,rewarded_trials)]
        reward_types = types[np.isin(trials,rewarded_trials)]
        failed_rates = rates[np.isin(trials,rewarded_trials, invert=True)]
        failed_speed = speed[np.isin(trials,rewarded_trials, invert=True)]
        failed_position = position[np.isin(trials,rewarded_trials, invert=True)]
        failed_trials = trials[np.isin(trials,rewarded_trials, invert=True)]
        failed_types = types[np.isin(trials,rewarded_trials, invert=True)]

        spike_data = drop_probe_data_into_frame(spike_data, cluster, rewarded_rates, rewarded_speed , rewarded_position, reward_trials, reward_types, failed_rates, failed_speed, failed_position, failed_trials , failed_types)

        ## for probe & nonbeaconed trials
        data_filtered = data[data[:,4] != 0,:] # filter data for nonbeaconed trials
        rates = data_filtered[:,0]
        speed = data_filtered[:,1]
        position = data_filtered[:,2]
        trials = data_filtered[:,3]
        types = data_filtered[:,4]

        rewarded_rates = rates[np.isin(trials,rewarded_trials)]
        rewarded_speed = speed[np.isin(trials,rewarded_trials)]
        rewarded_position = position[np.isin(trials,rewarded_trials)]
        reward_trials = trials[np.isin(trials,rewarded_trials)]
        reward_types = types[np.isin(trials,rewarded_trials)]
        failed_rates = rates[np.isin(trials,rewarded_trials, invert=True)]
        failed_speed = speed[np.isin(trials,rewarded_trials, invert=True)]
        failed_position = position[np.isin(trials,rewarded_trials, invert=True)]
        failed_trials = trials[np.isin(trials,rewarded_trials, invert=True)]
        failed_types = types[np.isin(trials,rewarded_trials, invert=True)]

        spike_data = drop_nb_data_into_frame(spike_data, cluster, rewarded_rates, rewarded_speed , rewarded_position, reward_trials, reward_types, failed_rates, failed_speed, failed_position, failed_trials , failed_types)
        spike_data = extract_time_binned_firing_rate_rewarded(spike_data, cluster, prm)


        rewarded_locations = np.array(spike_data.loc[cluster, 'rewarded_locations'])
        rewarded_locations = rewarded_locations[~np.isnan(rewarded_locations)]
        locations = np.array(np.append(rewarded_locations, rewarded_locations[0:14]))
        spike_data.at[cluster,"rewarded_locations"] = pd.Series(locations)
        rewarded_locations = np.array(spike_data.loc[cluster, 'rewarded_locations'])
        #spike_data = extract_time_binned_firing_rate_failed(spike_data, cluster, prm)
    return spike_data



def drop_data_into_frame(spike_data, cluster_index, a,b, c, d, e, f,  g, h, i, j):
    sn=[]
    sn.append(a) # rate
    sn.append(b) # speed
    sn.append(c) # position
    sn.append(d) # trials
    sn.append(e) # trials
    spike_data.at[cluster_index, 'spikes_in_time_rewarded_b'] = list(sn)

    sn=[]
    sn.append(f) # rate
    sn.append(g) # speed
    sn.append(h) # position
    sn.append(i) # trials
    sn.append(j) # trials
    spike_data.at[cluster_index, 'spikes_in_time_failed_b'] = list(sn)
    return spike_data


def drop_all_data_into_frame(spike_data, cluster_index, a,b, c, d, e, f,  g, h, i, j):
    sn=[]
    sn.append(a) # rate
    sn.append(b) # speed
    sn.append(c) # position
    sn.append(d) # trials
    sn.append(e) # trials
    spike_data.at[cluster_index, 'spikes_in_time_rewarded'] = list(sn)

    sn=[]
    sn.append(f) # rate
    sn.append(g) # speed
    sn.append(h) # position
    sn.append(i) # trials
    sn.append(j) # trials
    spike_data.at[cluster_index, 'spikes_in_time_failed'] = list(sn)
    return spike_data


def drop_probe_data_into_frame(spike_data, cluster_index, a,b, c, d, e, f,  g, h, i, j):
    sn=[]
    sn.append(a) # rate
    sn.append(b) # speed
    sn.append(c) # position
    sn.append(d) # trials
    sn.append(e) # trials
    spike_data.at[cluster_index, 'spikes_in_time_rewarded_p'] = list(sn)

    sn=[]
    sn.append(f) # rate
    sn.append(g) # speed
    sn.append(h) # position
    sn.append(i) # trials
    sn.append(j) # trials
    spike_data.at[cluster_index, 'spikes_in_time_failed_p'] = list(sn)
    return spike_data


def drop_nb_data_into_frame(spike_data, cluster_index, a,b, c, d, e, f,  g, h, i, j):
    sn=[]
    sn.append(a) # rate
    sn.append(b) # speed
    sn.append(c) # position
    sn.append(d) # trials
    sn.append(e) # trials
    spike_data.at[cluster_index, 'spikes_in_time_rewarded_nb'] = list(sn)

    sn=[]
    sn.append(f) # rate
    sn.append(g) # speed
    sn.append(h) # position
    sn.append(i) # trials
    sn.append(j) # trials
    spike_data.at[cluster_index, 'spikes_in_time_failed_nb'] = list(sn)
    return spike_data


def beaconed_plot(spike_data,cluster,  position_array, binned_speed, binned_speed_sd, save_path):
    cluster_index = spike_data.cluster_id.values[cluster] - 1
    speed_histogram = plt.figure(figsize=(4,3))
    ax = speed_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.plot(position_array,binned_speed, '-', color='Black')
    ax.fill_between(position_array, binned_speed-binned_speed_sd,binned_speed+binned_speed_sd, facecolor = 'Black', alpha = 0.2)

    plt.ylabel('Rates (Hz)', fontsize=12, labelpad = 10)
    plt.xlabel('Location (cm)', fontsize=12, labelpad = 10)
    plt.xlim(0,200)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    Python_PostSorting.plot_utility.style_track_plot(ax, 200)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=True,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        right=False,
        left=True,
        labelleft=True,
        labelbottom=True,
        labelsize=14,
        length=5,
        width=1.5)  # labels along the bottom edge are off

    ax.axvline(0, linewidth = 2.5, color = 'black') # bold line on the y axis
    ax.axhline(0, linewidth = 2.5, color = 'black') # bold line on the x axis
    ax.set_ylim(0)
    plt.locator_params(axis = 'x', nbins  = 3)
    ax.set_xticklabels(['-30', '70', '170'])
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig(save_path + '/time_binned_Rates_histogram_' + spike_data.session_id[cluster] + '_' + str(cluster_index +1) + 'rewarded.png', dpi=200)
    plt.close()


def probe_plot(spike_data,cluster,  position_array, binned_speed, binned_speed_sd, save_path):
    cluster_index = spike_data.cluster_id.values[cluster] - 1
    speed_histogram = plt.figure(figsize=(4,3))
    ax = speed_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.plot(position_array,binned_speed, '-', color='Black')
    ax.fill_between(position_array, binned_speed-binned_speed_sd,binned_speed+binned_speed_sd, facecolor = 'Black', alpha = 0.2)

    plt.ylabel('Rates (Hz)', fontsize=12, labelpad = 10)
    plt.xlabel('Location (cm)', fontsize=12, labelpad = 10)
    plt.xlim(0,200)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    Python_PostSorting.plot_utility.style_track_plot(ax, 200)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=True,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        right=False,
        left=True,
        labelleft=True,
        labelbottom=True,
        labelsize=14,
        length=5,
        width=1.5)  # labels along the bottom edge are off

    ax.axvline(0, linewidth = 2.5, color = 'black') # bold line on the y axis
    ax.axhline(0, linewidth = 2.5, color = 'black') # bold line on the x axis
    ax.set_ylim(0)
    plt.locator_params(axis = 'x', nbins  = 3)
    ax.set_xticklabels(['-30', '70', '170'])
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig(save_path + '/time_binned_Rates_histogram_' + spike_data.session_id[cluster] + '_' + str(cluster_index +1) + 'rewarded_probe.png', dpi=200)
    plt.close()


def beaconed_failed_plot(spike_data,cluster,  position_array, binned_speed, binned_speed_sd, save_path):
    cluster_index = spike_data.cluster_id.values[cluster] - 1
    speed_histogram = plt.figure(figsize=(4,3))
    ax = speed_histogram.add_subplot(1, 1, 1)  # specify (nrows, ncols, axnum)
    ax.plot(position_array,binned_speed, '-', color='Black')
    ax.fill_between(position_array, binned_speed-binned_speed_sd,binned_speed+binned_speed_sd, facecolor = 'Black', alpha = 0.2)

    plt.ylabel('Rates (Hz)', fontsize=12, labelpad = 10)
    plt.xlabel('Location (cm)', fontsize=12, labelpad = 10)
    plt.xlim(0,200)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    Python_PostSorting.plot_utility.style_track_plot(ax, 200)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=True,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        right=False,
        left=True,
        labelleft=True,
        labelbottom=True,
        labelsize=14,
        length=5,
        width=1.5)  # labels along the bottom edge are off

    ax.axvline(0, linewidth = 2.5, color = 'black') # bold line on the y axis
    ax.axhline(0, linewidth = 2.5, color = 'black') # bold line on the x axis
    ax.set_ylim(0)
    plt.locator_params(axis = 'x', nbins  = 3)
    ax.set_xticklabels(['-30', '70', '170'])
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig(save_path + '/time_binned_Rates_histogram_' + spike_data.session_id[cluster] + '_' + str(cluster_index +1) + 'failed.png', dpi=200)
    plt.close()


def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    """
    return np.isnan(y), lambda z: z.nonzero()[0]


def extract_time_binned_firing_rate_rewarded(spike_data,cluster, prm):
    save_path = prm.get_local_recording_folder_path() + '/Figures/Average_Rates_rewarded'
    if os.path.exists(save_path) is False:
        os.makedirs(save_path)

    speed=np.array(spike_data.iloc[cluster].spikes_in_time_rewarded[1])
    rates=np.array(spike_data.iloc[cluster].spikes_in_time_rewarded[0])
    position=np.array(spike_data.iloc[cluster].spikes_in_time_rewarded[2])
    #trials=np.array(spike_data.iloc[cluster].spikes_in_time_rewarded[3], dtype= np.int32)
    types=np.array(spike_data.iloc[cluster].spikes_in_time_rewarded[4], dtype= np.int32)

    try:
        window = signal.gaussian(3, std=5)
        rates = signal.convolve(rates, window, mode='same')/ sum(window)/sum(window)
    except (TypeError, ValueError):
        print("")

    data = np.vstack((rates,speed,position,types))
    data=data.transpose()

    data_filtered = data[data[:,3] == 0,:]
    rates = data_filtered[:,0]
    position = data_filtered[:,2]

    position_array = np.arange(1,201,1)
    binned_speed = np.zeros((position_array.shape))
    binned_speed_sd = np.zeros((position_array.shape))
    for rowcount, row in enumerate(position_array):
        speed_in_position = np.take(rates, np.where(np.logical_and(position >= rowcount, position < rowcount+1)))
        average_speed = np.nanmean(speed_in_position)
        sd_speed = np.nanstd(speed_in_position)
        binned_speed[rowcount] = average_speed
        binned_speed_sd[rowcount] = sd_speed
    spike_data.at[cluster, 'averaged_rewarded_b'] = list(binned_speed)

    #beaconed_failed_plot(spike_data,cluster,  position_array, binned_speed, binned_speed_sd, save_path)
    beaconed_plot(spike_data,cluster,  position_array, binned_speed, binned_speed_sd, save_path)

    data_filtered = data[data[:,3] == 2,:]
    rates = data_filtered[:,0]
    position = data_filtered[:,2]

    position_array = np.arange(1,201,1)
    binned_speed = np.zeros((position_array.shape))
    binned_speed_sd = np.zeros((position_array.shape))
    for rowcount, row in enumerate(position_array):
        speed_in_position = np.take(rates, np.where(np.logical_and(position >= rowcount, position < rowcount+1)))
        average_speed = np.nanmean(speed_in_position)
        sd_speed = np.nanstd(speed_in_position)
        binned_speed[rowcount] = average_speed
        binned_speed_sd[rowcount] = sd_speed

    data_b = pd.Series(binned_speed,dtype=None, copy=False)
    data_b = data_b.interpolate(method='linear', order=2)
    spike_data.at[cluster, 'averaged_rewarded_p'] = list(np.asarray(data_b))

    data_filtered = data[data[:,3] != 0,:]
    rates = data_filtered[:,0]
    position = data_filtered[:,2]

    position_array = np.arange(1,201,1)
    binned_speed = np.zeros((position_array.shape))
    binned_speed_sd = np.zeros((position_array.shape))
    for rowcount, row in enumerate(position_array):
        speed_in_position = np.take(rates, np.where(np.logical_and(position >= rowcount, position < rowcount+1)))
        average_speed = np.nanmean(speed_in_position)
        sd_speed = np.nanstd(speed_in_position)
        binned_speed[rowcount] = average_speed
        binned_speed_sd[rowcount] = sd_speed
    spike_data.at[cluster, 'averaged_rewarded_nb'] = list(binned_speed)
    return spike_data


def extract_time_binned_firing_rate_failed(spike_data, cluster, prm):
    speed=np.array(spike_data.iloc[cluster].spikes_in_time_failed[1])
    rates=np.array(spike_data.iloc[cluster].spikes_in_time_failed[0])
    position=np.array(spike_data.iloc[cluster].spikes_in_time_failed[2])
    types=np.array(spike_data.iloc[cluster].spikes_in_time_failed[4], dtype= np.int32)

    rates = convolve_with_scipy(rates)

    data = np.vstack((rates,speed,position,types))
    data=data.transpose()

    data_filtered = data[data[:,3] == 0,:]
    rates = data_filtered[:,0]
    position = data_filtered[:,2]

    position_array = np.arange(1,201,1)
    binned_speed = np.zeros((position_array.shape))
    binned_speed_sd = np.zeros((position_array.shape))
    for rowcount, row in enumerate(position_array):
        speed_in_position = np.take(rates, np.where(np.logical_and(position >= rowcount, position < rowcount+1)))
        average_speed = np.nanmean(speed_in_position)
        sd_speed = np.nanstd(speed_in_position)
        binned_speed[rowcount] = average_speed
        binned_speed_sd[rowcount] = sd_speed
    binned_speed = convolve_with_scipy(binned_speed)
    #binned_speed_sd = convolve_with_scipy(binned_speed_sd)
    spike_data.at[cluster, 'averaged_failed_b'] = list(binned_speed)

    save_path = prm.get_local_recording_folder_path() + '/Figures/Average_Rates_rewarded'
    if os.path.exists(save_path) is False:
        os.makedirs(save_path)
    beaconed_failed_plot(spike_data,cluster,  position_array, binned_speed, binned_speed_sd, save_path)

    data_filtered = data[data[:,3] == 2,:]
    rates = data_filtered[:,0]
    position = data_filtered[:,2]

    position_array = np.arange(1,201,1)
    binned_speed = np.zeros((position_array.shape))
    binned_speed_sd = np.zeros((position_array.shape))
    for rowcount, row in enumerate(position_array):
        speed_in_position = np.take(rates, np.where(np.logical_and(position >= rowcount, position < rowcount+1)))
        average_speed = np.nanmean(speed_in_position)
        sd_speed = np.nanstd(speed_in_position)
        binned_speed[rowcount] = average_speed
        binned_speed_sd[rowcount] = sd_speed
    #binned_speed = convolve_with_scipy(binned_speed)
    #binned_speed_sd = convolve_with_scipy(binned_speed_sd)
    spike_data.at[cluster, 'averaged_failed_p'] = list(binned_speed)

    data_filtered = data[data[:,3] != 0,:]
    rates = data_filtered[:,0]
    position = data_filtered[:,2]

    position_array = np.arange(1,201,1)
    binned_speed = np.zeros((position_array.shape))
    binned_speed_sd = np.zeros((position_array.shape))
    for rowcount, row in enumerate(position_array):
        speed_in_position = np.take(rates, np.where(np.logical_and(position >= rowcount, position < rowcount+1)))
        average_speed = np.nanmean(speed_in_position)
        sd_speed = np.nanstd(speed_in_position)
        binned_speed[rowcount] = average_speed
        binned_speed_sd[rowcount] = sd_speed
    #binned_speed = convolve_with_scipy(binned_speed)
    #binned_speed_sd = convolve_with_scipy(binned_speed_sd)
    spike_data.at[cluster, 'averaged_failed_nb'] = list(binned_speed)
    return spike_data


def convolve_with_scipy(rate):
    window = signal.gaussian(2, std=3)
    convolved_rate = signal.convolve(rate, window, mode='same')/ sum(window)
    return convolved_rate

