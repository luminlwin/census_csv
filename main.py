import redatam_out_csv as redatam_out
import census_cleaner as c_cleaner

REDATAM_EXCEL_FPATH = 'files/redatam_output_xls/'
CSV_OUPUT_PATH = 'files/township_csv/'

def main(xls_dir=REDATAM_EXCEL_FPATH, csv_dir=CSV_OUPUT_PATH):
	redatam_out.create_new_csv(xls_dir, csv_dir)
	c_cleaner.main()
	return None

main()