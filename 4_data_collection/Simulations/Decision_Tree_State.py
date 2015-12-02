import pandas as pd
import numpy as np
import csv
import random
import json

import time


start_time = time.time()

class Node():

#	This class defines the basic structure of the node
#	The node contains particular attributes, the subset
#	of the DataFrame that satisfy those particular
#	attributes, and an array of possible child nodes
	
	def __init__(self):

		self.node_attributes = {

			'Gender'		: None 	,
			'Age_years'		: None	,
			'Weight'		: None	,
			'Height'		: None	,
			'Waist'			: None	,
			'Ethnicity'		: None
#			'Vig_YN'		: None 	,
#			'Vig_DW'		: None 	,
#			'Vig_MD'		: None	,
#			'Mod_YN'		: None 	,
#			'Mod_DW'		: None 	,
#			'Mod_MD'		: None

		}

		self.node_filter = {

			'Filter'		: None,
			'Value'			: None,
			'Total_Entries'	: None,
			'Node_Entries'	: None

		}

		self.children = []
		self.range = []

		# self.dataframe = None


	def set_attribute(self, key, value):

#	This function is used to assign values to attributes
#	which are already in the node_attribute dictionary.

		if key in self.node_attributes:

			# print "Approved assignment of key to valid value."
			self.node_attributes[ key ] = value

		else:
			pass
			# print "Adding attribute to list which is not allowed!!!"


	def print_attributes(self):

#	This function is used to print the attributes assigned
#	to the node_attributes dictionary

		print "Printing Attributes of the Nodes"

		for key in self.node_filter:
			print
			print key, self.node_filter[ key ]


##########################################################

class RegressionTree():

#	This class defines a Tree structure composed of nodes of
#	the Node Class described above. The main

	def __init__(self, dataframe):
		self.root = Node()
		# self.root.dataframe = dataframe


	
	def modID3(self, node, dataframe, freeAttributes, bins, predictor):
		
		if len(freeAttributes) == 0:
		#	This case is for when there are no more attributes that can be
		#	used to classify the dataset.
			pass
		
		elif len(dataframe['SEQN']) <= 20:
			pass
			
		else:

		#	This case is for when there exists at least one attribute that
		#	can be used to classify the dataset

		#	minRange is initialized to be the range of predictor of the
		#	current DataFrame. It will be compared to subsets of the 
		#	Dataframe classified by the attributes to see if an even smaller
		#	prediction range can be found.

		#	filterAttribute is the name of the attribute that minimizes the
		#	average of the ranges of the predictor the most
			mean = dataframe[predictor].mean()
			std = dataframe[predictor].std()
			minRange = (mean + std) - (mean - std)
#			minRange = dataframe[predictor].max() - dataframe[predictor].min()
			filterAttribute = None

		#	For each attribute that has not yet been used to filter the data,
		#	check to see if the average range of the subsetted data is smaller
		#	than the range of the original data (which should be true, this
		#	decision criteria is subject to change)

		#	Currently the algorithm take the average each range from each subset
		#	of data. While particle filter distributes the individal bins in
		#	this is only applied only to attributes that take on a range of
		#	values. We compensate for this by weighing the range of the bin
		#	by the number of elements in this bin and then dividing the sum of
		#	the ranges by the total number of elements in the subset of data

			for attribute in freeAttributes:
				tmpRange = 0

		#	This algorithm makes the distinction between whether any bin of the
		#	attribute has length 1 or lenght 2. Length 1 implies that the attribute
		#	takes on discrete value. Length 2 imples that the attribute can take
		#	a range of values.

				if len(bins[attribute][ 0 ]) == 1:

					for choice in bins[attribute]:

						tmpdf = dataframe[dataframe[attribute] == choice[ 0 ]]
#						tmpRange += (tmpdf[predictor].max() - tmpdf[predictor].min()) \
#										* tmpdf["SEQN"].count()

						tmpRange += (2 * tmpdf[predictor].std()) / tmpdf["SEQN"].count()
					tmpRange /= len(bins[attribute])
					tmpRange /= dataframe["SEQN"].count()

				else:
					for choice in bins[attribute]:

						tmpdf = dataframe[(dataframe[attribute] >= choice[ 0 ]) & \
									(dataframe[attribute] <= choice[ 1 ])]
#						tmpRange += (tmpdf[predictor].max() - tmpdf[predictor].min()) \
#										* tmpdf["SEQN"].count()

						tmpRange += (2 * tmpdf[predictor].std()) / tmpdf["SEQN"].count()
