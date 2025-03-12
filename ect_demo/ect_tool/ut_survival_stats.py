#   App Name:   Endometrial Cancer Tool v5.
#   Author:     Xavier Llobet Navàs.
#   Content:    Clinical subcategory survival analysis.
#
# - This file contains two functions, one for search survival plots 
#   in the database for certain clinical subcategory, and second to
#   generate the plots if not in the database. Te functions are:
#
#   - survival_statistics_generator(): survival analysis for all  
#     dataset entries.
#   - check_plots_for_survival_stats(): search for plots in the
#     database.
#
# - Other modules used are:
#
#   - ut_survival_plots
#   - ut_database
#   - ut_constants
#
# =====================================================================
# IMPORTS
# =====================================================================

from . import   plotly_survival_plots   as      sp
from . import   ut_constants            as      cns
import          pandas                  as      pd

# =====================================================================
# FUNCTIONS
# =====================================================================

# Generate several plots for a clinical subcategory:
# ---------------------------------------------------------------------
def survival_statistics_generator(df:                       pd.DataFrame,
                                  mode:                     str,
                                  column_name:              str, 
                                  current_subcategory:      str,
                                  current_categories_dict:  dict,
                                  target_categories:        list)->dict:
    '''
    Retrieve plots from the database. If plots not in the database,
    will ask 'ut_survival_plots' module to create survival curve, at 
    risk by time table and population bar plot for each category 
    except for the category where the 'column_name' value belongs to.

    ## Parameters:
        - df (pd.Dataframe): The Survival Dataframe to be analyzed.
        - mode (str): Can be Overall (os) or Progression-Free Survival
        (pfs).
        - column_name (str): main clinical category where 
        'current_subcategory'belongs to.
        - current_subcategory (str): clinical subcategory to be analyzed.
        - current_categories_dict (dict): dictionary of all the 
        subcategories that belongs to the main clinical category 
        (column_name).
        - target_categories (list): all the clinical categories to search 
        in the subcategory to analyze (current_subcategory).

    ## Returns:
        - context (dict): Dictionary with the data to fill up the Django
        template.
    '''

    controller: bool = False

    if mode == 'pfs':
        analysis_type:  str             = 'Progression-Free Survival'
    elif mode == 'os':
        analysis_type:  str             = 'Overall Survival'

    # If plots not in the database:
    if not controller:

        #Sort DataFrame by the survival mode:
        sort_by:        str             = f'''{mode}_months'''
        sorted_df:      pd.DataFrame    = df.sort_values(by=sort_by, ascending=True)

        # Cycle will be used to create the context keys for the user's html view:
        cycle:          int             = 1

        # Create new context
        context                         = {}
        
        # Create the survival, table and bar plots for each category in the 'target_categories' variable:
        for category in target_categories:

            # For title complement:
            sub_cat:    str             = current_categories_dict[current_subcategory]
            main_cat:   str             = cns.CATEGORIES_DICT[category]

            if (current_subcategory == 'Yes') or (current_subcategory == 'No'):
                sub_cat = f"Radiation Therapy ({sub_cat})"

            # Keys for the context if plots in the database:
            key1:                       str         = f"plot{cycle}"
            key2:                       str         = f"table{cycle}"
            key3:                       str         = f"bar{cycle}"
            survival_title:             str         = f"<b>EC <b style='color: green;'>{sub_cat}</b> {analysis_type}</b><br><sup>by <b style='color: green;'>{main_cat}</b></sup>"

            # Set column values:
            survival_groups:            list[str]   = list(set(sorted_df[category]))
            ordered_survival_groups:    list        = [value for value in cns.SURVIVAL_GROUPS[category] if value in survival_groups]
            length_apply:               list        = [group for group in ordered_survival_groups if (len(sorted_df.loc[sorted_df[category]==group])>2)]

            # Set order for categories:
            cat_orders: dict            = {category:length_apply}
            
            # Create survival and table plots:
            plot, table                 = sp.plotly_survival(sorted_df, 
                                                            mode, 
                                                            survival_title,
                                                            category,
                                                            length_apply)

            # Create bar plot:
            bar_title:  str             = f"<b>EC {sub_cat} Population</b><br><sup>by <b style='color: green;'>{main_cat}</b>"
            bar:        str             = sp.create_counting_bar_plot(  sorted_df, 
                                                                        category,
                                                                        bar_title, 
                                                                        cat_orders, 
                                                                        cns.CATEGORIES_DICT[category])

            # Add plots to 'context' dictionary:
            context[key1]   = plot
            context[key2]   = table
            context[key3]   = bar
            
            # Update 'cycle' variable
            cycle = cycle+1

        # Needed keys for access and fill the template
        context['title']                        = 'Overview Survival' 
        context['survival_mode']                = mode
        context['analysis_type']                = analysis_type             

    return context

