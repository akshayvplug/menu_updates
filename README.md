Menu Report Generator
Overview
The Menu Report Generator is a Python script that processes XML menu data files, compares them with existing database records, generates detailed reports on menu changes, and aggregates results into a summary Excel file. It supports fetching and analyzing menu data for different restaurant branches, creating concise reports in JSON format, and exporting results to Excel.

Requirements
install modules in requirements.txt and create a virtual environment

File Structure


generate_report.py: Main script for generating reports and comparing data.
get_xml.py: Module for retrieving XML menu files.
extract.py: Module for parsing XML files.
connection.py: Module for database connection setup.
output/: Directory where reports and SQL queries are saved.


Usage
Generate Reports:

Modify the rest_dict in the script to include the desired restaurant abbreviations and store IDs.
Run the script. It will:
Fetch menu data.
Compare new data with existing database records.
Generate detailed and concise JSON reports.
Save results as Excel files in the output/ directory.
Create SQL queries for updating the database.
Amalgamate Reports:

After generating individual reports, the script combines them into a single summary Excel file.
The amalgamate_excel_reports function merges data from all generated reports into combined_summary_report.xlsx and optionally deletes the individual files.
Functions
generate_report(rest_abbr, id_list): Generates detailed reports for given restaurant abbreviations and store IDs. Saves reports and SQL queries to the output/ directory.
amalgamate_excel_reports(output_folder='output'): Combines individual Excel reports into a single summary report. Deletes original files after amalgamation.