#					tmpRange /= len(bins[attribute])
					tmpRange /= dataframe["SEQN"].count()

		#	If the range of the attribute is smaller than the smallest one found,
		#	then this attribute and range will be stored as the smallest.
		#	The smallest one found will be used as the filter

				if tmpRange <= minRange:
					minRange = tmpRange
					filterAttribute = attribute

			#print filterAttribute, minRange

		#	If no such attribute further filters the ranges down, then we will not
		#	split the data. The function ends

			if filterAttribute == None:
				pass

		#	If there is an attribute that further filters the ranges then we will
		#	create as many children as there are bins for the attribute

			else:

		#	First, we create a free attributes list from the current node by creating 
		#	a deep copy. Then we remove the attribute from that list. THis will be used
		#	in the recursion for the child node

				from copy import deepcopy
				childFreeAttributes = deepcopy(freeAttributes)
				childFreeAttributes.remove(filterAttribute)

				for i in range(len(bins[filterAttribute])):

		#	Here, we initiate a child node, set the child node attributes to that of
		#	the current node. Then set the filter attribute chosen to a bin of the
		#	attribute. Afterwards, append the node to the list of children of the
		#	current node

					tmpChild = Node()
					tmpChild.node_attributes = deepcopy(node.node_attributes)
					tmpChild.set_attribute(filterAttribute, bins[filterAttribute][ i ])
					node.children.append(tmpChild)

		#	Testing

					tmpChild.node_filter['Filter'] = filterAttribute
					tmpChild.node_filter['Value'] = bins[filterAttribute][ i ]
					tmpChild.node_filter['Total_Entries'] = dataframe['SEQN'].count()

		#	Depending on whether the filter takes on discrete or continuous values,
		#	query a subset of the data based on the criteria and store it

					if len(bins[filterAttribute][ 0 ]) == 1:
						dfChild = dataframe[dataframe[filterAttribute] \
									== bins[filterAttribute][ i ][ 0 ]]

					else:
						dfChild = dataframe[(dataframe[filterAttribute] \
									>= bins[filterAttribute][ i ][ 0 ]) \
									& (dataframe[filterAttribute]
									<= bins[filterAttribute][ i ][ 1 ])]
						
					tmpMean = dfChild[predictor].mean()
					tmpStd = dfChild[predictor].std()
					tmpChild.range = [tmpMean - tmpStd, tmpMean + tmpStd]

					tmpChild.node_filter['Node_Entries'] = dfChild['SEQN'].count()
		#	Recurse

					self.modID3(node.children[ i ], dfChild, childFreeAttributes, \
									bins, predictor)

	


	def print_Tree(self, node, tabcount = 0):
		
		print "\t" * tabcount, node.node_filter['Filter'], node.node_filter['Value'], \
				node.node_filter['Node_Entries']

		if len(node.children) == 0:
			pass

		else:
			for child in node.children:
				self.print_Tree(child, tabcount + 1)


	def treeToJson(self, node):

		jNode = {}

		jNode['key'] = node.node_filter['Filter']
		jNode['value'] = node.node_filter['Value']
		jNode['children'] = []

		if len(node.range) >  0:
			jNode['Min'] = node.range[ 0 ]
			jNode['Max'] = node.range[ 1 ]

		if len(node.children) > 0:
			for i in range(len(node.children)):
				tmpjNode = self.treeToJson(node.children[ i ])
				if tmpjNode != None:
					jNode['children'].append(tmpjNode)
			
		return jNode


def printJson(jNode, tabcount = 0):
	
	if len(jNode['children']) == 0:
		print "\t" * tabcount, 'Filter', jNode['key']
		print "\t" * tabcount, 'Value', jNode['value']
		print "\t" * tabcount, 'Children', jNode['children']

	else:
		for key in jNode:
			print "\t" * tabcount, 'Filter', jNode['key']
			print "\t" * tabcount, 'Value', jNode['value']
			print "\t" * tabcount, 'Children'
			printJson(jNode['children'] , tabcount + 1)


##########################################################

def particle_filter(dataframe, attribute, bins=10):


