#   App Name:   Endometrial Cancer Tool (Demo).
#   Author:     Xavier Llobet Navàs.
#   Content:    Survival analysis helpers.
#
# - This file contains all the functions that ECT (Demo) will use
#   to do a survival analysis. Te functions are:
#
#   - km_category_survival_helper(): survival analysis by clinical category.
#
# - Other modules used are:
#
#   - plotly_survival_plots
#   - ut_constants
#
# =====================================================================
# IMPORTS
# =====================================================================

from    .           import  plotly_survival_plots    as  sp
from    .           import  ut_constants             as  cns
import  pandas      as      pd

# =====================================================================
# FUNCTIONS
# =====================================================================

# Survival and PF.Survival related to a clinical category
# ---------------------------------------------------------------------
def km_category_survival_helper(df:                  pd.DataFrame, 
                                mode:                str,
                                group_column_name:   str,
                                main_category:       str,
                                group_categories:    list[str])->dict:
    '''
    Handle survival and population bar plot generation for specific 
    clinical categories, save the plots into the database,
    and return yo the views.py a context dictionary prepared for the 
    template view.

    ## Parameters:
        - df (pd.Dataframe): The Dataframe to be filtered.
        - mode (str): Can be Overall (os) or Progression-Free Survival
        (pfs).
        - group_column_name (str): main category that contain the 
        group_categories.
        - main_category (str): main category name only for plot tile.
        - group_categories (list[str]): list of the categories included 
        in group_column_name.
        - html_key (str): string as key for the Django template blocks.

    ## Returns:
        - context (dict): Dictionary with the data to fill up the Django
        template.
    '''
    # Create title depending on the 'mode':
    if mode == 'os':
        survival_title:     str             = f"<b>EC Overall Survival</b><br><sup>by <b style='color: green;'>{main_category}</b></sup>"
    if mode =='pfs':
        survival_title:     str             = f"<b>EC Progression-Free Survival</b><br><sup>by <b style='color: green;'>{main_category}</b></sup>"    
    # Create survival plot, and table for population at risk by time:
    survival_plot, table_plot               = sp.plotly_survival(   df, 
                                                                    mode, 
                                                                    survival_title, 
                                                                    group_column_name, 
                                                                    group_categories)
    # Create histogram plot for all population:
    category_orders:        dict            = {group_column_name:group_categories}
    bar_plot:               str             = sp.create_counting_bar_plot(df, 
                                                                          group_column_name, 
                                                                          f"<b>EC Population</b><br><sup>by <b style='color: green;'>{main_category}</b>", 
                                                                          category_orders,
                                                                          main_category)    

    # Create context to return to the 'views.py':
    context:                dict            = { 'survival_plot':        survival_plot,
                                                'bar_plot':             bar_plot,
                                                'table_plot':           table_plot,
                                                'survival_mode':        mode,
                                                'survival_mode_title':  cns.SURVIVAL_MODES[mode],
                                                'category_title':       main_category,
                                                'subcategories':        group_categories}
    
    return context


