import numpy as np
import pandas as pd
import random as rnd
import csv

from math import floor

import time

start_time = time.time()

FRACTION_POPULATION = 100
print



print "Fraction of Population (1 / x): ", FRACTION_POPULATION

def age_split(dataframe):

	age_min = []
	age_max = []
	list_index = range(len(dataframe.index))

	for index in list_index:

		if '-' in dataframe['age group'][ i ]:
			age_split = dataframe['age group'][ i ].split('-')
			age_split = map(int, age_split)
			if age_split[ 0 ] == 20:
				age_min.append(18)
			else:
				age_min.append(age_split[ 0 ])
			age_max.append(age_split[ 1 ])
		else:
			tmp_age = int(dataframe['age group'][ i ])
			age_min.append(tmp_age)
			age_max.append(tmp_age)

	dataframe.loc[ : , 'age_min'] = pd.Series(age_min, index=list_index)	
	dataframe.loc[ : , 'age_max'] = pd.Series(age_max, index=list_index)

	return dataframe




census = pd.read_csv('census.csv')

state_list = census.state.unique()

state_census = {}

for state in state_list:

	print "Reading Census Data for State: ", state
	tmp_census = census[ census.state == state ]
	tmp_census.index = range(len(tmp_census.index))

	age_min = []
	age_max = []
	pop_cdf = []

	tmp_pop = 0
	state_entries = range(len(tmp_census.index))
	for i in state_entries:

		if i == 0:
			tmp_pop = tmp_census['group population'][ i ]
			pop_cdf.append(tmp_pop)
		else:
			tmp_pop += tmp_census['group population'][ i ]
			pop_cdf.append(tmp_pop)

		if '-' in tmp_census['age group'][ i ]:
			age_split = tmp_census['age group'][ i ].split('-')
			age_split = map(int, age_split)
			age_min.append(age_split[ 0 ])
			age_max.append(age_split[ 1 ])
		else:
			tmp_age = int(tmp_census['age group'][ i ])
			age_min.append(tmp_age)
			age_max.append(tmp_age)

	tmp_census.loc[ : , 'age_min'] = pd.Series(age_min, index=state_entries)	
	tmp_census.loc[ : , 'age_max'] = pd.Series(age_max, index=state_entries)
	tmp_census.loc[ : , 'pop_cdf'] = pd.Series(pop_cdf, index=state_entries)

	state_census[ state ] = tmp_census


print



height_df = pd.read_csv('nchs_heights.csv')
waist_df = pd.read_csv('nchs_waist.csv')
weight_df = pd.read_csv('nchs_weights.csv')

age_min = []
age_max = []
list_index = range(len(height_df.index))

for i in list_index:

	print "Reading Height Data"

	if '-' in height_df['age group'][ i ]:
		age_split = height_df['age group'][ i ].split('-')
		age_split = map(int, age_split)
		if age_split[ 0 ] == 20:
			age_min.append(18)
		else:
			age_min.append(age_split[ 0 ])
		age_max.append(age_split[ 1 ])
	else:
		tmp_age = int(height_df['age group'][ i ])
		age_min.append(tmp_age)
		age_max.append(tmp_age)

height_df.loc[ : , 'age_min'] = pd.Series(age_min, index=list_index)	
height_df.loc[ : , 'age_max'] = pd.Series(age_max, index=list_index)


print


age_min = []
age_max = []
list_index = range(len(waist_df.index))

for i in list_index:

	print "Reading Waist Data for State"

	if '-' in waist_df['age group'][ i ]:
		age_split = waist_df['age group'][ i ].split('-')
		age_split = map(int, age_split)
		if age_split[ 0 ] == 20:
			age_min.append(18)
		else:
			age_min.append(age_split[ 0 ])
		age_max.append(age_split[ 1 ])
	else:
		tmp_age = int(waist_df['age group'][ i ])
		age_min.append(tmp_age)
		age_max.append(tmp_age)

waist_df.loc[ : , 'age_min'] = pd.Series(age_min, index=list_index)	
waist_df.loc[ : , 'age_max'] = pd.Series(age_max, index=list_index)