#	Given a DataFrame, it will return bins of particular sizes
#	such that any entry has equal probability of belonging to
#	those bins. The function takes a entries of an attribute
#	and returns a list of values that define the range of the
#	bins. The function also return the dataframe with altered
#	values by pass-by-reference
#	
#	The number of bins is default set to 10
#
#	The list of bins is calculated first by sorting the dataframe
#	based on the attribute passed. Then we read the value of the
#	attribute column of the dataframe and store it as the upper
#	and lower bounds of the particular bins. 

	attribute_ranges = []
	temp_rows = dataframe.index
	num_entries = len(dataframe.index)
	num_entries_per_bin = int(num_entries / 10)

#	Before calculating the bins, we add a random number x in
#	[0.0, 1.0) to introduce noise. This is so that the lower
#	bound of one bin is not equal to the upper bound of another
#	bin. This ensures that any test data falls into one unique
#	bin always. However, we do not do this for fields where the
#	entries are already 0. This is so that we do not set nonzero
#	minutes of exercise to a partcipant who does ont exercise

#	for j in range(len(dataframe.index)):
#		if dataframe.loc[ j , attribute ] != 0:
#			dataframe.loc[ j , attribute ] += random.random()

	dataframe = dataframe.sort(columns=attribute)
	dataframe.index = range(len(dataframe.index))

#	print dataframe	
#	print num_entries
#	print num_entries_per_bin

#	Creating the bins by reading the values at regular intervals of
#	num_entries_per_bin width. The last bin may have fewer elemens
#	than the other bins, but not by much since the current dataset
#	has >5000 elements

	i = 0

	while i < num_entries:
		if i + num_entries_per_bin < num_entries:
			attribute_ranges.append([ dataframe.loc[i , attribute ], \
				dataframe.loc[ i + num_entries_per_bin , attribute ]])

		else:
			attribute_ranges.append([dataframe.loc[i , attribute], \
				dataframe.loc[num_entries - 1 , attribute]])

		i = i + 1 + num_entries_per_bin


	k = 0

	while attribute_ranges[ k ][ 1 ] - attribute_ranges [ k ][ 0 ] < 1:
		k = k + 1

	attribute_ranges = attribute_ranges[ k: ]
	bins = len(attribute_ranges)

#	The lower bound of the first bin is always set to 0 to represent
#	unbounded below. Similarly, the upper bound of the last bin is always
#	set to 1000 to represent unbounded above. If, however, the attribute
#	is Vig_MD or Mod_MD, we set the minimum bound to be 10, as this any
#	participant who partakes in Vigorous or Moderate exercise does so
#	for at least 10 min per day, by experimental design. This is to avoid
#	confusion that it is possible for a minimum bound of 0 minutes of
#	exercise per day

#	if attribute == "Vig_MD" or attribute == "Mod_MD":
#		attribute_ranges[ 0 ] = [ 0.0 ,  9.9 ]
#		attribute_ranges[ 1 ][ 0 ] = 10.0
#	else:
#		attribute_ranges[ 0 ][ 0 ] = 0.0

	attribute_ranges[ bins - 1 ][ 1 ] = 1000.0
	
	return attribute_ranges


##########################################################


def df_attribute_dict(dataframe):

#	This function creates the necessary dictionary that contain the proper
#	bins for classification in the regression tree. This function depends
#	on the function particle_filter to return ranges that are 'continuous',
#	which in this case means a high number of discretized values. This
#	function also adds ranges to the filter which are have a small set of
#	discrete values. The dictionary of discrete bins are returned to the
#	program

#	print "Creating particle filter for", dataframe.columns[ -1 ]

	attribute_filter = {	
			
			'Age_years'		: None	,
			'Weight'		: None	,
			'Height'		: None	,
			'Waist'			: None	
#			'Vig_MD'		: None	,
#			'Mod_MD'		: None	
		}

	for key in attribute_filter:

		#print "Calculating the Particle Filter for ", key
		attribute_filter[key] = particle_filter(dataframe, key)
		#print "Finished"

	attribute_filter['Gender'] = [['M'], ['F']]
	attribute_filter['Ethnicity'] = [['WhiteNonHisp'], ['Hisp'], ['Asian'], \
		['Other'], ['Black'], ['Mixed'], ['NavAm'], ['PacIs']]
#	attribute_filter['Vig_YN'] = [[ 0 ], [ 1 ]]
#	attribute_filter['Vig_DW'] = [ [ i ] for i in range(8) ]
#	attribute_filter['Mod_YN'] = [[ 0 ], [ 1 ]]
#	attribute_filter['Mod_DW'] = [ [ i ] for i in range(8) ]

	
#	print
#	for key in attribute_filter:
#		print key, attribute_filter[ key ]
#		print
	
	return attribute_filter


