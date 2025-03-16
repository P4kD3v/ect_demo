#   App Name:   Endometrial Cancer Tool (Demo).
#   Author:     Xavier Llobet Navàs.
#   Content:    Constant variables for ECT (Demo).
#
# - This file contains all the global and unmutable variables
#   that can be reused in all the ECT (Demo). the fields of these
#   variables are:
#
#   - Load dataframe.
#   - Survival dataset columns names and its values.
#   - Survival method names translation dictionary.
#   - Clinical categories name translation dictionary.
#   - Plotly toolbar configuration.
#
# - Other modules used:
#   
#   - tcga_read_csv
#
# =====================================================================
# IMPORTS
# =====================================================================

import              pandas          as  pd
from    .  import   tcga_read_csv   as  tcga

# =====================================================================
# GLOBAL CONSTANTS VARIABLES
# =====================================================================

# DataFrames
SURVIVAL:               pd.DataFrame    = tcga.read_survival_file()

# About categories
CATEGORIES:             list[str]       = [ 'grade',
                                            'tumor_type',
                                            'mol_subtype',
                                            'stage',
                                            'bmi_status',
                                            'radiotherapy',
                                            'age_group']


GRADES_DICT:            dict            = { "G1":           "Grade 1", 
                                            "G2":           "Grade 2", 
                                            "G3":           "Grade 3"}

CAT_AND_SUBCAT:         dict            = { 'grade':        {'G1':'Grade-1','G2':'Grade-2','G3':'Grade-3'},
                                            'tumor_type':   {'Serous':'Serous','Endometrioid':'Endometrioid'},
                                            'mol_subtype':  {'CN-LOW':'CN-LOW','CN-HIGH':'CN-HIGH', 'MSI':'MSI','POLE':'POLE'},
                                            'radiotherapy': {'Yes':'Yes','No':'No'},
                                            'age_group':    {'31-40':'31-40','41-50':'41-50', '51-60':'51-60','61-70':'61-70','>70':'>70'},
                                            'stage':        {'Stage I':'Stage I','Stage II':'Stage II', 'Stage III':'Stage III','Stage IV':'Stage IV'},
                                            'bmi_status':   {'Healthy Weight':'Healthy Weight','Overweight':'Overweight','Obesity':'Obesity'}}

SURVIVAL_GROUPS:        dict            = { 'grade':        ["G1", "G2", "G3"],
                                            'tumor_type':   ["Serous", "Endometrioid"],
                                            'mol_subtype':  ["POLE", "MSI", "CN-LOW", "CN-HIGH"],
                                            'radiotherapy': ["Yes", "No"],
                                            'age_group':    ["31-40", "41-50", "51-60", "61-70", ">70"],
                                            'stage':        ["Stage I", "Stage II", "Stage III", "Stage IV"],
                                            'bmi_status':   ["Healthy Weight", "Overweight", "Obesity"]}

CATEGORIES_DICT:        dict            = { 'grade':        'Grade',
                                            'tumor_type':   'Histologic Type',
                                            'mol_subtype':  'Molecular Subtype',
                                            'radiotherapy': 'Radiation Therapy',
                                            'age_group':    'Age',
                                            'stage':        'Stage',
                                            'bmi_status':   'BMI'}

SURVIVAL_MODES:         dict            = { 'os':           'Overall Survival',
                                            'pfs':          'Progression-Free Survival'}


# Plotly plots toolbar configuration
TOOLBAR_CONFIG:         dict            = { 'toImageButtonOptions':  {  'format':   'svg', # one of png, svg, jpeg, webp
                                                                        'filename': 'custom_image',
                                                                        'height':   500,
                                                                        'width':    700,
                                                                        'scale':    1 # Multiply title/legend/axis/canvas sizes by this factor
                                                                    }}

# Plotly plots toolbar configuration
TOOLBAR_CONFIG_XL:      dict            = { 'toImageButtonOptions':  {  'format':   'svg', # one of png, svg, jpeg, webp
                                                                        'filename': 'custom_image',
                                                                        'height':   500,
                                                                        'width':    1800,
                                                                        'scale':    1 # Multiply title/legend/axis/canvas sizes by this factor
                                                                    }}

# Plotly plots toolbar configuration
TOOLBAR_CONFIG_L:       dict            = { 'toImageButtonOptions':  {  'format':   'svg', # one of png, svg, jpeg, webp
                                                                        'filename': 'custom_image',
                                                                        'height':   500,
                                                                        'width':    1050,
                                                                        'scale':    1 # Multiply title/legend/axis/canvas sizes by this factor
                                                                    }}

