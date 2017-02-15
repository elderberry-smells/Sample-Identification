import glob
import os
import pandas as pd
import csv

# using glob to grab a list of only qc data csv files in a folder (path)
path = r'C:\Users\u590135\Code\testing code\Sample ID'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]

results_files = []
for i in result:
    if 'QC-' in i:
        results_files.append(i)
    else:
        continue

for i in results_files:
    # grab the headers on the sample to make a summary header list for pandas dataframe
    with open(i) as csvinput:
        reader = csv.DictReader(csvinput)
        headerlist = reader.fieldnames

        group_list = []
        for heads in headerlist:
            if 'Zygosity' in heads:
                group_list.append(heads)
            else:
                continue

        print group_list

    # for each csv file in the folder, use the pandas module to "groupby" each set based on the assays in the file,
    # add the count and average to the dataframe in a temp csv file
    df = pd.read_csv(i)
    df1 = df[group_list]

    #  remove lines that have empty wells or no data
    cols_of_interest = ['FAD 3C Zygosity Call']
    df1 = df1[(df[cols_of_interest] != 'Empty').any(axis=1)]
    df1 = df1[(df1[cols_of_interest] != 'No Data').any(axis=1)]

    #  group by same assay results occurance and count
    df2 = df1.groupby(group_list).size().reset_index().rename(columns={0: 'Count'})

    #  add in an average column and sort descending base don count column, write to a new temporary csv
    df3 = df2.copy()
    num = df3['Count'].sum(axis=0)
    df3['Average (%)'] = (df3['Count'] / num) * 100
    df3 = df3.sort_values(['Count'], ascending=[False])

    df3.to_csv('temp.csv', index=False)

    # get the list off of master_id as a dictionary, so you can use the get function for the identification(profile)
    with open('master_id.csv') as master:
        reader = csv.reader(master)

        md = dict((rows[7], rows[0:7]) for rows in reader)

        #  open the summaries of each file and add a profile column, grab the profile from the master_dict
        #  then remove the summary file and keep only the summary with profile version of the file.

        # for files in name_file:
        with open('temp.csv', 'r') as input_file:
            new_reader = csv.reader(input_file)
            d_reader = csv.DictReader(input_file)
            headers = d_reader.fieldnames
            headers.append('Profile')

            with open('results_' + i, 'wb') as outfile:
                dwriter = csv.DictWriter(outfile, fieldnames=headers)
                dwriter.writeheader()

                for line in d_reader:
                    assid = [line['FAD 3C Zygosity Call'], line['GT73 Zygosity Call'], line['LepR1B Zygosity Call'],
                             line['LepR2C Zygosity Call'], line['PM2 Zygosity Call'], line['CRM2 Zygosity Call'],
                             line['Sask BAR Zygosity Call']]
                    try:
                        keys = md.keys()[md.values().index(assid)]
                        end_id = keys.find("(")
                        profile_id = keys[:end_id]
                    except:
                        profile_id = 'not in list - needs to be evaluated'

                    dwriter.writerow({
                        "FAD 3C Zygosity Call": line['FAD 3C Zygosity Call'],
                        "GT73 Zygosity Call": line['GT73 Zygosity Call'],
                        "LepR1B Zygosity Call": line['LepR1B Zygosity Call'],
                        "LepR2C Zygosity Call": line['LepR2C Zygosity Call'],
                        "PM2 Zygosity Call": line['PM2 Zygosity Call'],
                        "CRM2 Zygosity Call": line['CRM2 Zygosity Call'],
                        "Sask BAR Zygosity Call": line['Sask BAR Zygosity Call'],
                        "Count": line['Count'], "Average (%)": line['Average (%)'], "Profile": profile_id})

    os.remove('temp.csv')