print


age_min = []
age_max = []
list_index = range(len(weight_df.index))

for i in list_index:

	print "Reading Weight Data for State"

	if '-' in weight_df['age group'][ i ]:
		age_split = weight_df['age group'][ i ].split('-')
		age_split = map(int, age_split)
		if age_split[ 0 ] == 20:
			age_min.append(18)
		else:
			age_min.append(age_split[ 0 ])
		age_max.append(age_split[ 1 ])
	else:
		tmp_age = int(weight_df['age group'][ i ])
		age_min.append(tmp_age)
		age_max.append(tmp_age)

weight_df.loc[ : , 'age_min'] = pd.Series(age_min, index=list_index)	
weight_df.loc[ : , 'age_max'] = pd.Series(age_max, index=list_index)

#print height_df
#print waist_df
#print weight_df


print



state_sample_list = {}
tmp_state_list = {k : state_census[k] for k in state_census}


total_sample_size = 0

for state in tmp_state_list:

	print "Generating State, Age, Ethnicity, Gender data for state: ", state

	state_information = tmp_state_list[ state ]
	state_population = state_information['pop_cdf'].max()
	sample_population = int(state_population / FRACTION_POPULATION)
	tmp_state = pd.Series([state for i in range(sample_population)], \
						index=range(sample_population))
	tmp_group_cdf = pd.Series(state_information['pop_cdf'])

	print "\t\t Sample state Population: ", sample_population
	total_sample_size += sample_population

	SEQN = rnd.sample(range(state_population), sample_population)
#	print SEQN
	#print tmp_group_cdf 

	age = []
	ethnicity = []
	gender = []
	min_idx = 0
	age_min_pl = 0.0
	age_max_pl = 0.0
	age_calc_pl = 0.0

	for person_id in SEQN:

		min_idx = tmp_group_cdf[ tmp_group_cdf[ : ] > person_id ].argmin()

		ethnicity.append(state_information['ethnicity'][ min_idx ])
		gender.append(state_information['gender'][ min_idx ])

		age_min_pl = float(state_information['age_min'][ min_idx ])
		age_max_pl = float(state_information['age_max'][ min_idx ])
		age_calc_pl = age_min_pl + rnd.random() * (age_max_pl - age_min_pl)

		age.append(age_calc_pl)


	tmp_state_sample = {}
	tmp_state_sample = tmp_state

	#tmp_state_sample['age'] = pd.Series(age, index=range(sample_population))
	#tmp_state_sample['ethnicity'] = pd.Series(ethnicity, index=range(sample_population))
	#tmp_state_sample['gender'] = pd.Series(gender, index=range(sample_population))

	tmp_state_sample_df = pd.DataFrame(SEQN, index=range(sample_population))
	tmp_state_sample_df['state'] = pd.Series(tmp_state_sample, index=range(sample_population))
	tmp_state_sample_df['gender'] = pd.Series(gender, index=range(sample_population))
	tmp_state_sample_df['age'] = pd.Series(age, index=range(sample_population))
	tmp_state_sample_df['ethnicity'] = pd.Series(ethnicity, index=range(sample_population))


	tmp_state_sample_df = tmp_state_sample_df.rename(columns = {0 : 'SEQN'})

	state_sample_list[ state ] = tmp_state_sample_df


print
print "Sample Size of all States Combined: ", total_sample_size
print


for state in state_sample_list:

	height = []
	waist = []
	weight = []

	print "Generating Height, Waist, Weight data for state: ", state
