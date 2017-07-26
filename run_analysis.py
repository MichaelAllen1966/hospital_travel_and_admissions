"""
Analysis of patient travel distances and hospital admissions

Copyright 2017 Michael J Allen

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

"""

import ipdb # Used during dev to trace errors: ipdb.set_trace()
ipdb.set_trace()


# Load libraries
import numpy as np
import pandas as pd
import os, sys

class Data:
    """Data class stores all global data.
    All data is stored in the parent class. No other individual instances of the class exist"""
    OUTPUT_LOCATION = 'output/test'

def align_admissions_and_travel_matrix_data():
    # Ensure admissions by LSOA are in same order as travel matrix and replace any missing values with 0
    travel_matrix_patient_lsoa = pd.DataFrame(Data.travel_matrix.index)
    travel_matrix_patient_lsoa = travel_matrix_patient_lsoa.set_index('LSOA')
    admissions_by_lsoa = pd.concat([travel_matrix_patient_lsoa, loaded_admissions_per_LSOA], axis=1,
                                   join_axes=[travel_matrix_patient_lsoa.index])
    Data.admissions_by_lsoa.fillna(0,inplace=True)
    # Remove loaded admission data now data has been aligned
    del Data.loaded_admissions_per_LSOA
    return()

def check_hospital_list():
    # Check hospital list is same as in travel matrix. Exit if not.
    check_1 = list(Data.travel_matrix) # postcodes of hospitals in travel matrix
    check_2 = Data.hospitals.index.tolist() # postcodes of hospitals in hospital list
    if check_1 != check_2:
        print('Hospital list does not match travel matrix. Quitting')
        sys.exit()
    return()

def create_output_folder(output_folder):
    """If output path and folder do not exist, create them"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return()

def load_data():
    Data.loaded_admissions_per_LSOA = pd.read_csv('data/admissions_by_lsoa.csv',index_col=0)
    Data.travel_matrix = pd.read_csv('data/travel_matrix.csv',index_col=0)
    Data.hospitals=pd.read_csv('data/hospitals.csv',index_col=0)

def main():
    create_output_folder(Data.OUTPUT_LOCATION)
    load_data()
    align_admissions_and_travel_matrix_data()


if __name__ == "__main__":
    main()




# Check hospital list is same as in travel matrix. Exit if not.
check_1 = list(travel_matrix) # postcodes of hospitals in travel matrix
check_2 = hospitals.index.tolist() # postcodes of hospitals in hospital list
if check_1 != check_2:
    print('Hospital list does not match travel matrix. Quitting')
    sys.exit()
del check_1,check_2

