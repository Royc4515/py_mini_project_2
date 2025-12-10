from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calc_mean_erp(trial_points: np.ndarray, ecog_data: np.ndarray, pre_ms: int = 200, post_ms: int = 1000) -> np.ndarray:
    """
    Compute the mean Event Related Potential (ERP) per finger.

    Parameters
    ----------
    trial_points : np.ndarray of shape (n_trials, 3)
        Columns: [start_index, peak_index, finger_id].
        All values must be integers.
    ecog_data : np.ndarray of shape (n_samples,) or (n_samples, 1)
        ECOG time series sampled at 1000 Hz.
    pre_ms : int
        Milliseconds (samples) before movement onset.
    post_ms : int
        Milliseconds (samples) after movement onset.

    Returns
    -------
    fingers_erp_mean : np.ndarray of shape (5, pre_ms + 1 + post_ms)
        Row i (0-based) is the mean ERP for finger i+1.
    """
    # Make sure correct dtypes and shapes
    tp= np.asarray(trial_points, dtype=int)
    sig= np.asarray(ecog_data).squeeze()

    assert tp.ndim == 2 and tp.shape[1] == 3, "trial points must be (n_samples, 3)"
    assert sig.ndim == 1, "ecog data must be 1D"

    n_fingers = 5
    win_len= pre_ms + 1 + post_ms #200 before+ 1 onset + 1000 after = 1201

    #preparing a structure to group trials by finger
    finger_epochs: dict[int, list[np.ndarray]] = {f:[] for f in range(1, n_fingers+1)}

    #loop over trial and extract windows
    for start_index, peak_index, finger_id in tp:
        start_index = int(start_index)
        finger_id = int(finger_id)

        beg= start_index - pre_ms #the first index of the window (200 samples before start)
        end= start_index + post_ms + 1 #one past the last index (Python slicing end is exclusive)
        #Slice sig[beg:end] has length end - beg = 1201

        #skip out-of-bounds trial
        if beg < 0 or end > sig.shape[0]:
            continue

        epoch= sig[beg:end]
        if epoch.shape[0] != win_len: #double check for 1201 length
            continue

        finger_epochs[finger_id].append(epoch)
    """After the loop:
    
    finger_epochs[1] is a list of many (epochs for finger 1).
    
    finger_epochs[2] is a list of many (finger 2), etc."""

    #Avg per finger
    erp_list: list[np.ndarray] = [] #List to store the mean waveform for each finger (5 arrays total)
    for f in range(1, n_fingers+1):
        epochs = np.vstack(finger_epochs[f]) # shape: (n_trials_for_finger, win_len)
        erp_list.append(epochs.mean(axis=0))

    fingers_erp_mean = np.vstack(erp_list) #shape: (5,win_len)
    return fingers_erp_mean

def plot_erps(fingers_erp_mean: np.ndarray, pre_ms: int = 200, post_ms: int = 1000) -> None:
    """plot the mean ERP for all 5 fingers"""
    time_axis = np.arange(-pre_ms, post_ms+1)

    plt.figure(figsize=(10,6))
    colors = ['red', 'blue','green','orange', 'purple']

    for i in range(5):
        plt.plot(time_axis, fingers_erp_mean[i, :], label=f"Finger{i + 1}", color=colors[i], linewidth=1.5)

    plt.axvline(0, color='black', linestyle='--', alpha=0.6)
    plt.xlabel("Time relative to movement onset (ms)")
    plt.ylabel("ECOG amplitude")
    plt.title("Mean ERP per Finger")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def calc_mean_erp_from_files(trial_points_path: str, ecog_data_path: str,
                              pre_ms: int = 200, post_ms: int = 1000) -> np.ndarray:
    """
       Convenience wrapper:
       - loads CSVs (events as int, ECOG as float)
       - calls calc_mean_erp(...)
    """
    # events_file_ordered.csv has no header; enforce int
    trial_df = pd.read_csv(trial_points_path, header= None) #read the events file
    trial_points = trial_df.to_numpy(dtype=int) #convert to np.ndarray and force int type

    ecog_df= pd.read_csv(ecog_data_path, header= None)
    ecog_data = ecog_df.iloc[:,0].to_numpy() #pick the column and convert to 1D array

    return calc_mean_erp(trial_points, ecog_data, pre_ms= pre_ms, post_ms= post_ms)