#	print state_sample_list[ state ]
#	print state

	state_information = state_sample_list[ state ]
	sample_population_list = range(len(state_information.index))

	for person in sample_population_list:
		tmp_height_df = height_df[ height_df['gender'] == \
							state_information['gender'][ person ] ]
		tmp_waist_df = waist_df[ waist_df['gender'] == \
							state_information['gender'][ person ] ]
		tmp_weight_df = weight_df[ waist_df['gender'] == \
							state_information['gender'][ person ] ]						


		if (state_information['ethnicity'][ person ] == 'Black') or \
			(state_information['ethnicity'][ person ] == 'Hisp'):
			tmp_height_df = tmp_height_df[ tmp_height_df['ethnicity'] == \
							state_information['ethnicity'][ person ] ]
			tmp_waist_df = tmp_waist_df[ tmp_waist_df['ethnicity'] == \
							state_information['ethnicity'][ person ] ]
			tmp_weight_df = tmp_weight_df[ tmp_weight_df['ethnicity'] == \
							state_information['ethnicity'][ person ] ]			


		elif (state_information['ethnicity'][ person ] == 'WhiteNonHisp'):
			tmp_height_df = tmp_height_df[ tmp_height_df['ethnicity'] == 'White']
			tmp_waist_df = tmp_waist_df[ tmp_waist_df['ethnicity'] == 'White']
			tmp_weight_df = tmp_weight_df[ tmp_weight_df['ethnicity'] == 'White']


		else:
			tmp_height_df = tmp_height_df[ tmp_height_df['ethnicity'] == 'All']
			tmp_waist_df = tmp_waist_df[ tmp_waist_df['ethnicity'] == 'All']
			tmp_weight_df = tmp_weight_df[ tmp_weight_df['ethnicity'] == 'All']




		if state_information['age'][ person ] < 18.0:
			height.append(0.0)
			waist.append(0.0)
			weight.append(0.0)
			continue

		else:
			min_idx_height = tmp_height_df[ tmp_height_df[ : ]['age_max'] >= \
								floor(state_information['age'][ person ])]['age_max'].argmin()

			min_idx_waist = tmp_waist_df[ tmp_waist_df[ : ]['age_max'] >= \
								floor(state_information['age'][ person ])]['age_max'].argmin()

			min_idx_weight = tmp_weight_df[ tmp_weight_df[ : ]['age_max'] >= \
								floor(state_information['age'][ person ])]['age_max'].argmin()

			
			tmp_height_df = tmp_height_df.ix[ min_idx_height ]
			tmp_waist_df = tmp_waist_df.ix[ min_idx_waist ]
			tmp_weight_df = tmp_weight_df.ix[ min_idx_weight ]



			rnd_height = 100 * rnd.random()
			rnd_waist = 100 * rnd.random()
			rnd_weight = 100 * rnd.random()

			height_val_pl = 0.0
			waist_val_pl = 0.0
			weight_val_pl = 0.0


			if rnd_height > 95.0:
				height_val_pl = (tmp_height_df['95'] - tmp_height_df['90']) / 5.0
				height_val_pl = tmp_height_df['95'] + (height_val_pl * (rnd_height - 95.0))

			elif rnd_height > 90.0:
				height_val_pl = (tmp_height_df['95'] - tmp_height_df['90']) / 5.0
				height_val_pl = tmp_height_df['90'] + (height_val_pl * (rnd_height - 90.0))

			elif rnd_height > 85.0:
				height_val_pl = (tmp_height_df['90'] - tmp_height_df['85']) / 5.0
				height_val_pl = tmp_height_df['85'] + (height_val_pl * (rnd_height - 85.0))

			elif rnd_height > 75.0:
				height_val_pl = (tmp_height_df['85'] - tmp_height_df['75']) / 10.0
				height_val_pl = tmp_height_df['75'] + (height_val_pl * (rnd_height - 75.0))

			elif rnd_height > 50.0:
				height_val_pl = (tmp_height_df['75'] - tmp_height_df['50']) / 25.0
				height_val_pl = tmp_height_df['50'] + (height_val_pl * (rnd_height - 50.0))

			elif rnd_height > 25.0:
				height_val_pl = (tmp_height_df['50'] - tmp_height_df['25']) / 25.0
				height_val_pl = tmp_height_df['25'] + (height_val_pl * (rnd_height - 25.0))

			elif rnd_height > 15.0:
				height_val_pl = (tmp_height_df['25'] - tmp_height_df['15']) / 10.0
				height_val_pl = tmp_height_df['15'] + (height_val_pl * (rnd_height - 15.0))

			elif rnd_height > 10.0:
				height_val_pl = (tmp_height_df['15'] - tmp_height_df['10']) / 5.0
				height_val_pl = tmp_height_df['10'] + (height_val_pl * (rnd_height - 10.0))

			elif rnd_height > 5.0:
				height_val_pl = (tmp_height_df['10'] - tmp_height_df['5']) / 5.0
				height_val_pl = tmp_height_df['5'] + (height_val_pl * (rnd_height - 5.0))

			else:
				height_val_pl = (tmp_height_df['10'] - tmp_height_df['5']) / 5.0
				height_val_pl = tmp_height_df['5'] - (height_val_pl * (rnd_height - 5.0))




			if rnd_waist > 95.0:
				waist_val_pl = (tmp_waist_df['95'] - tmp_waist_df['90']) / 5.0
				waist_val_pl = tmp_waist_df['95'] + (waist_val_pl * (rnd_waist - 95.0))

			elif rnd_waist > 90.0:
				waist_val_pl = (tmp_waist_df['95'] - tmp_waist_df['90']) / 5.0
				waist_val_pl = tmp_waist_df['90'] + (waist_val_pl * (rnd_waist - 90.0))

			elif rnd_waist > 85.0:
				waist_val_pl = (tmp_waist_df['90'] - tmp_waist_df['85']) / 5.0
				waist_val_pl = tmp_waist_df['85'] + (waist_val_pl * (rnd_waist - 85.0))

			elif rnd_waist > 75.0:
				waist_val_pl = (tmp_waist_df['85'] - tmp_waist_df['75']) / 10.0
				waist_val_pl = tmp_waist_df['75'] + (waist_val_pl * (rnd_waist - 75.0))

			elif rnd_waist > 50.0:
				waist_val_pl = (tmp_waist_df['75'] - tmp_waist_df['50']) / 25.0
				waist_val_pl = tmp_waist_df['50'] + (waist_val_pl * (rnd_waist - 50.0))

			elif rnd_waist > 25.0:
				waist_val_pl = (tmp_waist_df['50'] - tmp_waist_df['25']) / 25.0
				waist_val_pl = tmp_waist_df['25'] + (waist_val_pl * (rnd_waist - 25.0))

			elif rnd_waist > 15.0:
				waist_val_pl = (tmp_waist_df['25'] - tmp_waist_df['15']) / 10.0
				waist_val_pl = tmp_waist_df['15'] + (waist_val_pl * (rnd_waist - 15.0))

			elif rnd_waist > 10.0:
				waist_val_pl = (tmp_waist_df['15'] - tmp_waist_df['10']) / 5.0
				waist_val_pl = tmp_waist_df['10'] + (waist_val_pl * (rnd_waist - 10.0))

			elif rnd_waist > 5.0:
				waist_val_pl = (tmp_waist_df['10'] - tmp_waist_df['5']) / 5.0
				waist_val_pl = tmp_waist_df['5'] + (waist_val_pl * (rnd_waist - 5.0))

			else:
				waist_val_pl = (tmp_waist_df['10'] - tmp_waist_df['5']) / 5.0
				waist_val_pl = tmp_waist_df['5'] - (waist_val_pl * (rnd_waist - 5.0))



			if rnd_weight > 95.0:
				weight_val_pl = (tmp_weight_df['95'] - tmp_weight_df['90']) / 5.0
				weight_val_pl = tmp_weight_df['95'] + (weight_val_pl * (rnd_weight - 95.0))

			elif rnd_weight > 90.0:
				weight_val_pl = (tmp_weight_df['95'] - tmp_weight_df['90']) / 5.0
				weight_val_pl = tmp_weight_df['90'] + (weight_val_pl * (rnd_weight - 90.0))

			elif rnd_weight > 85.0:
				weight_val_pl = (tmp_weight_df['90'] - tmp_weight_df['85']) / 5.0
				weight_val_pl = tmp_weight_df['85'] + (weight_val_pl * (rnd_weight - 85.0))

			elif rnd_weight > 75.0:
				weight_val_pl = (tmp_weight_df['85'] - tmp_weight_df['75']) / 10.0
				weight_val_pl = tmp_weight_df['75'] + (weight_val_pl * (rnd_weight - 75.0))

			elif rnd_weight > 50.0:
				weight_val_pl = (tmp_weight_df['75'] - tmp_weight_df['50']) / 25.0
				weight_val_pl = tmp_weight_df['50'] + (weight_val_pl * (rnd_weight - 50.0))

			elif rnd_weight > 25.0:
				weight_val_pl = (tmp_weight_df['50'] - tmp_weight_df['25']) / 25.0
				weight_val_pl = tmp_weight_df['25'] + (weight_val_pl * (rnd_weight - 25.0))

			elif rnd_weight > 15.0:
				weight_val_pl = (tmp_weight_df['25'] - tmp_weight_df['15']) / 10.0
				weight_val_pl = tmp_weight_df['15'] + (weight_val_pl * (rnd_weight - 15.0))

			elif rnd_weight > 10.0:
				weight_val_pl = (tmp_weight_df['15'] - tmp_weight_df['10']) / 5.0
				weight_val_pl = tmp_weight_df['10'] + (weight_val_pl * (rnd_weight - 10.0))

			elif rnd_weight > 5.0:
				weight_val_pl = (tmp_weight_df['10'] - tmp_weight_df['5']) / 5.0
				weight_val_pl = tmp_weight_df['5'] + (weight_val_pl * (rnd_weight - 5.0))

			else:
				weight_val_pl = (tmp_weight_df['10'] - tmp_weight_df['5']) / 5.0
				weight_val_pl = tmp_weight_df['5'] - (weight_val_pl * (rnd_weight - 5.0))



		height.append(height_val_pl)
		waist.append(waist_val_pl)
		weight.append(weight_val_pl)




	state_sample_list[ state ]['Height'] = pd.Series(height, index=range(len(height)))
	state_sample_list[ state ]['Waist'] = pd.Series(waist, index=range(len(waist)))
	state_sample_list[ state ]['Weight'] = pd.Series(weight, index=range(len(weight)))


