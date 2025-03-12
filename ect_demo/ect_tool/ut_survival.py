#   App Name:   Endometrial Cancer Tool v5.
#   Author:     Xavier Llobet Navàs.
#   Content:    Survival analysis helpers.
#
# - This file contains all the functions that ECT v5 will use
#   to do a survival analysis. Te functions are:
#
#   - km_all_survival_helper(): survival analysis for all dataset entries.
#   - km_category_survival_helper(): survival analysis by clinical category.
#   - filter_survival_df_ids(): filter patient ids from survival 
#     dataframe.
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
from    lifelines   import  KaplanMeierFitter
import  pandas      as      pd

# =====================================================================
# FUNCTIONS
# =====================================================================

# O.Survival and PF.Survival for all dataset entries
# ---------------------------------------------------------------------
def km_all_survival_helper( df:   pd.DataFrame, 
                            mode: str)->dict:
    '''
    Handle survival, table of population at risk by time
    and population bar plot generation for all patients
    independently of their clinical data, save the plots
    into the database, and return yo the views.py a context
    dictionary prepared for the template view.

    ## Parameters:
        - df (pd.Dataframe): The Dataframe to be filtered.
        - mode (str): Can be Overall (os) or Progression-Free Survival
        (pfs).

    ## Returns:
        - context (dict): Dictionary with the data to fill up the Django
        template.
    '''

    upper_mode:             str                 = mode.upper()
    kmf_init:               KaplanMeierFitter   = KaplanMeierFitter(alpha = 0.05,
                                                                    label = 'KM Survival Curve')
    
    # Create title and fit KaplanMeierFitter depending on the 'mode':
    if mode == 'pfs':
        plot_title:         str                 = "<b>EC Progression-Free Survival</b><br><sup>All EC Entries</sup>"
        plot_cum_title:     str                 = "<b>EC Cumulative Density</b><br><sup>Progression-Free Survival - All EC Entries</sup>"
        kmf_fitted:         KaplanMeierFitter   = kmf_init.fit( df['pfs_months'], 
                                                                df['pfs_status'])    
    if mode == 'os':
        plot_title:         str                 = "<b>EC Overall Survival</b><br><sup>All EC Entries</sup>"
        plot_cum_title:     str                 = "<b>EC Cumulative Density</b><br><sup>Overall Survival - All EC Entries</sup>"
        kmf_fitted:         KaplanMeierFitter   = kmf_init.fit( df['os_months'], 
                                                                df['os_status'])      
    
    # Create survival plot, and table for population at risk by time:
    survival_plot_div, survival_table           = sp.plotly_survival_function(  kmf_fitted, 
                                                                                kmf_fitted.survival_function_.index,
                                                                                upper_mode,
                                                                                plot_title)
    
    # Create cumulative density plot:
    cum_dens_plot_div:      str                 = sp.plotly_cumulative_density( kmf_fitted, 
                                                                                kmf_fitted.survival_function_.index,
                                                                                upper_mode,
                                                                                plot_cum_title)
    
    # Create context to return to the 'views.py':
    context:                dict                = { 'survival':             survival_plot_div,
                                                    'cumulative_den_surv':  cum_dens_plot_div,
                                                    'survival_table':       survival_table,
                                                    'title':                'Overview Survival',
                                                    'survival_mode':        mode,
                                                    'survival_mode_title':  cns.SURVIVAL_MODES[mode],
                                                    'category_title':       'All entries',
                                                    'type':                 'all'}

    return context


# O.Survival and PF.Survival related to a clinical category
# ---------------------------------------------------------------------
def km_category_survival_helper(df:                  pd.DataFrame, 
                                mode:                str,
                                group_column_name:   str,
                                main_category:       str,
                                group_categories:    list[str],
                                html_key:            str = '')->dict:
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
                                                'title':                'Overview Survival',
                                                'survival_mode':        mode,
                                                'survival_mode_title':  cns.SURVIVAL_MODES[mode],
                                                'category_title':       cns.CATEGORIES_DICT[html_key],
                                                'subcategories':        cns.SURVIVAL_GROUPS[html_key],
                                                'type':                 html_key}
    
    return context


# Filter IDs from Survival dataframe
# ---------------------------------------------------------------------
def filter_survival_df_ids(group_1: str, 
                           group_2: str = "")->tuple|dict[str:list]:
    '''
    Filter ids from survival dataframe for one or two clinical groups
    selected. If group_2 is not an empty string, the function will searh
    for the ids of the two groups. If not, will search for te categories 
    ids inside group_1 instead.
    Return a list of ids for each selected group.

    ## Parameters:
        - group_1 (str): First group name.
        - group_2 (str): Second group name. Default "".

    ## Returns:
        - context (tuple|dict): If the two groups are not empty strings,
        it will return a tuple of two lists ids (one for each group), and
        if only group_1 is not an empty string, it will return a dictionary
        for each caregory in group_1 and its ids.
    '''

    # Debug
    print("Group 1", group_1)
    print("Group 2", group_2)

    # If group 2 is not an empty string, it means that two 
    # subcategories form is used, so two subcategories are selected:
    if group_2 != "":
        # Find the columns where the selected groups are:
        group_1_col:    str             = [cat for cat in cns.CATEGORIES if group_1 in cns.SURVIVAL_GROUPS[cat]][0]
        group_2_col:    str             = [cat for cat in cns.CATEGORIES if group_2 in cns.SURVIVAL_GROUPS[cat]][0]
        
        # Filter survival df with the columns found and the selected groups
        group_1_df:     pd.DataFrame    = cns.SURVIVAL.loc[cns.SURVIVAL[group_1_col] == group_1]
        group_2_df:     pd.DataFrame    = cns.SURVIVAL.loc[cns.SURVIVAL[group_2_col] == group_2]

        # Get patient ids from each filtered dataframe
        group_1_ids:    list            = [f"{patient_id}-01" for patient_id in list(group_1_df['id'])]
        group_2_ids:    list            = [f"{patient_id}-01" for patient_id in list(group_2_df['id'])]
        result:         tuple           = (group_1_ids, group_2_ids)

        print("TUPLE RESULT")

    # If only group one is not an empty string, it means that
    # a clinical category is selected instead of using the
    # two subcategories comparison form:
    else:
        # Get subcategories inside the selected category
        subcategories:  list            = cns.SURVIVAL_GROUPS[group_1] 
        # Create a dictionary where the the subcategories name are dict keys and the
        # value its own filtered dataframe:
        df_dict:    dict[str:pd.DataFrame]  = { subcat:cns.SURVIVAL.loc[cns.SURVIVAL[group_1] == subcat] 
                                                    for subcat in subcategories 
                                                    if subcat in list(cns.SURVIVAL[group_1])}
        # Dictionary with subcategories as keys and corresponding patient ids
        # as vlaues:
        ids_dict:       dict[str:list]  = {subcategory:list(df['id']) for subcategory, df in df_dict.items()}
        # Corrected ids dictionary
        result:         dict[str:list]  = {}

        subcat:         str
        for subcat, lst in ids_dict.items():
            corrected_ids:    list      = [f"{patient_id}-01" for patient_id in lst]
            result[subcat]              = corrected_ids

    return result
