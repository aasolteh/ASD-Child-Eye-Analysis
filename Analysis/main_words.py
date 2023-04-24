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
    num_trials      = message_idx.shape[0]
    # print(message_idx.shape)
    
    main_df.iloc[base_end_idx+1:message_idx[1], :] = main_df.iloc[base_end_idx+1:message_idx[1], :].astype(float)
    main_df.iloc[22, :] = main_df.iloc[22, :].astype(str)
    main_df.iloc[22, 5] = int(main_df.iloc[22, 5].split('.')[0])
    main_df.iloc[22, 6] = int(main_df.iloc[22, 6].split('.')[0])
    base_df             = main_df.iloc[base_start_idx:base_end_idx]

    for idx in range(0, int(num_trials/2-2)):
        start_time    = float(main_df.iloc[[message_idx[2 * idx + 4]]].iloc[0, 1])
        end_time      = float(main_df.iloc[[message_idx[2 * idx + 5]]].iloc[0, 1])
        start_idx     = main_df.iloc[(main_df.iloc[base_end_idx+1:message_idx[1], 0] - start_time).abs().argsort()[:1]].index.values + base_end_idx + 1
        end_idx       = main_df.iloc[(main_df.iloc[base_end_idx+1:message_idx[1], 0] - end_time).abs().argsort()[:1]].index.values + base_end_idx + 1
        frames        = [base_df, main_df.loc[start_idx[0]:end_idx[0]], end_of_df]
        trial_df      = pd.concat(frames)
        trial_df = trial_df.replace(np.nan, '', regex=True)
        path_to_save  = str.replace(input_path, os.path.basename(os.path.normpath(input_path)), "")
        trial_message = main_df.iloc[[message_idx[2 * idx + 4]]].iloc[0, 2]
        start         = trial_message.split('= ')[-1].split(".")[0]
        print(start)
        pic_number    = start.split('e')[-1]
        with open(path_to_save + start.split("\\")[0] + '-' + pic_number + '.csv', "w") as f:
            f.write("\n".join([l.strip(",") for l in trial_df.to_csv(index=False, header=False).split("\n")]))

def make_output_directory(output_path):
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

if __name__ == "__main__":
    dataPath = '/Users/amirali/Desktop/Amirali/NBIC/Dehghan/Data/Words'
    subDataPath = os.listdir(dataPath)
    subDataPath.remove('.DS_Store')
    for sub in subDataPath:
        print(sub)
        subPath = os.path.join(dataPath, sub)
        subCSVFiles = os.listdir(subPath)
        if '.DS_Store' in subCSVFiles:
            subCSVFiles.remove('.DS_Store')
        for csv in subCSVFiles:
            if csv == 'datafile_123.csv' or csv == 'datafile_1.csv' or csv == 'datafile_23.csv':
                selected = csv
            else:
                continue
        csvDataPath = os.path.join(subPath, selected)
        make_trials_from_datafile(csvDataPath)
    # d = Converter.TrackerToGazeParser('/Users/amirali/Desktop/Amirali/NBIC/Dehghan/Data/Amir Parham/18.csv')
    # d, a = GazeParser.load('/Users/amirali/Desktop/Amirali/NBIC/Dehghan/Data/Amir Parham/18.db')
    # Plotter.drawScatterPlot(d[0], 'Slide18.PNG')