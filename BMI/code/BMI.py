
import sys
import json
from pathlib import Path
import pandas as pd

filename = Path("../data/data.json")
lookupfilename = Path("../data/lookup.json")



def file_name_exists():
    # file exists function, return 1 if dound else 0
    if  filename.exists():
        return 1
    else:
        return 0

def get_body_mass_index(df_row):
    # Calculate BMI for each data frame row
    wtkg =df_row['WeightKg']
    htcm = df_row['HeightCm']
    if wtkg>0 and htcm >0:
        htm = htcm/100
        htm2=htm*2
        result = wtkg/htm2
        return result
    else:
        return 0

def get_min_bmi(df_row):
    # calculate min bmi for each df_row
    bmirange = df_row['BMIRange']
    if 'below' in bmirange:
        return float(0)
    elif 'above' in bmirange:
        return float(bmirange.split()[0].strip())
    elif '-' in bmirange:
        return float(bmirange.split('-')[0].strip())
    else:
        return 0


def get_max_bmi(df_row):
    # calculate min bmi for each df_row
    bmirange = df_row['BMIRange']
    if 'below' in bmirange:
        return float(bmirange.split()[0].strip())
    elif 'above' in bmirange:
        return float(99)
    elif '-' in bmirange:
        return float(bmirange.split('-')[1].strip())
    else:
        return 0

def read_lookupjson_into_df():
    #load category and health risk into data frame
    global lookupdf
    lookupdf = pd.read_json(lookupfilename, orient="columns")
    lookupdf['MinBMI'] = lookupdf.apply(get_min_bmi, axis=1)
    lookupdf['MaxBMI'] = lookupdf.apply(get_max_bmi, axis=1)

def get_bmi_category(df_row):
    #Get BMI Category
    bmi = df_row['BodyMassIndex']
    bmi = round(bmi, 1)
    resultdf = lookupdf.loc[(lookupdf['MaxBMI'] >= bmi) & (lookupdf['MinBMI'] <= bmi)]['BMICategory'].values
    resultdf = str(resultdf)
    resultdf = resultdf.replace("['", "")
    resultdf = resultdf.replace("']", "")
    return str(resultdf)

def get_bmi_healthrisk(df_row):
    #Get BMI health risk
    bmi = df_row['BodyMassIndex']
    bmi = round(bmi, 1)
    resultdf = lookupdf.loc[(lookupdf['MaxBMI'] >= bmi) & (lookupdf['MinBMI'] <= bmi)]['HealthRisk'].values
    resultdf = str(resultdf)
    resultdf = resultdf.replace("['", "")
    resultdf = resultdf.replace("']", "")
    return str(resultdf)

def read_json_into_df():
    # load json data onto pandas data frame. Perform BMI Calculation and look up for category and health risk
    try:
        file_exists = file_name_exists()
        if (file_exists == 1):
            read_lookupjson_into_df()
            df = pd.read_json(filename, orient="columns")
            df['BodyMassIndex'] = df.apply(get_body_mass_index, axis=1)
            df['BMICategory'] = df.apply(get_bmi_category, axis=1)
            df['HealthRisk'] = df.apply(get_bmi_healthrisk, axis=1)
            return df
        else:
            return 'ERROR- File Not Found'
    except:
        return 'ERROR- An exception occured'

dfresult=read_json_into_df()
overweightcountAllGender = dfresult[(dfresult['BMICategory'] == 'Overweight')].count()
print('Total Overweight people: ' + str(overweightcountAllGender))
print ('-------------------------------------')
print ('Information by Gender, BMI Category')
print (dfresult.groupby(['Gender','BMICategory']).size())
print ('------------------------------------')
print ('Information by Gender, Health Risk')
print (dfresult.groupby(['Gender','HealthRisk']).size())
print ('----------------------------------')
print ('Information by Gender, BMI Category - Mean')
print (dfresult.groupby(['Gender','BMICategory']).mean())
print ('----------------------------------')
print ('Information by Gender, BMI Category - Standard Deviation')
print (dfresult.groupby(['Gender','BMICategory']).std())
print ('----------------------------------')
print ('Information by Gender, Health Risk- Standard Deviation')
print (dfresult.groupby(['Gender','HealthRisk']).std())
