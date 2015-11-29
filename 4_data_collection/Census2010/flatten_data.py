import csv, json, os, re

# Output Directory
output = './outputs/'
output_csv = 'census.csv'
# Crete the output folder if needed...
if not os.path.exists(output):
  os.makedirs(output)


# List of JSON files to extract the data from
files = [
  "american_indian_and_alaska_native_alone.json",
  "asian_alone.json",
  "black_or_african_american_alone.json",
  "hispanic_or_latino.json",
  "native_hawaiian_and_other_pacific_islander_alone.json",
  "some_other_race_alone.json",
  "two_or_more_races.json",
  "white_alone.json",
  "white_alone_not_hispanic_or_latino.json"
  ]
total_pop_file = 'total_population_per_state.json'


# Get Ethinicity from the ID
def get_ethnicity(id=None):
  if not id:
    return None
  elif re.match('^..12A...$', id): # White Alone
    return 'White'
  elif re.match('^..12B...$', id): # Black ALone
    return 'Black'
  elif re.match('^..12C...$', id): # Native American
    return 'NavAm'
  elif re.match('^..12D...$', id): # Asian
    return 'Asian'
  elif re.match('^..12E...$', id): # Pacific Islanders
    return 'PacIs'
  elif re.match('^..12F...$', id): # Other
    return 'Other'
  elif re.match('^..12G...$', id): # Two or More Races
    return 'Mixed'
  elif re.match('^..12H...$', id): # Hispanic
    return 'Hisp'
  elif re.match('^..12I...$', id): # White Non Hispanic
    return 'WhiteNonHisp'
  else:
    return None



# Gets the gender from the ID
def get_gender(id=None):
  if not id:
    return None
  gender_number = int(id[5:])
  if (gender_number > 2) and (gender_number < 26): # Male
    return 'Male'
  elif (gender_number > 26) and (gender_number < 50): # Female
    return 'Female'
  else:
    return None



# Get the age range
def get_age(id=None):
  if not id:
    return None
  # Parse the number
  age_number = int(id[5:])
  # If it is on the women side of the range, normalize
  # by substracting '24' which will then send us into the 3 - 25 range.
  if age_number > 26:
    age_number -= 24 
  ages_definition = {
    3: '0-4',
    4: '5-9',
    5: '10-14',
    6: '15-17',
    7: '18-19',
    8: '20',
    9: '21',
    10: '22-24',
    11: '25-29', 
    12: '30-34',
    13: '35-39',
    14: '40-44',
    15: '45-49',
    16: '50-54',
    17: '55-59',
    18: '60-61',
    19: '62-64',
    20: '65-66',
    21: '67-69',
    22: '70-74',
    23: '75-79',
    24: '80-84',
    25: '85-100',
  }
  return ages_definition.get(age_number, None)



# Get state from number
def get_state(number=None):
  if not number:
    return None
  # Parse the number
  try:
    state_number = int(number)
  except:
    return None
  states_definition = {
    1: 'AL',
    2: 'AK',
    4: 'AZ',
    5: 'AR',
    6: 'CA',
    8: 'CO',
    9: 'CT',
    10: 'DE',
    11: 'DC',
    12: 'FL',
    13: 'GA',
    15: 'HI',
    16: 'ID',
    17: 'IL',
    18: 'IN', 
    19: 'IA',
    20: 'KS',
    21: 'KY',
    22: 'LA',
    23: 'ME',
    24: 'MD',
    25: 'MA', 
    26: 'MI',
    27: 'MN',
    28: 'MS',
    29: 'MO',
    30: 'MT',
    31: 'NE',
    32: 'NV',
    33: 'NH',
    34: 'NJ',
    35: 'NM',
    36: 'NY',
    37: 'NC',
    38: 'ND',
    39: 'OH',
    40: 'OK',
    41: 'OR',
    42: 'PA',
    44: 'RI',
    45: 'SC',
    46: 'SD',
    47: 'TN',
    48: 'TX',
    49: 'UT',
    50: 'VT',
    51: 'VA',
    53: 'WA',
    54: 'WV', 
    55: 'WI',
    56: 'WY',
    72: 'PR'
  }
  return states_definition.get(state_number, None)



# First read the total population file:
totals_map = dict()
with open(total_pop_file, 'rb') as totals:
  totals_list = json.load(totals)
  for item in totals_list[1:]:
    totals_map[get_state(item[1])] = int(item[0])
  print "Parsed total populations per state."



# Read all other json files and write them to csv
with open(output + output_csv, 'wb') as out: # Open the output csv
  # Open dictionary writer and add the header labels
  fieldnames = ['state', 'state population', 'ethnicity', 'gender', 'age group', 'group population']
  writer = csv.DictWriter(out, fieldnames=fieldnames)
  writer.writeheader()
  
  # Go through each JSON file and read into a JSON variable
  for file_name in files:
    with open(file_name, 'rb') as json_file: # Open file in read+binary format
      temp_json = json.load(json_file) # load file into json variable
      index = 0 # keep track of the index/column used in the for loop below

      # For each column we will write a row in the csv file, 
      # except for the totals, we don't want them
      for column in temp_json[0][:-2]:
        # If gender is not found, we assume it is a totals column and ignore it
        if get_gender(column) is None:
          index+=1 # increase the index/column pointer
          continue

        # create template row, we'll fill it below
        row_to_write = {
        'state': None,
        'state population': None,
        'ethnicity': get_ethnicity(column),
        'gender': get_gender(column),
        'age group': get_age(column),
        'group population': None
        }

        # We go through all other entries in the json file and get the value
        # we use the index/column number to make sure we are getting the correct value
        for item in temp_json[1:]:
          row_to_write['state'] = get_state(item[-1]) # the state is always the last column
          row_to_write['state population'] = totals_map.get(row_to_write['state']) # we get the state population from the totals_map
          row_to_write['group population'] = int(item[index])
          writer.writerow(row_to_write) # write the row
        index+=1 # increase the index/column pointer
    print "Read " + file_name + "."

print 'Done.'