import os
import sys
from src.erp import calc_mean_erp_from_files, plot_erps


#define paths
EVENTS_PATH = os.path.join("mini_project_2_data", "events_file_ordered.csv")
ECOG_PATH = os.path.join("mini_project_2_data", "brain_data_channel_one.csv")

def main():
    print("=== MiniProject 2: ERP analysis ===")

    #check that the data files exist
    if not os.path.exists(EVENTS_PATH):
        print(f"ERROR: events file not found at {EVENTS_PATH}")
        sys.exit(1)
        
    if not os.path.exists(ECOG_PATH):
        print(f"ERROR: brain data file not found at {ECOG_PATH}")
        sys.exit(1)

    try:
        #compute the ERP matrix (calls helper function in erp.py
        fingers_erp_mean = calc_mean_erp_from_files(trial_points_path=EVENTS_PATH, ecog_data_path=ECOG_PATH)
    
        #verification
        print(f"ERP matrix shape: {fingers_erp_mean.shape}")
        if fingers_erp_mean.shape == (5,1201):
            print("SUCCESS: Matrix shape matches requirements (5, 1201).")
        else:
            print(f"WARNING: Unexpected shape {fingers_erp_mean.shape}")
    
        #visualisation
        plot_erps(fingers_erp_mean, pre_ms=200, post_ms=1000)

    except Exception as e:
        print (f"Critical ERROR during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
