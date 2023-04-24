import numpy as np
from GazeParser import Converter
import GazeParser
import os
import pandas as pd
import Plotter

def make_trials_from_datafile(input_path):
    cols            = ["A", "B", "C", "D", "E", "F", "G"]
    main_df         = pd.read_csv(input_path, names=cols)
    failed_idx      = np.where(main_df["D"] == "FAIL")[0]
    main_df.drop(failed_idx, axis = 0, inplace=True)
    message_idx     = np.where(main_df["A"] == "#MESSAGE")[0]
    base_start_idx  = 0
    base_end_idx    = np.where(main_df["A"] == "#CALPOINT")[0][-1] + 1
    end_of_df       = main_df.iloc[-1:]
    num_trials      = 40
    
    main_df.iloc[base_end_idx+1:message_idx[1], :] = main_df.iloc[base_end_idx+1:message_idx[1], :].astype(float)
    main_df.iloc[22, :] = main_df.iloc[22, :].astype(str)
    main_df.iloc[22, 5] = int(main_df.iloc[22, 5].split('.')[0])
    main_df.iloc[22, 6] = int(main_df.iloc[22, 6].split('.')[0])
    base_df             = main_df.iloc[base_start_idx:base_end_idx]

    for idx in range(num_trials):
        start_time    = float(main_df.iloc[[message_idx[2 * idx + 4]]].iloc[0, 1])
        end_time      = float(main_df.iloc[[message_idx[2 * idx + 5]]].iloc[0, 1])
        start_idx     = main_df.iloc[(main_df.iloc[base_end_idx+1:message_idx[1], 0] - start_time).abs().argsort()[:1]].index.values + base_end_idx + 1
        end_idx       = main_df.iloc[(main_df.iloc[base_end_idx+1:message_idx[1], 0] - end_time).abs().argsort()[:1]].index.values + base_end_idx + 1
        frames        = [base_df, main_df.loc[start_idx[0]:end_idx[0]], end_of_df]
        trial_df      = pd.concat(frames)
        trial_df = trial_df.replace(np.nan, '', regex=True)
        path_to_save  = str.replace(input_path, os.path.basename(os.path.normpath(input_path)), "")
        trial_message = main_df.iloc[[message_idx[2 * idx + 4]]].iloc[0, 2]
        start = "4\Slide"
        end   = ".PNG"
        pic_number    = int(trial_message[trial_message.find(start)+len(start):trial_message.rfind(end)])
        with open(path_to_save + str(pic_number) + '.csv', "w") as f:
            f.write("\n".join([l.strip(",") for l in trial_df.to_csv(index=False, header=False).split("\n")]))

def make_output_directory(output_path):
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

if __name__ == "__main__":
    # dataPath = '/Users/apple/Desktop/Amirali/Dehghan/Data'
    # subDataPath = os.listdir(dataPath)
    # subDataPath.pop(0)
    # for sub in subDataPath:
    #     subPath = os.path.join(dataPath, sub)
    #     subCSVFiles = os.listdir(subPath)
    #     for csv in subCSVFiles:
    #         if csv[9] == '4' and csv[-3:] == 'csv':
    #             selected = csv
    #         else:
    #             continue
    #     csvDataPath = os.path.join(subPath, selected)
    #     make_trials_from_datafile(csvDataPath)
    d = Converter.TrackerToGazeParser('/Users/amirali/Desktop/Amirali/NBIC/Dehghan/Data/Amir Parham/18.csv')
    d, a = GazeParser.load('/Users/amirali/Desktop/Amirali/NBIC/Dehghan/Data/Amir Parham/18.db')
    Plotter.drawScatterPlot(d[0], 'Slide18.PNG')