print


for state in state_sample_list:

	print "Cleaning Data for Health Statistics for state: ", state

	BMI = []
	WtHR = []
	tmp_BMI = 0.0
	tmp_WtHR = 0.0

	state_information = state_sample_list[ state ]

	mask_male = state_information['gender'] == 'Male'
	mask_female = state_information['gender'] == 'Female'
	state_information.loc[mask_male, 'gender'] = 'M'
	state_information.loc[mask_female, 'gender'] = 'F'


	for person in range(len(state_information.index)):
		tmp_BMI = 10000 * state_information['Weight'][ person ] / \
					(state_information['Height'][ person ] ** 2)
		BMI.append(tmp_BMI)

		WtHR.append(state_information['Waist'][ person ] / 
					state_information['Height'][ person ])

	state_sample_list[ state ]['BMI'] = pd.Series(BMI, index=range(len(BMI)))
	state_sample_list[ state ]['WtHR'] = pd.Series(WtHR, index=range(len(WtHR)))

	state_sample_list[ state ].columns = ['SEQN', 'State', 'Gender', 'Age_years', 
										'Ethnicity', 'Height', 'Waist', 'Weight', \
										'BMI', 'WtHR']

	state_sample_list[ state ] = state_information[ state_information ['Age_years'] >= 18.0]

