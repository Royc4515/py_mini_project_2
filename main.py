import os

from src.erp import calc_mean_erp_from_files, plot_erps

EVENTS_PATH = os.path.join("mini_project_2_data", "events_file_ordered.csv")
ECOG_PATH = os.path.join("mini_project_2_data", "brain_data_channel_one.csv")

def main()-> None:
    print("=== MiniProject 2: ERP analysis ===")

    #check that the data files exist
    if not os.path.exists(EVENTS_PATH):
        print(f"ERROR: events file does not found at {EVENTS_PATH}")
        return
    if not os.path.exists(ECOG_PATH):
        print(f"ERROR: brain data channel does not found at {ECOG_PATH}")
        return

    #compute the ERP matrix
    fingers_erp_mean = calc_mean_erp_from_files(trial_points_path=EVENTS_PATH, ecog_data_path=ECOG_PATH,
                                                pre_ms=200, post_ms=1000)
    #basic verification
    print("ERP matrix shape:", fingers_erp_mean.shape)
    if fingers_erp_mean.shape == (5,1201):
        print("OK ✅ Shape is (5,1201) as required.")
    else:
        print("⚠️ Warning: unexpected ERP shape, please check the code/data.")

    #plot the ERPs
    plot_erps(fingers_erp_mean, pre_ms=200, post_ms=1000)

if __name__ == "__main__":
    main()