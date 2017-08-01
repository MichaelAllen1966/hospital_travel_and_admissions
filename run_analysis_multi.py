"""
Analysis of patient travel distances and hospital admissions

For info/bugs contact michael.allen1966@gmail.com

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

#import ipdb # Used during dev to trace errors: ipdb.set_trace()
#ipdb.set_trace()


# Load libraries
print('Loading libraries')
import numpy as np
import pandas as pd
import os, sys
#import ipdb; ipdb.set_trace()

def main():
    """Main code. Note: All data is stored in Data class. Functions access data in Data class
    directly"""
    # ***************** SET OUTPUT LOCATION BELOW ******************
    Data.OUTPUT_LOCATION = 'output/test'
    # Main code
    create_output_folder(Data.OUTPUT_LOCATION)
    load_data()
    align_admissions_and_travel_matrix_data()
    check_hospital_list()
    initiate_results_tables()
    for scenario in range(Data.scenarios+1):
        print('\nRunning scenario %d of %d' %(scenario+1, Data.scenarios+1))
        truncate_data_to_available_hospitals(scenario)
        identify_closest_hospital()
        combine_admissions_with_closest_hospital()
        summarise_data_by_hospital()
        record_results(scenario)
    save_results()
    print('end')

class Data:
    """Data class stores all global data.
    All data is stored in the parent class. No other individual instances of the class exist.
	Data strored:
		OUTPUT_LOCATION - folder location for output
		admissions_by_lsoa - number of admission by lsoa (dorted to match travel matric)
		hospitals - list of hospitals amrked for whether required specialty is present
		loaded_admissions_per_LSOA - loaded admission by LSOA. Deleted after sorted and stored in
            admissions_by_lsoa
		travel_matrix - distance or time between all LSOAs and all hospitals
		"""
class Results:
    """Stores results data frames in parent class (no individual instances)"""

def align_admissions_and_travel_matrix_data():
    """Ensure admissions by LSOA are in same order as travel matrix and replace any missing values
    with 0"""
    print('Aligning admissions and travel mattrix LSOAs')
    travel_matrix_patient_lsoa = pd.DataFrame(Data.travel_matrix_full.index)
    travel_matrix_patient_lsoa = travel_matrix_patient_lsoa.set_index('LSOA')
    Data.admissions_by_lsoa = pd.concat([travel_matrix_patient_lsoa,
        Data.loaded_admissions_per_LSOA], axis=1,join_axes=[travel_matrix_patient_lsoa.index])
    Data.admissions_by_lsoa.fillna(0,inplace=True)
    # Remove loaded admission data now data has been aligned
    del Data.loaded_admissions_per_LSOA
    return()

def check_hospital_list():
    """Check hospital list is same as in travel matrix. Exit if not."""
    print('Checking hospital list matches travel matrix hospitals')
    check_1 = list(Data.travel_matrix_full) # postcodes of hospitals in travel matrix
    check_2 = Data.hospitals_full.index.tolist() # postcodes of hospitals in hospital list
    if check_1 != check_2:
        print('Hospital list does not match travel matrix. Quitting')
        sys.exit()
    return()

def combine_admissions_with_closest_hospital():
    """Create single table of LSOAs with admissions, closesy hopsital postocde and closest hospital
    distance"""
    print('Collating data')
    Data.results_by_LSOA = pd.concat([Data.admissions_by_lsoa,Data.closest_hospital_postcode,
                                      Data.closest_hospital_distance],axis=1)
    return()

def create_output_folder(output_folder):
    """If output path and folder do not exist, create them"""
    print('Creating output folder')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return()

def identify_closest_hospital():
    """Identifiesd the closest hospital and distance cto closest hospital for each LSOA"""
    print('Identifying the closest available hospital for each LSOA')
    Data.closest_hospital_postcode=pd.DataFrame()
    Data.closest_hospital_postcode['closest_hospital_postcode'] = Data.travel_matrix.idxmin(axis=1)
    Data.closest_hospital_distance=pd.DataFrame()
    Data.closest_hospital_distance['closest_hospital_distance'] = Data.travel_matrix.min(axis=1)
    return()

def initiate_results_tables():
    """Set up dataframes for results"""
    Results.summary_by_hospital_admissions = pd.DataFrame(index = list(Data.hospitals_full.index))
    Results.summary_by_hospital_average_distance = (
        pd.DataFrame(index = list(Data.hospitals_full.index)))
    Results.summary_by_hospital_maximum_distance = (
        pd.DataFrame(index = list(Data.hospitals_full.index)))
    Results.global_results = pd.DataFrame()
    Results.results_by_LSOA_admissions = pd.DataFrame()
    Results.results_by_LSOA_closest_hospital_postcode = pd.DataFrame()
    Results.results_by_LSOA_closest_hospital_distance = pd.DataFrame()
    Results.results_by_LSOA_weighted_distance = pd.DataFrame()
    max_distance=int(max(Data.travel_matrix_full.max())+15)
    distance_bins=list(range(15,max_distance,15))
    Results.binned_admissions_by_distance = pd.DataFrame(index=distance_bins)

def load_data():
    """Load data"""
    print('Loading data')
    Data.loaded_admissions_per_LSOA = pd.read_csv('data/admissions_by_lsoa.csv',index_col=0)
    Data.travel_matrix_full = pd.read_csv('data/travel_matrix_minutes.csv',index_col=0)
    Data.hospitals_full=pd.read_csv('data/hospitals_multi.csv',index_col=0)
    Data.scenarios = Data.hospitals_full.shape[1]-3
    return()

def record_results(scenario):
    """Save results to previously defined output location"""
    print('Recording results')
    # Round results prior to Saving
    scenario_name='scen_'+str(scenario+1)
    Results.summary_by_hospital_admissions[scenario_name] = (
        Data.summary_by_hospital['admissions'].round(decimals=2))
    Results.summary_by_hospital_average_distance[scenario_name] = (
        Data.summary_by_hospital['average_distance'].round(decimals=2))
    Results.summary_by_hospital_maximum_distance[scenario_name] = (
        Data.summary_by_hospital['maximum_distance'].round(decimals=2))
    Results.binned_admissions_by_distance[scenario_name] = (
        Data.binned_admissions_by_distance.round(decimals=2))
    Results.global_results[scenario_name] = Data.global_results.round(decimals = 2)
    Results.results_by_LSOA_admissions[scenario_name] = (
        Data.results_by_LSOA['admissions'].round(decimals=1))
    Results.results_by_LSOA_closest_hospital_postcode[scenario_name] = (
        Data.results_by_LSOA['closest_hospital_postcode'])
    Results.results_by_LSOA_closest_hospital_distance[scenario_name] = (
        Data.results_by_LSOA['closest_hospital_distance'].round(decimals=1))
    Results.results_by_LSOA_weighted_distance[scenario_name] = (
        Data.results_by_LSOA['weighted_distance'].round(decimals=1))
    return()

def save_results():
    """Save results to previously defined output location"""
    print('\nSaving results')
    Results.summary_by_hospital_admissions.fillna(0,inplace=True)
    Results.summary_by_hospital_average_distance.fillna(0,inplace=True)
    Results.summary_by_hospital_maximum_distance.fillna(0,inplace=True)
    Results.summary_by_hospital_maximum_distance.fillna(0,inplace=True)
    (Results.summary_by_hospital_admissions.to_csv
     (Data.OUTPUT_LOCATION+'/summary_by_hospital_admissions.csv'))
    (Results.summary_by_hospital_average_distance.to_csv
     (Data.OUTPUT_LOCATION+'/summary_by_hospital_average_distance.csv'))
    (Results.summary_by_hospital_maximum_distance.to_csv
     (Data.OUTPUT_LOCATION+'/summary_by_hospital_maximum_distance.csv'))
    Results.binned_admissions_by_distance.fillna(value=0,inplace=True)
    (Results.binned_admissions_by_distance.to_csv
     (Data.OUTPUT_LOCATION+'/binned_admissions_by_distance.csv'))
    Results.global_results.to_csv(Data.OUTPUT_LOCATION+'/global_results.csv')
    (Results.results_by_LSOA_admissions.to_csv
     (Data.OUTPUT_LOCATION+'/results_by_LSOA_admissions.csv'))
    (Results.results_by_LSOA_closest_hospital_postcode.to_csv
     (Data.OUTPUT_LOCATION+'/results_by_LSOA_closest_hospital_postcode.csv'))
    (Results.results_by_LSOA_closest_hospital_distance.to_csv
     (Data.OUTPUT_LOCATION+'/results_by_LSOA_closest_hospital_distance.csv'))
    (Results.results_by_LSOA_weighted_distance.to_csv
     (Data.OUTPUT_LOCATION+'/results_by_LSOA_weighted_distance.csv'))


def summarise_data_by_hospital():
    """Summarise admission numbers and distances by hospital. Weighted distances are used for
    averaging travel distances - for each LSOA the average distance is multiplied by the number of
    admissions. The average disatnce for each hospital is then the sum of weighted distances divided
    by the number fo admssions"""
    _bin = 15
    print('Summarising data by hospital')
    _data = Data.results_by_LSOA
    _data['weighted_distance'] = _data['admissions']*_data['closest_hospital_distance']
    _data['binned_distance'] = _data['closest_hospital_distance']/_bin
    _data['binned_distance'] = (_data['binned_distance'].astype(int) * _bin) + _bin
    grouped = _data.groupby(['closest_hospital_postcode'])
    Data.summary_by_hospital = pd.DataFrame()
    Data.summary_by_hospital['admissions'] = grouped['admissions'].sum()
    Data.summary_by_hospital['average_distance'] = (grouped['weighted_distance'].sum() /
                                                    grouped['admissions'].sum())
    Data.summary_by_hospital['maximum_distance'] = (grouped['closest_hospital_distance'].max())

    Data.binned_admissions_by_hospital_and_distance = (pd.pivot_table(_data,
                                         values='admissions',
                                         index=['closest_hospital_postcode'],
                                         columns=['binned_distance'],
                                         aggfunc=np.sum))
    # Create global summary (not grouped by hospital attended)
    # Data.binned_admissions_by_distance = (pd.pivot_table(_data,
    #                                          values='admissions',
    #                                          columns=['binned_distance'],
    #                                          aggfunc=np.sum))
    Data.binned_admissions_by_distance=_data.groupby(['binned_distance'])['admissions'].sum()
    Data.global_results=pd.Series()
    Data.global_results['total_admissions'] = _data['admissions'].sum()
    Data.global_results['average_distance'] = (_data['weighted_distance'].sum()/
                                               _data['admissions'].sum())
    Data.global_results['maximum_distance'] = _data['closest_hospital_distance'].max()

    return()

def truncate_data_to_available_hospitals(scenario):
    """Truncates hospital list and travel matrix to only those hospitals marked as available in the
    hospital list"""
    print('Truncating data to available hospitals')
    # Truncate hopsital table
    mask = Data.hospitals_full.iloc[:,[scenario+2]]
    mask = mask.values==1
    mask = mask.flatten()
    Data.hospitals = Data.hospitals_full.loc[mask]
    # Get available hospital postcodes and truncate travel matrix
    hospital_list = Data.hospitals.index
    Data.travel_matrix = Data.travel_matrix_full[hospital_list]
    return()

if __name__ == "__main__":
    main()