##########################################################

def splitData(dataframe, testPart=2):

	shuffledData = dataframe.reindex(np.random.permutation(dataframe.index))

	n = len(shuffledData.index)
	split = int(n / testPart)

	dfModel = shuffledData[ : split ]
	dfValidate = shuffledData[ split : ]

	dfModel.index = range(len(dfModel.index))
	dfValidate.index = range(len(dfValidate.index))

	return dfModel, dfValidate

##########################################################

def validateEntry(testEntry, dataModel, node, predictor):

	if len(node.children) == 0:
#		print testEntry
#		print testEntry[predictor]
#		print
#		print dataModel
#		print dataModel[predictor]
#		print dataModel[predictor].min()

#		if (testEntry[predictor] >= dataModel[predictor].min()) & \
#			(testEntry[predictor] <= dataModel[predictor].max()):
		mean = dataModel[predictor].mean()
		std = dataModel[predictor].std()
		if ((testEntry[predictor] >= (mean - std)) & \
				(testEntry[predictor] <= (mean + std))):

#			print testEntry[predictor], "Correct"
#			print "\t", "Min: ", dataModel[predictor].min(), \
#					 "Max: ", dataModel[predictor].max(), \
#					 "Avg: ", dataModel[predictor].mean(), \
#					 "Number of Samples", len(dataModel.index)
			return 1

		else:
#			print testEntry[predictor], "Incorrect"
#			print "\t", "Min: ", dataModel[predictor].min(), \
#					 "Max: ", dataModel[predictor].max(), \
#					 "Avg: ", dataModel[predictor].mean(), \
#					 "Number of Samples", len(dataModel.index)
			return 0

	else:

		filterAttribute = node.children[ 0 ].node_filter['Filter']
		filterValue = testEntry.ix[filterAttribute]
		childKey = 0

		if len(node.children[ 0 ].node_filter['Value']) == 1:
			for j in range (len(node.children)):
				if (filterAttribute == 'Gender') | (filterAttribute == 'Ethnicity'):
					if filterValue == node.children[ j ].node_filter['Value'][ 0 ]:
						childKey = j
				else:
					if np.float64(filterValue) == node.children[ j ].node_filter['Value'][ 0 ]:
						childKey = j

			filterDF = dataModel[dataModel[filterAttribute] == filterValue]

			return validateEntry(testEntry, filterDF, node.children[childKey], predictor)

		else:
			for i in range(len(node.children)):

				if (np.float64(filterValue) >= node.children[ i ].node_filter['Value'][ 0 ]) \
					& (np.float64(filterValue) <= node.children[ i ].node_filter['Value'][ 1 ]):
					childKey = i

			filterDF = dataModel[(dataModel[filterAttribute] \
						>= node.children[childKey].node_filter['Value'][ 0 ]) \
						& (dataModel[filterAttribute] \
						<= node.children[childKey].node_filter['Value'][ 1 ])]

			return validateEntry(testEntry, filterDF, node.children[childKey], predictor)


##########################################################

def validateModel(testModel, dataModel, model, predictor):

	totalEntries = len(testModel.index)
	correctPredictions = 0

	percent_completion = [ i * totalEntries / 4 for i in range(1, 5) ]
	j = 0

	for i in range(totalEntries):
		if i >= percent_completion[ j ]:
			print '\t\tPrecent Completion: ', 25 * (j + 1)
			j += 1
		correctPredictions += validateEntry(testModel.iloc[ i ], \
								dataModel, model.root, predictor)

	return 100.0 * float(correctPredictions) / float(totalEntries)


##########################################################

def entryPredict(testEntry, dataModel, node, predictor):

	if len(node.children) == 0:

		mean = dataModel[predictor].mean()
		std = dataModel[predictor].std()
		return [mean - std , mean + std]
