import pandas as pd
import os


"""
Notes on observations and generalizations made for script: 
	
	Ideally, this code would take any xls file with smaller subsets of graphs and put them in the form necessary for 
	census_cleaner.py to execute, but generalization means many many corner cases, and this was built specifically for 
	REDATAM output data. There are patterns in the output of REDATAM data. 

	Each township level file has a column 0 with only descriptive information about the file as a whole (Database, 
	crosstabs, geographic area) and then the pattern starts with the name of the township and the crosstabulated 
	table, repeat. Because of this, I do take some liberties of indexing directly especially in the get_first_rows function.
	I will try my best to impose assertions.
====================================================================================================================================

Procedural pipeline

township_xls_filename --> messy dataframe --> clean columns --> clean_df --> township_csv
load_df					  load_df			  retreive_col_names			 create_new_csv
						  get_first_rows	  rename_columns
						  fix_string_values





"""



def load_df(fname):
	"""
	Load xls output file given by REDATAM and ouput a new data frame
	without blank lines and no first columns but still messy

	input -- 
		fname: str - filepath to xls file
	output -- 
		df: pd.DataFrame - pandas data frame (still messy)
	"""
	FIRST_COL = 0
	df = pd.read_excel(fname)
	df = df.drop(df.columns[FIRST_COL], axis=1)
	df = df.dropna(axis=0, how='all')
	return df

def get_first_rows(df):
	'''
	new column names are made as combination of cross tabs then 
	the cross tabs value e.g. car/truck/van then yes or no. This function
	isolates these values for later extraction.

	input --
		df: pd.DataFrame - messy dataframe from xls loaded file
	output -- 
		df: pd.DataFrame - two rows from df that hold all information on column names
	'''
	TAB_ROW_IX = 1
	TAB_CHOICE_IX = 3

	df = df.reset_index(drop=True)[TAB_ROW_IX: TAB_CHOICE_IX]
	return df


def retreive_col_names(col_df):
	"""
	given the column data frame, create the new set of column names 
	input -- 
		col_df: pd.DataFrame - column names df of length 2
	output -- 
		col_list: List<str> -- column list of length len(col_df.columns)
	"""
	col_1_name = col_df.iloc[0,0]
	new_cols = [fix_string_values(col_1_name)]
	col_base = col_df.iloc[0,1]
	col_suffix = col_df.iloc[1,1:].astype(str)
	return combine_col_names(col_base, col_suffix, new_cols)
    
def fix_string_values(col_string):
	"""
	simple replacement function for backslashes and spaces
	"""
	UNDERSCORE = '_'
	SLASH = '/'
	SPACE = ' '
	col_string = col_string.replace(SLASH, UNDERSCORE)
	col_string = col_string.replace(SPACE, UNDERSCORE)
	return col_string

def combine_col_names(col_base, col_suffixes, col_list):
	'''
	input --
		col_base: string - base name or prefix of columns
		col_suffixes: List<str> - suffix names for columsn
		col_list: List<str> -- current list of columns 
				(comes with 1 column already)
	ouput -- 
		col_list: List<str> -- updated column list of length len(col_suffixes) + 1

	'''
	for suffix in col_suffixes:
		new_val = fix_string_values(col_base) + '_' + fix_string_values(suffix)
		col_list.append(new_val)
	return col_list


def rename_columns(df_full, col_names):
	'''
	update names of columns of original dataframs
	input -- 
		df_full: pd.DataFrame - dataframe of all townships with old column names
	output -- 
		col_names: pd.DataFrame - dataframe with updated column names
	'''
	current_cols = df_full.columns
	col_df = {current_cols[i]:col_names[i] for i in range(len(col_names))}
	return df_full.rename(columns=col_df)
    

def generate_clean_dataframe(fname):
	'''
	create a dataframe for Lu Min's script from filename to clean DataFrame hence 
	I fill nan values with '*' since he requested it. 
	input -- 
		fname: string - filepath to xls file from REDATAM
	ouput -- 
		df: pd.DataFrame - data representing the dataframe
	'''
	df = load_df(fname)
	col_names = retreive_col_names(get_first_rows(df))
	df = rename_columns(df, col_names)
	return df.fillna('*')


def create_new_csv(xls_dir, new_dir):
	'''
	iterative function that calls the generate_clean_dataframe function and stores its result 
	in the same file name with csv files. 
	'''
	try:
	    for fname in os.listdir(xls_dir):
	        new_filename = os.path.splitext(fname)[0] + '.csv'
	        new_path = os.path.join(new_dir, new_filename)
	        if new_filename in os.listdir(new_dir):
	            print('skipping the creation of:', new_filename)
	            continue
	    
	        path_name = os.path.join(xls_dir,fname)
	        new_df = generate_clean_dataframe(path_name)
	        print('generated new df for:', path_name)
	        new_df.to_csv(new_path, index=False)

	except Exception as e:
	    print('*****************************')
	    print(fname)
	    print(e)
	    print('*****************************')

	return True



