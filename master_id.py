import os
import pandas as pd
import csv

file_name = 'updated_master_id.csv'

#  read the master id file and get everything similar grouped, write a new file and get that into a dictionary
with open(file_name) as csvinput:
        reader = csv.DictReader(csvinput)
        headerlist = reader.fieldnames

        group_list = []

        for heads in headerlist:
            if 'Zygosity' in heads:
                group_list.append(heads)
            else:
                continue



df = pd.read_csv(file_name)
new_df = df[group_list]

df1 = new_df.groupby(group_list).size().reset_index().rename(columns={0: 'count'})

df1.to_csv('1_' + file_name, index=False)