#		return [dataModel[predictor].min(), dataModel[predictor].max()]

	else:

		filterAttribute = node.children[ 0 ].node_filter['Filter']
		filterValue = testEntry[filterAttribute].values[ 0 ]
		childKey = 0

		if len(node.children[ 0 ].node_filter['Value']) == 1:
			for j in range (len(node.children)):
				if (filterAttribute == 'Gender') | (filterAttribute == 'Ethnicity'):
					if filterValue == node.children[ j ].node_filter['Value'][ 0 ]:
						childKey = j
				else:
					if np.float64(filterValue) == node.children[ j ].node_filter['Value'][ 0 ]:
						childKey = j

			filterDF = dataModel[dataModel[filterAttribute] == filterValue]

			return entryPredict(testEntry, filterDF, node.children[childKey], predictor)

		else:
			for i in range(len(node.children)):

				if (np.float64(filterValue) >= node.children[ i ].node_filter['Value'][ 0 ]) \
					& (np.float64(filterValue) <= node.children[ i ].node_filter['Value'][ 1 ]):
					childKey = i

			filterDF = dataModel[(dataModel[filterAttribute] \
						>= node.children[childKey].node_filter['Value'][ 0 ]) \
						& (dataModel[filterAttribute] \
						<= node.children[childKey].node_filter['Value'][ 1 ])]

			return entryPredict(testEntry, filterDF, node.children[childKey], predictor)

##########################################################


def displayStatistics(entry, ldlModel, hdlModel, triModel, sysModel, diaModel, hrModel, \
			ldlModelData, hdlModelData, triModelData, sysModelData, diaModelData, hrModelData):

	ldlPredict 	= entryPredict(entry, ldlModelData, ldlModel.root, "LDL")
	hdlPredict 	= entryPredict(entry, hdlModelData, hdlModel.root, "HDL")
	triPredict 	= entryPredict(entry, triModelData, triModel.root, "Tri")
	sysPredict	= entryPredict(entry, sysModelData, sysModel.root, "Avg_Sys")
	diaPredict 	= entryPredict(entry, diaModelData, diaModel.root, "Avg_Dia")
	hrPredict 	= entryPredict(entry, hrModelData, hrModel.root, "HR") 

	print
	print
	print "Stored Information"						, 4 * "\t", "User Information"
	print
	print
	print "Physical Characteristics"
	print
	print "Age (years): "							, 5 * "\t", entry['Age_years'].values[ 0 ]
	print "Gender (M/F): "							, 5 * "\t", entry['Gender'].values[ 0 ]
	print "Weight (kg): "							, 5 * "\t", entry['Weight'].values[ 0 ]
	print "Height (cm): "							, 5 * "\t", entry['Height'].values[ 0 ]
	print "Waist (cm): "							, 5 * "\t", entry['Waist'].values[ 0 ]
	print
#	print "Exercise Properties"
#	print
#	print "Participates in Vigorous Exercise?: "	, 2 * "\t", entry['Vig_YN'].values[ 0 ]
#	print "Vigorous Exercise, Days per Week: "		, 2 * "\t", entry['Vig_DW'].values[ 0 ]
#	print "Vigorous Exercise, Minutes per Day: "	, 2 * "\t", entry['Vig_MD'].values[ 0 ]
#	print "Participates in Moderate Exercise?: "	, 2 * "\t", entry['Mod_YN'].values[ 0 ]
#	print "Moderate Exercise, Days per Week: "		, 2 * "\t", entry['Mod_DW'].values[ 0 ]
#	print "Moderate Exercise, Minutes per Day: "	, 2 * "\t", entry['Mod_MD'].values[ 0 ]
#	print
	print
	print "Predictions"								, 5 * "\t", "Min", "\t", "Max"
	print
	print "Cholesterol"
	print "Low Density Lipoproteins: "		, 3 * "\t", ldlPredict[ 0 ], "\t", ldlPredict[ 1 ]
	print "High Desntiy Lipoproteins: "		, 3 * "\t", hdlPredict[ 0 ], "\t", hdlPredict[ 1 ]
	print "Triglycerides: "					, 4 * "\t", triPredict[ 0 ], "\t", triPredict[ 1 ]
	print 
	print "Blood Pressure"
	print "Systolic Pressure (mm/Hg): "		, 3 * "\t", sysPredict[ 0 ], "\t", sysPredict[ 1 ]
	print "Diastolic Pressure (mm/Hg): "	, 3 * "\t", diaPredict[ 0 ], "\t", diaPredict[ 1 ]
	print
	print "Heart Rate"
	print "Heart Rate (bpm): "				, 4 * "\t", hrPredict[ 0 ], "\t", hrPredict[ 1 ]	



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

############
#df = pd.read_csv('HealthData_10_16_2015.csv')
############

ldl_p = [['State', 'Accuracy']]
hdl_p = [['State', 'Accuracy']]
tri_p = [['State', 'Accuracy']]
sys_p = [['State', 'Accuracy']]
dia_p = [['State', 'Accuracy']]
hr_p = [['State', 'Accuracy']]

state_abb = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', \
			'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',  \
			'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', \
			'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', \
			'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

