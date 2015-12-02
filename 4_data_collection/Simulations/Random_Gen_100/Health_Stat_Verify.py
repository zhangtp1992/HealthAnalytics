import pandas as pd



state_abb = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', \
			'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', \
			'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', \
			'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', \
			'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', \
			'WI', 'WY']

overweight = []
hypertension = []
cholesterol = []



repeat = '_SampleData.csv'


for state in range(len(state_abb)):

	print "Checking health for ", state_abb[ state ]
	cholesterol_count = 0
	overweight_count = 0
	hypertension_count = 0

	fraction_sample_overweight = 0.0
	fraction_sample_hypertension = 0.0

	filename = state_abb[ state ] + repeat

	df = pd.read_csv(filename)
	df.pop('Unnamed: 0')

	sample_population = len(df.index)

	overweight_count = len(df[ df['BMI'] >= 25.0 ].index) 
	fraction_sample_overweight = float(overweight_count) / float(sample_population)
	overweight.append(fraction_sample_overweight)

	hypertension_count = len(df[ (df['Avg_Sys'] >= 140.0) | (df['Avg_Dia'] >= 90)].index)
	fraction_sample_hypertension = float(hypertension_count) / float(sample_population)
	hypertension.append(fraction_sample_hypertension)


	for person in range(sample_population):

		ch_tmp = 0.0
		ch_tmp = df['LDL'][ person ] + df['HDL'][ person ] + (df['Tri'][ person ] / 5)

		if ch_tmp >= 240.0:
			cholesterol_count += 1

		else:
			pass

	cholesterol.append(float(cholesterol_count) / float(sample_population))

df_out = pd.DataFrame(state_abb, index=range(len(state_abb)))
df_out['Overweight'] = pd.Series(overweight, index=range(len(overweight)))
df_out['Hypertension'] = pd.Series(hypertension, index=range(len(hypertension)))
df_out['High_Cholesterol'] = pd.Series(cholesterol, index=range(len(cholesterol)))

df_out.to_csv('State_Health_Summary.csv')