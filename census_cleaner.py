import csv
import os

# Important global vars
xtab_loc = "files/township_csv"
output_dir = "out_files"
mimu_dict_loc = "files/mimu_translate.csv"

def main():
  # Read in a python dict for MIMU name translation
  mimu_dict = read_dict(mimu_dict_loc)
  
  # List out all the crosstabs we want
  xtab_list = os.listdir(xtab_loc)
  
  # Generate csv's for each kind of crosstab
  for xtab in xtab_list:

    # Don't look at hidden files beginning with '.'
    if (xtab[0] == '.'): continue
    
    # Make output directories for xtabs
    dir_name = xtab.split('.')[0]
    long_dir_name = "%s/%s" % (output_dir, dir_name)
    if (dir_name not in os.listdir(output_dir)):
      os.mkdir(long_dir_name)
    
    # Make CSVs!!
    print("Working on %s" % (dir_name))
    make_csv(xtab, long_dir_name, mimu_dict)

"""
Takes the MIMU name translation csv and
outputs a python dictionary
"""
def read_dict(trans_filename):
  trans_file = open(trans_filename, 'r')

  trans_reader = csv.reader(trans_file)
  next(trans_reader)
  
  mimu_dict = {}
  for line in trans_reader:
    tsp_dict = {}
    tsp_dict['tsp_code_mimu'] = line[2]
    tsp_dict['tsp_name_mimu'] = line[3]
    if (line[5] == 'Main'):
      tsp_dict['sub'] = False
    else:
      tsp_dict['sub'] = True
    
    mimu_dict[line[1]] = tsp_dict

  return mimu_dict

"""
Makes township CSVs
"""
def make_csv(filename, out_dir, mimu_dict):
  data_file = open("%s/%s" % (xtab_loc, filename), 'r')
  master_outfile = open(out_dir+"/"+filename, 'w')
  township_outfile = False 

  master_reader = csv.reader(data_file)
  header = next(master_reader)
  header += ['Township', 'MIMU_code']
  master_writer = csv.writer(master_outfile)
  master_writer.writerow(header)

  township = ""

  for row in master_reader:
    # Ignore empty rows
    if (row[0] == '*'):
      continue
    # We detected a new township table section
    elif (row[0][:4] == "AREA"):
      township = row[1]
      if (township not in mimu_dict.keys()):
        continue
      if ("/" in township):
        township = township.replace("/","-")
      # Create new township file
      township_outfile = open(out_dir+"/%s_%s.csv" % (filename.split('.')[0],township), 'w+')
      township_writer = csv.writer(township_outfile)
      township_writer.writerow(header)
    elif('*' in row): continue
    else:
      if (township not in mimu_dict.keys()): continue
      new_row = row + [township, mimu_dict[township]['tsp_code_mimu']]

      # write to a master file
      master_writer.writerow(new_row)

      # write to township-specific file
      township_writer.writerow(new_row)

main()
