# hospital_travel_and_admissions
================================

General code to calculate travel time/distances from LSOA centroids to acute hospitals, with
admission numbers per hospital.


Data
====
In the data subfolder are four files:

1) admissions_by LSOA. This is the yearly admissions to any hospital by LSOA. If this table is
incomplete then the code will fill in missing values with zeros. Order of this table is not
important; the code will sort the order.

2) hospitals. This table contains all acute hospitals. The order of the hospitals must not be
altered and no hospitals can be added or removed. The forth column of the table allows hospitals
to be selected as being able to offer the service under investigation. This column should have a
value of 1 (hospital is open for service) or 0 (hospital is closed). The code truncates the hospital
list just to those hospitals with a 1.

3) travel_matrix_miles. DO NOT CHANGE THIS FILE. This contains estimated road travel distances (from
Maptitude 2016 with MP-MileCharter add-in) from all LSOAs to all acute hospitals.

4) travel_matrix_minutes. DO NOT CHANGE THIS FILE. This contains estimated road travel times (from
Maptitude 2016 with MP-MileCharter add-in) from all LSOAs to all acute hospitals.


Running the code
================
The output folder for results needs to be set. This is set in the first line of the main() function,
which is placed first in the list of functions (all other functions are ordered alphabetically)

By default the travel matrix loaded is travel times, not distances. This may be changed in the
load_data function.


Output files
============
The following output files are generated:

1) binned_admissions_by_distance.csv - this bins admissions by 15 minute or 15 mile bins by default.
The bin value is set in the first line of the summarise_data_by_hospital function. This counts
admissions by time/distance bin. This is not broken down by hospital attended.

2) binned_admissions_by_hospital_and_distance.csv - as (1) but broken dowm by hospital attended.

3) global_results.csv - total admissions and overall average travel time/distance

4) results_by_LSOA.csv - admissions, closest hospital and travel time or distance by LSOA.

5) summary_by_hospital.csv - admissions to each hospital with average travel time for people
travelling to that hospital.


Licence
=======

This code is provided under a permissive Open Source Licence:

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
