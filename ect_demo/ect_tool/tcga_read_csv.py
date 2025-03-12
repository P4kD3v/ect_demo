#   App Name:   Endometrial Cancer Tool v5.
#   Author:     Xavier Llobet Navàs.
#   Content:    Dataset reading.

# IMPORTS
# =====================================================================

from    pathlib import  Path
import  pandas  as      pd
import  os

# Global variables
# ---------------------------------------------------------------------

# Get current directory:
cwd:            str     = os.getcwd()
print('CWD:', cwd)

dataset_path:   str     =  cwd.replace("DLN5", "Datasets")

# Constant variable for the dataset path
CSV_FILES_PATH: Path    = Path(dataset_path)


# FUNCTIONS
# =====================================================================

# Read 'survival.csv' file and convert to pandas DataFrame:
# ---------------------------------------------------------------------

def read_survival_file() -> pd.DataFrame:
    '''
    Create a pandas DataFrame for 'survival' CSV file.

    ## Return:
        - df (pd.Dataframe): created dataframe.
    '''

    filepath:   Path            = Path(CSV_FILES_PATH/"survival.csv")
    df:         pd.DataFrame    = pd.read_csv(filepath, sep=",")
    
    return df