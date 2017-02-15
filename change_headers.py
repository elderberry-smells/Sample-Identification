import glob
import os
import pandas as pd
import csv

# using glob to grab a list of only qc data csv files in a folder (path)
path = r'C:\Users\u590135\Code\testing code\csv'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]

results_files = []
for i in result:
    if 'QC-' in i:
        results_files.append(i)
    else:
        continue


header_list = ['Box', 'Well', 'Project', 'FAD 3C Zygosity Call', 'GT73 Zygosity Call',
               'LepR1B Zygosity Call', 'LepR2C Zygosity Call', 'PM2 Zygosity Call', 'CRM2 Zygosity Call',
               'Sask BAR Zygosity Call']

for i in results_files:
    df = pd.read_csv(i)
    new_df = df[header_list]

    new_df.to_csv('results_'+i, index=False)


