import xport, csv, json, os
from datetime import datetime

# Output Directory
output = './outputs/'

# List of SAS files to export
files_SAS = [
  "CVX_C.XPT",
  "BMX.XPT",
  "BMX_B.XPT",
  "BMX_C.XPT",
  "BMX_D.XPT",
  "BMX_E.XPT",
  "BMX_F.XPT",
  "BMX_G.XPT",
  "BMX_H.XPT",
  "BPX.XPT",
  "BPX_B.XPT",
  "BPX_C.XPT",
  "BPX_D.XPT",
  "BPX_E.XPT",
  "BPX_F.XPT",
  "BPX_G.XPT",
  "BPX_H.XPT",
  "DEMO.XPT",
  "DEMO_B.XPT",
  "DEMO_C.XPT",
  "DEMO_D.XPT",
  "DEMO_E.XPT",
  "DEMO_F.XPT",
  "DEMO_G.XPT",
  "DEMO_H.XPT",
  "HDL_D.XPT",
  "HDL_E.XPT",
  "HDL_F.XPT",
  "HDL_G.XPT",
  "LAB13AM.XPT",
  "L13AM_B.XPT",
  "L13AM_C.XPT",
  "TRIGLY_D.XPT",
  "TRIGLY_E.XPT",
  "TRIGLY_F.XPT",
  "TRIGLY_G.XPT",
  "TCHOL_D.XPT",
  "TCHOL_E.XPT",
  "TCHOL_F.XPT",
  "TCHOL_G.XPT",
  "TCHOL_H.XPT",
  "LAB13.XPT",
  "L13_B.XPT",
  "L13_C.XPT",
  "L13_2_B.XPT"
  ]

  

# JSON serializer needed to dump dates into files
def json_serial(obj):
  """JSON serializer for objects not serializable by default json code"""
  if isinstance(obj, datetime):
    serial = obj.isoformat()
    return serial
  raise TypeError ("Type not serializable")


# Crete the output folder if needed...
if not os.path.exists(output):
  os.makedirs(output)

# Go through each SAS file and do work
for file_name in files_SAS:
  # Open SAS data file
  with xport.XportReader(file_name) as reader:
    # Writing the data legend.
    with open(output+ file_name + '_legend.json', 'wb') as legend:
      legend_txt = json.dumps(reader.fields, sort_keys=True, indent=2, separators=(',', ': '), default=json_serial)
      legend.write(legend_txt)
    # Writing data file info.
    with open(output+ file_name + '_file_info.json', 'wb') as info:
      info_txt = json.dumps(reader.file_info, sort_keys=True, indent=2, separators=(',', ': '), default=json_serial)
      info.write(info_txt)
    # Writing data file info.
    with open(output+ file_name + '_member_info.json', 'wb') as info:
      info_txt = json.dumps(reader.member_info, sort_keys=True, indent=2, separators=(',', ': '), default=json_serial)
      info.write(info_txt)
    # Writing data to CSV
    with open(output+ file_name + '.csv', 'wb') as out: # add .csv at the end
      # first, open dict writer and add the header labels
      writer = csv.DictWriter(out, fieldnames=[f['name'] for f in reader.fields])
      writer.writeheader()
      # read data, row by row
      for row in reader:
        writer.writerow(row)
    print "Finished " + file_name + "."
print 'Done.'