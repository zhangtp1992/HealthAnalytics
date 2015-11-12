This script will extract data from SAS files (with .xpt extension) into multiple output files:
- <file>.csv : contains the raw data with a header row of the IDs for each column
- <file>_legend.json : a json file that contains descriptions for each row ID
- <file>_file_info.json : a json file that contains information about the SAS file (i.e. date created, etc.)
- <file>_member_info.json : a json file that contains mofe inromation about the SAS file (i.e. set-name, etc.)

Pre-requisites:
- Have python installed (2.7.*)
- Have 'pip' installed (How to: http://pip.readthedocs.org/en/stable/installing/)
- Have SAS files to export: (see the "Notes" below for the files we included. Look for files with the ".XPT" extension)
- Install the program's python requirements:
  - In the same directory of the project run: 
  pip install -r requirements.txt

How to use:
- Open the file: "export_sas_data.py"
- Modify the array "files_SAS" and remove/add items
  - Add an entry into the array for each SAS file.
  - An entry consists of the full name of the SAS file, case sensitive
  - If the data file is not in the same directory as the python file, the entry should then have the full path to the SAS file.
- Run the python script:
  python export_sas_data.py
- The script should print "Finished <file>." for each finished SAS data file and will print "Done." once finished. 
- You should now see the files mentioned at the begining of this document.


Notes:
- Python library used: https://github.com/jcushman/xport
- Data files used are from: 
  - http://wwwn.cdc.gov/Nchs/Nhanes/Search/DataPage.aspx?Component=Examination
  - http://wwwn.cdc.gov/Nchs/Nhanes/Search/DataPage.aspx?Component=Laboratory
  - 
- Data files included:
  - CVX_C.XPT:    2003-2004 Cardiovascular Fitness
  - BMX.XPT:      1999-2000 Body Measures
  - BMX_B.XPT:    2001-2002 Body Measures
  - BMX_C.XPT:    2003-2004 Body Measures
  - BMX_D.XPT:    2005-2006 Body Measures
  - BMX_E.XPT:    2007-2008 Body Measures
  - BMX_F.XPT:    2009-2010 Body Measures
  - BMX_G.XPT:    2011-2012 Body Measures
  - BMX_H.XPT:    2013-2014 Body Measures
  - BPX.XPT:      1999-2000 Blood Pressure
  - BPX_B.XPT:    2001-2002 Blood Pressure
  - BPX_C.XPT:    2003-2004 Blood Pressure
  - BPX_D.XPT:    2005-2006 Blood Pressure
  - BPX_E.XPT:    2007-2008 Blood Pressure
  - BPX_F.XPT:    2009-2010 Blood Pressure
  - BPX_G.XPT:    2011-2012 Blood Pressure
  - BPX_H.XPT:    2013-2014 Blood Pressure
  - DEMO.XPT:     1999-2000 Demographic Variables & Sample Weights
  - DEMO_B.XPT:   2001-2002 Demographic Variables & Sample Weights
  - DEMO_C.XPT:   2003-2004 Demographic Variables & Sample Weights
  - DEMO_D.XPT:   2005-2006 Demographic Variables & Sample Weights
  - DEMO_E.XPT:   2007-2008 Demographic Variables & Sample Weights
  - DEMO_F.XPT:   2009-2010 Demographic Variables & Sample Weights
  - DEMO_G.XPT:   2011-2012 Demographic Variables & Sample Weights
  - DEMO_H.XPT:   2013-2014 Demographic Variables & Sample Weights
  - HDL_D.XPT:    2005-2006 Cholesterol - HDL
  - HDL_E.XPT:    2007-2008 Cholesterol - HDL
  - HDL_F.XPT:    2009-2010 Cholesterol - HDL
  - HDL_G.XPT:    2011-2012 Cholesterol - HDL
  - LAB13AM.XPT:  1999-2000 Cholesterol - LDL & Triglycerides
  - L13AM_B.XPT:  2001-2002 Cholesterol - LDL & Triglycerides
  - L13AM_C.XPT:  2003-2004 Cholesterol - LDL & Triglycerides
  - TRIGLY_D.XPT: 2005-2006 Cholesterol - LDL & Triglycerides
  - TRIGLY_E.XPT: 2007-2008 Cholesterol - LDL & Triglycerides
  - TRIGLY_F.XPT: 2009-2010 Cholesterol - LDL & Triglycerides
  - TRIGLY_G.XPT: 2011-2012 Cholesterol - LDL & Triglycerides
  - TCHOL_D.XPT:  2005-2006 Cholesterol - Total
  - TCHOL_E.XPT:  2007-2008 Cholesterol - Total
  - TCHOL_F.XPT:  2009-2010 Cholesterol - Total
  - TCHOL_G.XPT:  2011-2012 Cholesterol - Total
  - TCHOL_H.XPT:  2013-2014 Cholesterol - Total
  - LAB13.XPT:    1999-2000 Cholesterol - Total & HDL
  - L13_B.XPT:    2001-2002 Cholesterol - Total & HDL
  - L13_C.XPT:    2003-2004 Cholesterol - Total & HDL
  - L13_2_B.XPT:  2001-2002 Cholesterol - Total, HDL, LDL & Triglycerides, Second Exam