print


##########################################################


#	Importing Data as a DataFrame object
#	The imported data has the following columns:
#
#	1) 	SEQN 			(Participant ID)
#	2) 	Gender 			(Male == M, Female == F)
#	3) 	Age_years
#	4) 	Age_months
#	5) 	Weight 			(kg)
#	6)	Height			(cm)
#	7) 	BMI				(kg/m^2)
# 	8) 	Waist			(cm)
#	9) 	HR 				(Heart Rate in 60s, 30s HR * 2)
#	10)	Avg_Sys			(Average Systolic Blood Pressure)
#	11)	Avg_Dia			(Average Diastolic Bloot Pressure)
#	12)	Tri				(Triglyceride Levels, mg/dL)
#	13) LDL				(Low-Density Cholesterol Levels, mg/dL)
#	14)	HDL 	 		(High-Density Cholesterol Levels, mg/dL)
#	15)	Vig_YN			(Does the participant partake in at least vigorous
#							recreational activities for at least 10 min,
#							Y == 1, N == 2)
#	16)	Vig_DW			(If Vig_YN == 1, how many days a week)
#	17) Vig_MD			(If Vig_YN == 1, how many minutes a day)
#	18)	Mod_YN			(Does the participant partake in at least mdoerate
#							recreational activities for at least 10 min)
#	19)	Mod_DW			(If Mod_YN == 1, how many days a week)
#	20) Mod_MD			(If Mod_YN == 1, how many minutes a day)