filename = "_SampleData.csv"
print state_abb

for state in range(len(state_abb)):

	print "Working on State: ", state_abb[ state ]
	df = pd.read_csv(state_abb[ state ] + filename)
	df.pop('Unnamed: 0')


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


#df = df[df.Gender.notnull() & df.Age_years.notnull() & df.Weight.notnull() \
#			& df.Height.notnull() & df.Waist.notnull()]

#df = df[df['Age_years'] > 17]

#mask_vig = df['Vig_YN'] == 2
#df.loc[mask_vig, 'Vig_YN'] = 0
#df.loc[mask_vig, 'Vig_DW'] = 0
#df.loc[mask_vig, 'Vig_MD'] = 0

#mask_mod = df['Mod_YN'] == 2
#df.loc[mask_mod, 'Mod_YN'] = 0
#df.loc[mask_mod, 'Mod_DW'] = 0
#df.loc[mask_mod, 'Mod_MD'] = 0


#	Creating a DataFrame from previously filtered entires
#	to remove any remaining entries that have any missing
#	heart rate information

#df_hr = df[df.HR.notnull()]
#df_hr.index = range(len(df_hr.index))

#	Removing columns in dataframe so that only attributes
#	and heart rate information remains

#df_hr = df_hr.drop(df_hr.columns[[ 9, 10, 11, 12, 13 ]], axis=1)

#	Reorganizing the dataframe so as to move heart rate (HR)
#	to the end of the dataframe. This provides the final
#	format to split the data into test and training datasets

#cols = list(df_hr)
#cols.insert(len(cols), cols.pop(cols.index('HR')))
#df_hr = df_hr.ix[: , cols]

#print df_hr

#	Creating a DataFrame from previously filtered entries
#	to remove any remaining entries that have any missing
#	blood pressure information
#	The new DataFrame also has reindexed row numbers

#df_bp = df[df.Avg_Sys.notnull() & df.Avg_Dia.notnull()]
#df_bp.index = range(len(df_bp.index))

#	Removing columns in dataframe so that only attributes
#	and blood pressure information remains

#df_bp = df_bp.drop(df_bp.columns[[ 8, 11, 12, 13 ]], axis=1)

#	Reorganizing the dataframe so as to move Blood Pressure,
#	Avg_Sys and Avg_Dia, to the end of the dataframe. This 
#	provides the final format to split the data into test 
#	and training datasets

#cols = list(df_bp)
#cols.insert(len(cols), cols.pop(cols.index('Avg_Sys')))
#cols.insert(len(cols), cols.pop(cols.index('Avg_Dia')))
#df_bp = df_bp.ix[: , cols]

#print df_bp

#	Creating a DataFrame from previously filtered entries
#	to remove any remaining entries that have any missing
#	cholesterol information

#df_ch = df[df.Tri.notnull() & df.LDL.notnull() & df.HDL.notnull()] 
#df_ch.index = range(len(df_ch.index))

#	Reorganizing the dataframe so as to move Cholesterol,
#	Tri LDL and HDL, to the end of the dataframe. This 
#	provides the final format to split the data into test 
#	and training datasets

#cols = list(df_ch)
#cols.insert(len(cols), cols.pop(cols.index('Tri')))
#cols.insert(len(cols), cols.pop(cols.index('LDL')))
#cols.insert(len(cols), cols.pop(cols.index('HDL')))
#df_ch = df_ch.ix[: , cols]

#print df_ch

# 	DL = Total cholesterol - HDL - (Triglycerides / 5)

#print df_ch.loc[0,"Tri"]

#print df_hr


#attribute_hr = df_attribute_dict(df_hr)


# 	The code block used below tests the whether the Node
#	class behaves as it should

# tmp_node = Node()

# print '#######'
# print tmp_node.print_attributes()
# print '#######'
# print tmp_node.print_children()
# print '#######'
# print tmp_node.children.append(Node())
# print '#######'
# print tmp_node.print_attributes()
# print '#######'
# print tmp_node.print_children()
# print '#######'
# print tmp_node.set_attribute("Key" , 1000)
# print tmp_node.print_attributes()
# print tmp_node.set_attribute("Mod_YN" , 1)
# print tmp_node.print_attributes()



#predictor = "Tri"
#print df_ch[predictor]

