# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 15:46:57 2019

@author: user8
"""

import os
import os.path
import pandas as pd
import re
import matplotlib.pyplot as plt
import pandas as pd
import glob
import seaborn as sns
sns.set()


#Read excel files from a folder and merge into a single excel file
path = os.getcwd()
files = os.listdir(path)

files_xlsx = [f for f in files if f[-4:] == 'xlsx']

df = pd.DataFrame()
for f in files_xlsx:
    data = pd.read_excel(f, 'Sheet1')
    file = list(os.path.splitext(f))[0]
    data['Filename'] = [file]*len(data)
    df = df.append(data)
    df = df.reset_index(drop=True)
    


#Finding L1, L2 and L3 transporters

group = df[['Lot Number','Filename','Annual Lane Spend']].groupby(['Lot Number','Filename']).sum()
group['combined'] = group.index
group['Lot Number'] = group['combined'].apply(lambda x:x[0])
group['Transporter Name'] = group['combined'].apply(lambda x:x[1])

group = group.reset_index(drop=True)
group = group.drop(['combined'], axis=1)

list1 = list(pd.unique(group['Lot Number']))
final = pd.DataFrame()
    
for i in list1:
    dfh = group[group['Lot Number']==i]
    dfh = dfh.sort_values(by='Annual Lane Spend', ascending=True)
    if len(dfh) > 3:
        dfh = dfh.iloc[0:3,:]
        dfh['Winners'] = ['L1', 'L2', 'L3']
    final = final.append(dfh)
final = final.reset_index(drop=True)
final = final.rename(columns = {"Annual Lane Spend":"Transporter Spend"})

'''        
final['winners'].groupby([''])

final['Annual Lane Spend'].iloc[0:3].sum()
'''

#Read Baseline rate card
'''
d = os.path.dirname(os.getcwd())
b = os.listdir(d)
b_xlsx = []
for i in b:
    x = i.split('.')
    try:
        if (x[1] == 'xlsx'):
            b_xlsx.append(i)    
    except Exception:
        pass

baseline = pd.DataFrame()
for f in b_xlsx:
    base = pd.read_excel(f, 'Sheet1')
    baseline = baseline.append(base)
    baseline = baseline.reset_index(drop=True)   
'''   
    
baseline = pd.read_excel(r'D:\User8\Shrikanth\Project\Baseline.xlsx')    
baseline_final = baseline[['Lot Number', 'Annual Lane Spend']].groupby(['Lot Number']).sum()
baseline_final = baseline_final.reset_index()
baseline_final = baseline_final.rename(columns = {"Annual Lane Spend":"Baseline Spend"})

#baseline_final['Lot Number'] = baseline_final.index

baseline_sum = baseline_final['Baseline Spend'].sum()

#To find escalations from L1, L2 and L3

merge = pd.merge(baseline_final, final, how='right', on='Lot Number')


#Overall escalation

escalation = (merge[['Winners','Baseline Spend', 'Transporter Spend']].groupby("Winners").sum())
escalation = escalation.reset_index()

difference = []
escalation1 = []

for i in range(len(escalation)):    
    difference.append(escalation['Transporter Spend'][i] - escalation['Baseline Spend'][i])
    x = escalation['Transporter Spend'][i] - escalation['Baseline Spend'][i]
    escalation1.append((x/escalation['Baseline Spend'][i])*100)

esc = pd.DataFrame({'Difference':difference, 'Escalation (in %)':escalation1, 'Winners':['L1','L2','L3']})

total_esc = pd.merge(escalation, esc, how='right', on='Winners')

#Lot Level Escalation
'''
lot_esc = pd.DataFrame()
for i in range(len(merge))
'''





#Pie Chart
def pie(pie_type):
    df1 = df[df['Filename'] == 'R1']
    count=df1[pie_type].value_counts()
    count = count.reset_index()
    plt.pie(x=count[pie_type], labels=count['index'], autopct='%.1f%%')
    
pie('Truck Type')

'''
count=df['Product Type'].value_counts()
count = count.reset_index()
plt.pie(x=count['Product Type'], labels=count['index'], autopct='%.1f%%')

count=df['Origin State'].value_counts()
count = count.reset_index()
plt.pie(x=count['Origin State'], labels=count['index'], autopct='%.1f%%')
'''

#Bar graph
'''Between type(Column) and annual trips'''
def bar(type):   
    bar = (baseline[[type,'Annual Trips']].groupby(type).sum())
    bar = bar.reset_index()
    bar.plot.bar(x=type, y='Annual Trips')
    
bar('Origin State')


#plt.plot(merge['Winners'], merge[['Baseline Spend']=='L1'])

#Summary


def get_uni(df, column):
    return len(df[column].unique())

listdata = []
for column in baseline.columns:
    temp_data = {}
    temp_data['Entity'] = column 
    temp_data['Count'] = get_uni(baseline, column)
    listdata.append(temp_data)
    
count_summary = pd.DataFrame(listdata)
count_summary = count_summary[['Entity', 'Count']]

plt.plot(count_summary['Entity'], count_summary['Count'])


#PTPK
TT = []

def numerical(s):
    return re.sub("\D", "", s)

numerical(df['Truck Type'])

for i in range(len(df)):
    df['PTPK'] = df['Rate \n(Per Truckload)'][i]/(df['Distance (in km)'][i]*9)
    



    
    