print "Reading Nation NHANES data"
print

df = pd.read_csv('HealthData_10_16_2015.csv')

#	Filtering any entry that does not have any of
#	the following specified:
#
#	1) Gender
#	2) Age in years
#	3) Weight in kg
#	4) Height in cm
#	5) Waist line in cm
#
#	All applicants Age < 18 are excluded
#	
#	Modifying entries of exercising so that participants that answered
#	no for vigorous or moderate exercise will have 0 for fields that
#	ask if they exercise, how many days per week do you exercise, and
#	how many minutes per day do you exercise

df = df[df.Gender.notnull() & df.Age_years.notnull() & df.Weight.notnull() \
			& df.Height.notnull() & df.Waist.notnull()]

df = df[df['Age_years'] > 17]

mask_vig = df['Vig_YN'] == 2
df.loc[mask_vig, 'Vig_YN'] = 0
df.loc[mask_vig, 'Vig_DW'] = 0
df.loc[mask_vig, 'Vig_MD'] = 0

mask_mod = df['Mod_YN'] == 2
df.loc[mask_mod, 'Mod_YN'] = 0
df.loc[mask_mod, 'Mod_DW'] = 0
df.loc[mask_mod, 'Mod_MD'] = 0

#print df

#	Creating a DataFrame from previously filtered entires
#	to remove any remaining entries that have any missing
#	heart rate information

df_hr = df[df.HR.notnull()]
df_hr.index = range(len(df_hr.index))

#	Removing columns in dataframe so that only attributes
#	and heart rate information remains

df_hr = df_hr.drop(df_hr.columns[[ 9, 10, 11, 12, 13 ]], axis=1)

#	Reorganizing the dataframe so as to move heart rate (HR)
#	to the end of the dataframe. This provides the final
#	format to split the data into test and training datasets

cols = list(df_hr)
cols.insert(len(cols), cols.pop(cols.index('HR')))
df_hr = df_hr.ix[: , cols]

#print df_hr

#	Creating a DataFrame from previously filtered entries
#	to remove any remaining entries that have any missing
#	blood pressure information
#	The new DataFrame also has reindexed row numbers

df_bp = df[df.Avg_Sys.notnull() & df.Avg_Dia.notnull()]
df_bp.index = range(len(df_bp.index))

#	Removing columns in dataframe so that only attributes
#	and blood pressure information remains

df_bp = df_bp.drop(df_bp.columns[[ 8, 11, 12, 13 ]], axis=1)

#	Reorganizing the dataframe so as to move Blood Pressure,
#	Avg_Sys and Avg_Dia, to the end of the dataframe. This 
#	provides the final format to split the data into test 
#	and training datasets

cols = list(df_bp)
cols.insert(len(cols), cols.pop(cols.index('Avg_Sys')))
cols.insert(len(cols), cols.pop(cols.index('Avg_Dia')))
df_bp = df_bp.ix[: , cols]

#print df_bp

#	Creating a DataFrame from previously filtered entries
#	to remove any remaining entries that have any missing
#	cholesterol information

df_ch = df[df.Tri.notnull() & df.LDL.notnull() & df.HDL.notnull()] 
df_ch.index = range(len(df_ch.index))

#	Reorganizing the dataframe so as to move Cholesterol,
#	Tri LDL and HDL, to the end of the dataframe. This 
#	provides the final format to split the data into test 
#	and training datasets