#print df_ch


	"""
	#for choice in bins:
	#	print
	#	print
	#	print choice, bins[choice]
	#	for elements in bins[choice]:
	#		print
	#		print elements, len(elements)
	"""
	testFree = ['Gender', 'Age_years', 'Weight', 'Height', 'Waist', 'Ethnicity'] #, \
	#				'Vig_YN', 'Vig_DW', 'Vig_MD', 'Mod_YN', 'Mod_DW', 'Mod_MD']




	#print "Run 3\n"
	print "\tBuilding LDL Model..."
#	print "\tSplitting Data..."
	ldlModelData , ldlValidateData = splitData(df)
#	print "\tDiscretizing continuous attributes..."
	ldlBins = df_attribute_dict(ldlModelData)
#	print "\tInstantiating Regression Tree..."
	modelLDL = RegressionTree(ldlModelData)
#	print "\tDeriving Regression Tree..."
	modelLDL.modID3(modelLDL.root, ldlModelData, testFree, ldlBins, "LDL")
	print "\tValidating Model..."
	validateLDL = validateModel(ldlModelData, ldlValidateData, modelLDL, "LDL")
#	print "LDL Model Accuracy (%): ", validateLDL
	ldl_p.append([state_abb[state], str(validateLDL)])
	#modelLDL.print_Tree(modelLDL.root)
	
	print "\tExporting Model to JSON..."
	ldljson = modelLDL.treeToJson(modelLDL.root)

	with open(state_abb[ state ] + '_LDL.json', 'w') as jsonfile:
		json.dump(ldljson, jsonfile)

	print "Done\n"


	print "\tBuilding HDL Model..."
#	print "\tSplitting Data..."
	hdlModelData, hdlValidateData = splitData(df)
#	print "\tDiscretizing continuous attributes..."
	hdlBins = df_attribute_dict(hdlModelData)
#	print "\tInstantiating Regression Tree..."
	modelHDL = RegressionTree(hdlModelData)
#	print "\tDeriving Regression Tree..."
	modelHDL.modID3(modelHDL.root, hdlModelData, testFree, hdlBins, "HDL")
	print "\tValidating Model..."
	validateHDL = validateModel(hdlModelData, hdlValidateData, modelHDL, "HDL")
#	print "HDL Model Accuracy (%): ", validateHDL
	hdl_p.append([state_abb[state], str(validateHDL)])
	#modelHDL.print_Tree(modelHDL.root)

	print "\tExporting Model to JSON..."
	hdljson = modelHDL.treeToJson(modelHDL.root)

	with open(state_abb[ state ] + '_HDL.json', 'w') as jsonfile:
		json.dump(hdljson, jsonfile)

#	print "Done\n"


	print "\tBuilding Tri Model..."
#	print "\tSplitting Data..."
	triModelData, triValidateData = splitData(df)
#	print "\tDiscretizing continuous attributes..."
	triBins = df_attribute_dict(triModelData)
#	print "\tInstantiating Regression Tree..."
	modelTri = RegressionTree(triModelData)
#	print "\tDeriving Regression Tree..."
	modelTri.modID3(modelTri.root, triModelData, testFree, triBins, "Tri")
	print "\tValidating Model..."
	validateTri = validateModel(triModelData, triValidateData, modelTri, "Tri")
#	print "Tri Model Accuracy (%): ", validateTri
	tri_p.append([state_abb[state], str(validateTri)])
	#modelTri.print_Tree(modelTri.root)

	print "\tExporting Model to JSON..."
	trijson = modelTri.treeToJson(modelTri.root)

	with open(state_abb[ state ] + '_Tri.json', 'w') as jsonfile:
		json.dump(trijson, jsonfile)

#	print "Done\n"


	print "\tBuilding Sys Model..."
#	print "\tSplitting Data..."
	sysModelData, sysValidateData = splitData(df)
#	print "\tDiscretizing continuous attributes..."
	sysBins = df_attribute_dict(sysModelData)
#	print "\tInstantiating Regression Tree..."
	modelSys = RegressionTree(sysModelData)
#	print "\tDeriving Regression Tree..."
	modelSys.modID3(modelSys.root, sysModelData, testFree, sysBins, "Avg_Sys")
	print "\tValidating Model..."
	validateSys = validateModel(sysModelData, sysValidateData, modelSys, "Avg_Sys")
#	print "Sys Model Accuracy (%): ", validateSys
	sys_p.append([state_abb[state], str(validateSys)])
	#modelSys.print_Tree(modelSys.root)

	print "\tExporting Model to JSON..."
	sysjson = modelSys.treeToJson(modelSys.root)

	with open(state_abb[ state ] + '_Sys.json', 'w') as jsonfile:
		json.dump(sysjson, jsonfile)

