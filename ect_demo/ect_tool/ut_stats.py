#   App Name:   Endometrial Cancer Tool (Demo).
#   Author:     Xavier Llobet Navàs.
#   Content:    ECT (Demo) statistics.
#
# - This file contains a function for statistical analysis. The
#   function is:
#
#   - calculate_formatted_multi_logrank_p(): calculate and format 
#     multivariate logrank test pvalue.
#
# =====================================================================
# IMPORTS
# =====================================================================

import  pandas                  as      pd
from    lifelines.statistics    import  multivariate_logrank_test

# Caluclate multivariate logrank test pvalue.
# ---------------------------------------------------------------------
def calculate_formatted_multi_logrank_p(months: list|pd.Series,
                                        groups: list|pd.Series,
                                        status: list|pd.Series)->str:
    '''
    Calculate a logrank test p value for more than two populations.
    This test is a generalization of the logrank_test: it can deal 
    with n>2 populations:

    ## Parameters:
        - months (list|pd.Series): array of months.
        - groups (list|pd.Series): array of groups.
        - status (list|pd.Series): array of status.
        
    ## Return:
        - p_value (str): formatted pvalue.
    '''

    # Calculate StatisticalResult object with properties 'p_value', 
    # 'summary', 'test_statistic', 'print_summary':
    logrank                     = multivariate_logrank_test(months, 
                                                            groups, 
                                                            status)
    
    # Formatted pvalue.
    logrank_p_value:    str     = "{:e}".format(logrank.p_value)

    return logrank_p_value