cols = list(df_ch)
cols.insert(len(cols), cols.pop(cols.index('Tri')))
cols.insert(len(cols), cols.pop(cols.index('LDL')))
cols.insert(len(cols), cols.pop(cols.index('HDL')))
df_ch = df_ch.ix[: , cols]




age_group = [18.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 100.0]
gender_group = ['M', 'F']




for state in state_sample_list:

	state_sample_list[ state ].loc[ : ,'HR'] = \
			pd.Series(np.zeros(state_population), index=range(state_population))

	state_sample_list[ state ].loc[ : ,'Avg_Sys'] = \
		pd.Series(np.zeros(state_population), index=range(state_population))

	state_sample_list[ state ].loc[ : ,'Avg_Dia'] = \
		pd.Series(np.zeros(state_population), index=range(state_population))

	state_sample_list[ state ].loc[ : ,'Tri'] = \
		pd.Series(np.zeros(state_population), index=range(state_population))

	state_sample_list[ state ].loc[ : ,'LDL'] = \
		pd.Series(np.zeros(state_population), index=range(state_population))

	state_sample_list[ state ].loc[ : ,'HDL'] = \
		pd.Series(np.zeros(state_population), index=range(state_population))




for age in range(len(age_group) - 1):
	for gender in range(len(gender_group)):

		print "Binning Health Statistics "
		print

		df_hr_filter = df_hr[ (df_hr['Age_years'] >= age_group[ age ]) & \
								(df_hr['Age_years'] < age_group[ age + 1 ]) & \
								(df_hr['Gender'] == gender_group[ gender ])]

		df_bp_filter = df_bp[ (df_bp['Age_years'] >= age_group[ age ]) & \
							(df_bp['Age_years'] < age_group[ age + 1 ]) & \
							(df_bp['Gender'] == gender_group[ gender ])]

		df_ch_filter = df_ch[ (df_ch['Age_years'] >= age_group[ age ]) & \
							(df_ch['Age_years'] < age_group[ age + 1 ]) & \
							(df_ch['Gender'] == gender_group[ gender ])]


#		print df_hr_filter
#		print "Age Range (HR): ", age_group[ age ], age_group[ age + 1 ]

#		print df_bp_filter
#		print "Age Range (BP): ", age_group[ age ], age_group[ age + 1  ]

#		print df_ch_filter
#		print "Age Range (CH): ", age_group[ age ], age_group[ age + 1 ]

		quantile_hr = []
		quantile_sys = []
		quantile_dia = []
		quantile_tri = []
		quantile_ldl = []
		quantile_hdl = []

		j = 0.0

		print "Generating Quantiles (5%)"
		print
		for i in range(21):
			j = float(i) / 20
			quantile_hr.append(df_hr_filter['HR'].quantile( j ))
			quantile_sys.append(df_bp_filter['Avg_Sys'].quantile( j ))
			quantile_dia.append(df_bp_filter['Avg_Dia'].quantile( j ))
			quantile_tri.append(df_ch_filter['Tri'].quantile( j ))
			quantile_ldl.append(df_ch_filter['LDL'].quantile( j ))
			quantile_hdl.append(df_ch_filter['HDL'].quantile( j ))

#		print "Quantile: HR: ", quantile_hr
#		print "Quantile: Sys:  ", quantile_sys
#		print "Quantile: Dia: ", quantile_dia
#		print "Quantile: Tri: ", quantile_tri
#		print "Quantile: LDL: ", quantile_ldl
#		print "Quantile: HDL", quantile_hdl


		for state in state_sample_list:

			print "Generating Health Statistics for state: ", state
			print "\t", "Age: ", age_group[ age ], "\t", "Gender: ", gender_group[ gender ] 
#			print "\n", state, "\n"


			state_sample_list[ state ].index = range(len(state_sample_list[ state ].index))
			state_population_index = state_sample_list[ state ].index
		
			for person in state_population_index:

#				print person
#				print state_sample_list[ state ]['Gender'][ person ], gender_group[gender]
#				print state_sample_list[ state ]['Age_years'][ person ], age_group[ age ]
#				print state_sample_list[ state ]['Age_years'][ person ], age_group[ age + 1 ]
#				print


				test = (state_sample_list[ state ]['Age_years'][ person ] >= age_group[ age ]) & \
						(state_sample_list[ state ]['Age_years'][ person ] < age_group[ age + 1 ]) & \
						(state_sample_list[ state ]['Gender'][ person ] == gender_group[ gender ])

#				print test

				if test == True:

#					print "Makes it"
#					print
#					print

					age_by_100 = state_sample_list[ state ]['Age_years'][ person ] / 100
					rnd_hr = 20 * rnd.random()


					rnd_sys = min(19.0 + rnd.random(), (20 * (rnd.random() + 0.3 * age_by_100)))
					rnd_dia = rnd_sys
#					rnd_dia = 20 * rnd.random()
					rnd_tri = 20 * rnd.random()
					rnd_ldl = 20 * rnd.random()
					rnd_hdl = 20 - rnd_tri
#					rnd_hdl = 20 * rnd.random()

					rnd_hr_f = floor(rnd_hr)
					rnd_sys_f = floor(rnd_sys)
					rnd_dia_f = floor(rnd_dia)
					rnd_tri_f = floor(rnd_tri)
					rnd_ldl_f = floor(rnd_ldl)
					rnd_hdl_f = floor(rnd_hdl)

					rnd_hr_diff = rnd_hr - rnd_hr_f
					rnd_sys_diff = rnd_sys - rnd_sys_f
					rnd_dia_diff = rnd_dia - rnd_dia_f
					rnd_tri_diff = rnd_tri - rnd_tri_f
					rnd_ldl_diff = rnd_ldl - rnd_ldl_f
					rnd_hdl_diff = rnd_hdl - rnd_hdl_f

					rnd_hr_i = int(rnd_hr_f)
					rnd_sys_i = int(rnd_sys_f)
					rnd_dia_i = int(rnd_dia_f)
					rnd_tri_i = int(rnd_tri_f)
					rnd_ldl_i = int(rnd_ldl_f)
					rnd_hdl_i = int(rnd_hdl_f)


					state_sample_list[ state ].loc[person, 'HR'] = quantile_hr[ rnd_hr_i ] + \
								((quantile_hr[ rnd_hr_i + 1 ] - quantile_hr[ rnd_hr_i]) \
								 * rnd_hr_diff)

					state_sample_list[ state ].loc[person, 'Avg_Sys'] = quantile_sys[ rnd_sys_i ] + \
								((quantile_sys[ rnd_sys_i + 1 ] - quantile_sys[ rnd_sys_i ]) \
								 * rnd_sys_diff)

					state_sample_list[ state ].loc[person, 'Avg_Dia'] = quantile_dia[ rnd_dia_i ] + \
								((quantile_dia[ rnd_dia_i + 1 ] - quantile_dia[ rnd_dia_i]) \
									* rnd_dia_diff)

					state_sample_list[ state ].loc[person, 'Tri'] = quantile_tri[ rnd_tri_i ] + \
								((quantile_tri[ rnd_tri_i + 1 ] - quantile_tri[ rnd_tri_i]) \
									* rnd_tri_diff)

					state_sample_list[ state ].loc[person, 'LDL'] = quantile_ldl[ rnd_ldl_i ] + \
								((quantile_ldl[ rnd_ldl_i + 1 ] - quantile_ldl[ rnd_ldl_i ]) \
									* rnd_ldl_diff)

					state_sample_list[ state ].loc[person, 'HDL'] = quantile_hdl[ rnd_hdl_i ] + \
								((quantile_hdl[ rnd_hdl_i + 1 ] - quantile_hdl[ rnd_hdl_i ])\
									* rnd_hdl_diff)		

				else:
					pass


for state in state_sample_list:
	state_sample_list[ state ].to_csv(state + '_SampleData.csv')

print "Fraction of Population (1 / x): ", FRACTION_POPULATION
print "State: ", state, "State_Population: ", len(state_sample_list[ state ].index)
print "---- %s seconds ----" % (time.time() - start_time)
					