#	print "Done\n"


	print "\tBuilding Dia Model..."
#	print "\tSplitting Data..."
	diaModelData, diaValidateData = splitData(df)
#	print "\tDiscretizing continuous attributes..."
	diaBins = df_attribute_dict(diaModelData)
#	print "\tInstantiating Regression Tree..."
	modelDia = RegressionTree(diaModelData)
	modelDia.modID3(modelDia.root, diaModelData, testFree, diaBins, "Avg_Dia")
	print "\tValidating Model..."
	validateDia = validateModel(diaModelData, diaValidateData, modelDia, "Avg_Dia")
#	print "Dia Model Accuracy (%): ", validateDia
	dia_p.append([state_abb[state], str(validateDia)])
	#modelDia.print_Tree(modelDia.root)

	print "\tExporting Model to JSON..."
	diajson = modelDia.treeToJson(modelDia.root)

	with open(state_abb[ state ] + '_Dia.json', 'w') as jsonfile:
		json.dump(diajson, jsonfile)

#	print "Done\n"


	print "\tBuilding HR Model..."
#	print "\tSplitting Data..."
	hrModelData, hrValidateData = splitData(df)
#	print "\tDiscretizing continuous attributes..."
	hrBins = df_attribute_dict(hrModelData)
#	print "\tInstantiating Regression Tree..."
	modelHR = RegressionTree(hrModelData)
#	print "\tDeriving Regression Tree..."
	modelHR.modID3(modelHR.root, hrModelData, testFree, hrBins, "HR")
	print "\tValidating Model..."
	validateHR = validateModel(hrModelData, hrValidateData, modelHR, "HR")
#	print "HR  Model Accuracy (%): ", validateHR
	hr_p.append([state_abb[state], str(validateHR)])
	#modelHR.print_Tree(modelHR.root)
	print "Done\n"

	print "\tExporting Model to JSON..."
	hrjson = modelHR.treeToJson(modelHR.root)

	with open(state_abb[ state ] + '_HR.json', 'w') as jsonfile:
		json.dump(hrjson, jsonfile)

#	print "Done\n"


#	Ming = { 
		
#		'Age_years' 	: 23 	,
#		'Gender'		: 'M'	,
#		'Weight'		: 85.0	,
#		'Height'		: 12.8	,
#		'Waist'			: 86.4	,
#		'Ethnicity'		: 'Asian'
#		'Vig_YN'		: 1		,
#		'Vig_DW'		: 4		,
#		'Vig_MD'		: 30.0	,
#		'Mod_YN'		: 0		,
#		'Mod_DW'		: 0		,
#		'Mod_MD'		: 0.0	

#		}

#	Ming = pd.DataFrame(Ming, index=[0])

#	displayStatistics(Ming, modelLDL, modelHDL, modelTri, modelSys, modelDia, modelHR, \
#			ldlModelData, hdlModelData, triModelData, sysModelData, diaModelData, hrModelData)


with open('LDL_State_Corr_Accuracy_2.csv', 'w') as ldlcsv:
	a = csv.writer(ldlcsv, delimiter=',')
	a.writerows(ldl_p)

with open('HDL_State_Corr_Accuracy_2.csv', 'w') as hdlcsv:
	a = csv.writer(hdlcsv, delimiter=',')
	a.writerows(hdl_p)

with open('Tri_State_Corr_Accuracy_2.csv', 'w') as tricsv:
	a = csv.writer(tricsv, delimiter=',')
	a.writerows(tri_p)

with open('Sys_State_Corr_Accuracy_2.csv', 'w') as syscsv:
	a = csv.writer(syscsv, delimiter=',')
	a.writerows(sys_p)

with open('Dia_State_Corr_Accuracy_2.csv', 'w') as diacsv:
	a = csv.writer(diacsv, delimiter=',')
	a.writerows(dia_p)

with open('HR_State_Corr_Accuracy_2.csv', 'w') as hrcsv:
	a = csv.writer(hrcsv, delimiter=',')
	a.writerows(hr_p)


print("--- %s seconds ---" % (time.time() - start_time))
	#print "\n\n"

	#testjson = modelHeartRate.treeToJson(modelHeartRate.root)

	#modelCholesterol.print_Tree(modelCholesterol.root)

	#print
	#print dataValidate.iloc[0]
	#print
	

	
