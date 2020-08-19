import argparse

import pandas as pd


class PlantAssay():
    '''Dallaglio Plant Assay Extractor
    -------------------------------
    Collect the daily data from each sheet in the Dallagio Plant Assays excel report,
    and return the full month's data in table format (csv)
    
    excel_filename (str): path to plant assay excel file
    assay_format (str): `Old` or `New`'''
    
    def __init__(self, excel_filename, assay_format='Old'):
        
        self.dict_sheets_dfs = pd.read_excel(excel_filename, sheet_name=None)
        self.assay_sheet_names = list(dict_sheets_dfs.keys())
        self.assay_format = assay_format
        
    def get_report_details(self, df):
        
        site_name = df.iloc[1].index[0]
        
        
        report_details = {'report_number': df.iloc[1][9],
                          'sample_date': pd.to_datetime(df.iloc[1][2]).date(),
                          'date_received': pd.to_datetime(df.iloc[2][2]).date(),
                          'assay_date': pd.to_datetime(df.iloc[3][2]).date()
                         }
        
        return report_details
    
    def get_crushing_milling_grade_summary(self, df_left_section):
        df_crs_mil_grades = df_left_section.loc[5:6].dropna(axis=1, how='all')

        crushing_milling_grade_summary = {'crusher_feed_DS': df_crs_mil_grades.loc[5].values[1:][0],
                                          'crusher_feed_NS': df_crs_mil_grades.loc[5].values[1:][1],
                                          'mill_feed_DS': df_crs_mil_grades.loc[6].values[1:][0],
                                          'mill_feed_NS': df_crs_mil_grades.loc[6].values[1:][1]
                                         }
        
        return crushing_milling_grade_summary
    
    def get_solids_gpt(self, df_left_section):
        df_solids = df_left_section.loc[13-2:27-2].dropna(axis=1, how='all')
        df_solids.columns = ['SOLIDS','DS','NS']
        df_solids = df_solids.drop(index=11, axis=0)
        df_solids['SOLIDS'] = [name .replace('"', 'LEACH TANK').replace(' ', '') for name in df_solids.SOLIDS.values]
        df_solids.set_index('SOLIDS', inplace=True)

        df_solids_ds = df_solids[['DS']]
        df_solids_ds.index = [name + '_DS' for name in df_solids_ds.index]
        df_solids_ds

        df_solids_ns = df_solids[['NS']]
        df_solids_ns.index = [name + '_NS' for name in df_solids_ns.index]
        df_solids_ns
        
        return df_solids_ds['DS'], df_solids_ns['NS']
    
    def get_solutions_ppm(self, df_left_section):
        df_solution = df_left_section.loc[30-2:44-2].dropna(axis=1, how='all')
        df_solution.columns = ['SOLUTIONS','DS','NS']
        df_solution = df_solution.drop(index=11, axis=0)
        df_solution['SOLUTIONS'] = [name .replace('"', 'LEACH TANK').replace(' ', '') for name in df_solution.SOLUTIONS.values]
        df_solution.set_index('SOLUTIONS', inplace=True)

        df_solution_ds = df_solution[['DS']]
        df_solution_ds.index = [name + '_DS' for name in df_solution_ds.index]
        df_solution_ds

        df_solution_ns = df_solution[['NS']]
        df_solution_ns.index = [name + '_NS' for name in df_solution_ns.index]
        df_solution_ns
        
        return df_solution_ds['DS'], df_solution_ns['NS']
    
    def get_elution_related_values(self, df_left_section):
        pass
        

parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='csv help')
args = parser.parse_args()