import numpy as np
import pandas as pd


def quantize(float):
    valores = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9, 10, 11, 12, 13, 14, 15, 16]
    value = min(valores, key=lambda x:abs(x-float))
    return value
    
def quantizeBeat(float):
    valores = [1, 2, 4, 8, 16]
    value = min(valores, key=lambda x:abs(x-float))
    return value
    
    

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 10)

filename =  '/Users/angelfaraldo/GoogleDrive/datasets/McGill/MIREX-format/0012/majmin.lab'
        
df = pd.read_table(filename, names=['initTime', 'endTime', 'chord'])

for i in range(len(df)-1):
    if df.chord[i] == df.chord[i+1]:
        df.loc[i+1] = [df.initTime[i], df.endTime[i+1], df.chord[i+1]]
        df = df.drop(i)
        
df = df.reset_index()
df = df.drop(df.columns[0], axis=1)

for i in range(len(df)):
    if type(df.chord[i]) is float:
        df = df.drop(i)

df = df.reset_index()
df = df.drop(df.columns[0], axis=1)

# por seguridad en el cálculo, si la primera o la última fila no es un acorde, la eliminamos:

if df.chord[len(df)-1] is 'N':
    df = df.drop(len(df)-1)   
if df.chord[0] is 'N':
    df = df.drop(0)    
 
df = df.reset_index()
    
df['duration'] = df['endTime'] - df['initTime']

maxVal = quantizeBeat(df.duration.max())

df['proportion'] = maxVal * df['duration'] / df['duration'].max()

quantVals = []
for i in range(len(df)):
    q = quantize(df['proportion'][i])
    quantVals.append(q)
    
df['quantize'] = quantVals
df = df.drop(df.columns[0:3], axis=1)


                 
try:
    for q in range(len(df)+30):
        if df.quantize[q] > 4:
            var1 = int(df.quantize[q] / 4)
            if var1 > 1:
                if df.quantize[q] % 4 != 0:
                    newLine = pd.DataFrame({'chord' : df.chord[q], 'quantize' : df.quantize[q] % 4}, index=[q])
                    df = pd.concat([df.ix[:q], newLine, df.ix[q+1:]]).reset_index(drop=True)
                for i in range(var1):
                    newLine = pd.DataFrame({'chord' : df.chord[q], 'quantize' : 4}, index=[q])
                    df = pd.concat([df.ix[:q+i], newLine, df.ix[q+(i+1):]]).reset_index(drop=True)
            elif var1 == 1:
                if df.quantize[q] % 4 != 0:
                    newLine = pd.DataFrame({'chord' : df.chord[q], 'quantize' : df.quantize[q] % 4}, index=[q])
                    df = pd.concat([df.ix[:q], newLine, df.ix[q+1:]]).reset_index(drop=True)
                newLine = pd.DataFrame({'chord' : df.chord[q], 'quantize' : 4}, index=[q])
                df = pd.concat([df.ix[:q], newLine, df.ix[q+1:]]).reset_index(drop=True)
except:
    pass
    