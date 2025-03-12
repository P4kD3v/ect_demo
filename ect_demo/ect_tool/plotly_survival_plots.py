#   App Name:   Endometrial Cancer Tool v5.
#   Author:     Xavier Llobet Navàs.
#   Content:    Survival plots file.
#
# - This file contains all the functions needed to generate the
#   next plots:
#               - Survival curve.
#               - At risk by time table.
#               - Population bar plot.
#
#   - plotly_survival(): main function for survival curve analyisis.
#   - kaplan_meier_fitter_generator(): survival analysis for all dataset entries.
#   - survival_figure_generator(): survival analysis by clinical category.
#   - ceate_at_risk_values_list(): survival analysis by gene mRNA expression.
#   - at_risk_table_generator(): filter patient ids from survival 
#     dataframe.
#   - create_counting_bar_plot(): population bar plot.
#   - plotly_scikit_survival(): TEST function.
#   - kme_dict_generator(): TEST function.
#   - plotly_survival_function(): survival function for the entire
#     dataset.
#   - plotly_cumulative_density(): cumulative density function for the 
#     entire dataset.
#   - plotly_median_expresion_survival(): gene expression survival for 
#     median cutoff.
#   - plotly_percentil_expresion_survival(): gene expression survival for 
#     percentil cutoff.
#
# - Other modules used are:
#
#   - ut_constants
#   - ut_stats
#
# =====================================================================
# IMPORTS
# =====================================================================

from    lifelines                   import  KaplanMeierFitter
from    sksurv.nonparametric        import  kaplan_meier_estimator
from    plotly.graph_objs           import  Figure
from    plotly.offline              import  plot
import  plotly.figure_factory       as      ff
import  plotly.express              as      px
import  plotly.graph_objs           as      go
import  pandas                      as      pd
from    pandas                      import  concat
from    .                           import  ut_constants as cns
from    .                           import  ut_stats     as stats

# =====================================================================
# MAIN AND REUSABLE KAPLAN-MEIER FUNCTIONS
# =====================================================================

# Generator of KaplanMeierFitter object
# ---------------------------------------------------------------------
def kaplan_meier_fitter_generator(entry_df:     pd.DataFrame,
                                  entry_label:  str,
                                  mode:         str)->KaplanMeierFitter:
    '''
    Generates a new 'KaplanMeierFitter' object for the 'entry_df', labeled
    with the value from 'entry_label' parameter. Fits the model with the
    months and status from the 'entry_df' depending on the entry 'mode'.

    ## Parameters:
        - entry_df (pd.Dataframe): The Survival Dataframe to be analyzed.
        - entry_label (str): subcategory name used to label the KMF object.
        - mode (str): Can be Overall (os) or Progression-Free Survival
        (pfs).
        
    ## Return:
        - new_kmf_object (KaplanMeierFitter): new and fitted KaplanMeierFitter
        object.
    '''

    months_column_name: str = f"{mode}_months"
    status_column_name: str = f"{mode}_status"

    # Create a new object from KaplanMeierFitter class:
    new_kmf_object: KaplanMeierFitter = KaplanMeierFitter(alpha = 0.05,
                                                          label = entry_label)
    
    # Fit the model with the data:
    new_kmf_object.fit(entry_df[months_column_name],entry_df[status_column_name])

    return new_kmf_object


# Survival Plot generator
# ---------------------------------------------------------------------
def survival_figure_generator(survival_df:      pd.DataFrame,
                              plot_title:       str,
                              logrank_p_value:  str|dict,
                              facet_col_name:   str|None    = None,
                              entry_orders:     dict|None   = None,
                              facet_col_groups: list|None   = None,
                              facet_row_name:   str|None    = None,
                              facet_row_groups: list|None   = None)->Figure:
    '''
    Generate a Survival Figure using Plotly library.

    ## Parameters:
        - survival_df (pd.Dataframe): The Survival Dataframe to be analyzed.
        - plot_title (str): title for the plot.
        - logrank_p_value (str|dict): value of statistical test used in  
        survival analysis to compare the distribution of time to event in  
        two or more independent samples. If no facet is passed to the function,
        then the 'logrank_p_value' must be a string, else must be a dictionary
        containing one entry for each facet with the subcategory as key and
        the logrank pvalue as its value.
        - facet_col_name (str|None):  Optional parameter. Category name.
        To create a facet column for each subcategory in it.
        - entry_orders (dict): Optional parameter. The order to follow for 
        the subcategories when plotting the data.
        - facet_col_groups (list|None):  Optional parameter. All the
        sucbategories in 'facet_col_name'.
        - facet_row_name (str|None):  Optional parameter. Category name.
        To create a facet row for each subcategory in it.
        - facet_row_groups (list|None):  Optional parameter. All the
        sucbategories in 'facet_row_name'.

    ## Return:
        - survival_fig (Figure): Survival plot as plotly Figure object.
    '''
    # print("Error in 1")
    text_colors_list:       list    = ['blue', 'red', 'green', 'purple', 'darkorange']
    groups:                 list    = list(set(survival_df['Legend']))
    current_colors_list:    list    = text_colors_list[:len(groups)]
    # print("Error in 2")

    # Create the plot figure:
    if (facet_col_groups != None):
        survival_fig: Figure  = px.line(data_frame              = survival_df,
                                        width=1000,
                                        x                       = "timeline",
                                        y                       = "Survival probability",
                                        color                   = "Legend",
                                        facet_col               = facet_col_name,
                                        facet_row               = facet_row_name,
                                        color_discrete_sequence = current_colors_list,
                                        category_orders         = entry_orders,
                                        markers                 = True,
                                        line_shape              = 'vh',
                                        title                   = plot_title)
    else:
        survival_fig: Figure  = px.line(data_frame              = survival_df,
                                        x                       = "timeline",
                                        y                       = "Survival probability",
                                        color                   = "Legend",
                                        facet_col               = facet_col_name,
                                        facet_row               = facet_row_name,
                                        color_discrete_sequence = current_colors_list,
                                        category_orders         = entry_orders,
                                        markers                 = True,
                                        line_shape              = 'vh',
                                        title                   = plot_title)
    # print("Error in 3")

    # Add annotations
    if (facet_col_groups != None) and not (facet_row_groups != None):
        count: int = 1
        x_range_anottation_move = 0.01
        anot_facet_extra_sapce: float           = 0.25

        if facet_col_name == 'bmi_status':
            x_range_anottation_move = x_range_anottation_move + (1/len(facet_col_groups))

        for facet in facet_col_groups:

        # Add Figure p-value annotation:
            # print("Error in row", row)
            survival_fig.add_annotation(    xref="paper", 
                                            yref="paper",
                                            x               = x_range_anottation_move,
                                            y               = 0.05, 
                                            borderpad               = 0,
                                            text                    = f"logrank pValue: {logrank_p_value[facet]}",
                                            showarrow               = False,
                                            font                    = dict( family  = "sans serif",
                                                                            size    = 15,
                                                                            color   = "black"))

            if facet_col_name == 'bmi_status':
                                                        
                x_range_anottation_move = x_range_anottation_move
                count = count + 1
                if count == 2:
                        x_range_anottation_move = x_range_anottation_move + (1.02/len(facet_col_groups))
                if count == 3:
                        x_range_anottation_move = x_range_anottation_move + (0.75/len(facet_col_groups))
                # if count == 4:
                #         x_range_anottation_move = x_range_anottation_move - (1/len(facet_col_groups))*3
            else:
                if len(facet_col_groups) < 4:
                        x_range_anottation_move = x_range_anottation_move + ((1+anot_facet_extra_sapce)/len(facet_col_groups)) + 0.2
                        count = count + 1
                        anot_facet_extra_sapce = anot_facet_extra_sapce + 0.015
                elif len(facet_col_groups) == 4:   
                        if count < 3:
                                x_range_anottation_move = x_range_anottation_move + (1/len(facet_col_groups))                                                            
                        count = count + 1
                        if count == 3:
                                x_range_anottation_move = x_range_anottation_move + (0.7/len(facet_col_groups))
                        if count == 4:
                                x_range_anottation_move = x_range_anottation_move + (1/len(facet_col_groups))
                elif len(facet_col_groups) == 5:
                        x_range_anottation_move = x_range_anottation_move + (1/len(facet_col_groups)) + 0.005                                                    
                        count = count + 1
                        if count == 3:
                                x_range_anottation_move = x_range_anottation_move + 0.075   
                        if count == 4:
                                x_range_anottation_move = x_range_anottation_move + 0.08    
                                                


    elif (facet_row_groups != None) and not (facet_col_groups != None):
        row: int = 1
        for facet in facet_row_groups:

        # Add Figure p-value annotation:
            survival_fig.add_annotation(    row=row,col=1,
                                            x                       = 50,
                                            y                       = 1.01,
                                            borderpad               = 0,
                                            text                    = f"logrank pValue: {logrank_p_value[facet]}",
                                            showarrow               = False,
                                            font                    = dict( family  = "sans serif",
                                                                            size    = 15,
                                                                            color   = "black"))
            row = row+1
    elif (facet_row_groups != None) and (facet_col_groups != None):
        pass
    else:
        survival_fig.add_annotation(    xref="paper", 
                                        yref="paper",
                                        x               = 0.05,
                                        y               = 0.05,
                                        borderpad           = 0,
                                        text                = f"logrank pValue: {logrank_p_value}",
                                        showarrow           = False,
                                        font                = dict( family  = "sans serif",
                                                                    size    = 15,
                                                                    color   = "black"))
    
    survival_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]) if "=" in a.text else a.update(text=a.text))
    
    # Update traces size and symbol:
    survival_fig.update_traces(     marker                  = dict(size=6, symbol="line-ns-open"),
                                    line                    = dict(width=1))  
    
    # Update layout like axis, titles, legend:
    survival_fig.update_layout(     hovermode               = "x unified",
                                    yaxis_title             = "Survival probability",
                                    barmode                 = 'stack',
                                    yaxis_range             = [0,1.05],
                                    legend                  = dict( orientation = 'v',
                                                                    font        = dict(size= 15)),
                                    title_x                 = 0.05,
                                    title_font_family       = "Raleway, sans-serif",
                                    title                   = dict(font=dict(size=20)),
                                    bargap                  = 0.1,
                                    paper_bgcolor           = 'rgb(255,255,255)',
                                    plot_bgcolor            = 'rgb(255, 255, 255)')
    
    # Update x and y axes
    survival_fig.update_xaxes(  title               = "Months",
                                showline            = True,
                                linewidth           = 2,
                                linecolor           = 'black',
                                mirror              = True)
    survival_fig.update_yaxes(  showline            = True,
                                linewidth           = 2,
                                linecolor           = 'black',
                                mirror              = True)
    
    return survival_fig


# At risk by time values generator
# ---------------------------------------------------------------------
def ceate_at_risk_values_list(entry_group:          str,
                              at_risk_event_table:  pd.DataFrame)->list:
    '''
    Create a list with the patients amount at risk by time table
    for the 'at_risk_event_table' dataframe.

    ## Parameters:
        - entry_group (str): all the prefiltered groups that are
        in the category to anayze.
        - at_risk_event_table (pd.DataFrame): dataframe containing all the 
        patients at risk by time data.
        
    ## Return:
        - at_risk_list (list): list of the population amount at risk by
        time.
    '''
    at_risk_list: list = [  entry_group, 
                            at_risk_event_table['at_risk'].max(), 
                            at_risk_event_table.loc[at_risk_event_table.index <= 10]['at_risk'].min(), 
                            at_risk_event_table.loc[(at_risk_event_table.index <= 20)]['at_risk'].min(), 
                            at_risk_event_table.loc[(at_risk_event_table.index <= 30)]['at_risk'].min(), 
                            at_risk_event_table.loc[(at_risk_event_table.index <= 40)]['at_risk'].min(), 
                            at_risk_event_table.loc[(at_risk_event_table.index <= 50)]['at_risk'].min(), 
                            at_risk_event_table['at_risk'].min()]
    
    return at_risk_list


# At risk by time table generator
# ---------------------------------------------------------------------
def at_risk_table_generator(survival_groups: list, 
                            entry_kmf_dict:  dict[str:KaplanMeierFitter],
                            entry_title:     str)->Figure:
    '''
    Create a table with the patients at risk by time for each entry in 
    the 'entry_kmf_dict'.

    ## Parameters:
        - survival_groups (list): all the prefiltered groups that are
        in the category to anayze.
        - entry_kmf_dict (dict[str:KaplanMeierFitter]): dictionary
        containing the subcategories as key, and its related and fitted
        KaplanMeierFitter object as value.
        - entry_title (str): Can be Overall (os) or Progression-Free Survival
        (pfs).
        
    ## Return:
        - survival_table (Figure): At risk by time table plot as plotly Figure object.
    '''
    # Create a dictionary with the at risk event tables:
    at_risk_tables_dict:    dict    = {group:entry_kmf_dict[group].event_table 
                                       for group in survival_groups if group in list(entry_kmf_dict.keys())}
    
    # Create a list with the values from the at risk event tables:
    at_risk_values_list:    list    = [ceate_at_risk_values_list(group, at_risk_tables_dict[group]) 
                                       for group in survival_groups if group in list(entry_kmf_dict.keys())]
    # Set the headers for the table:
    table_headers:          list    = ['Months', '0', '10', '20', '30', '40', '50', '60']

    # Insert headers in the beginning of the event values list:
    at_risk_values_list.insert(0,table_headers)

    # Set colors list:
    text_colors_list:       list    = ['white', 'blue', 'red', 'green', 'purple', 'darkorange']
    current_colors_list:    list    = text_colors_list[:len(list(entry_kmf_dict.keys()))+1]

    # Create table as plot
    survival_table:         Figure  = ff.create_table(at_risk_values_list, 
                                                      height_constant=20,
                                                      font_colors=current_colors_list)

    # Create title:
    table_title:            str     = f"<b>Population at risk by time of</b> {entry_title}"

    #Update table layout margins
    survival_table.update_layout(font               = dict(size = 10),
                                 margin             = {'t':50, 'b':0, 'r':50},
                                 title_text         = table_title,
                                 title_font_family  = "sans-serif",
                                 title_x            = 0.5,
                                 title              = dict(font=dict(size=18)))

    return survival_table


# Kaplan-Meier Survival curve manager
# ---------------------------------------------------------------------
def plotly_survival(entry_df:           pd.DataFrame,
                    mode:               str,
                    plot_title:         str,
                    groups_column_name: str,
                    survival_groups:    list[str],
                    facet_col_name:     str|None    = None,
                    facet_col_groups:   list|None   = None,
                    facet_row_name:     str|None    = None,
                    facet_row_groups:   list|None   = None)->tuple[str,str]:
    '''
    This function generate a survival curve for the category in 
    'groups_column_name' using the Kaplan-Meier method and a risk by time 
    table plot, and return it embedded into an html 'div' tag.

    -Kaplan-Meier estimate: is a way of computing the survival over 
    time in spite of all these difficulties associated with subjects or 
    situations. For each time interval, survival probability is calculated 
    as the number of subjects surviving divided by the number of patients 
    at risk.

    ## Parameters:
        - entry_df (pd.Dataframe): The Survival Dataframe to be analyzed.
        - mode (str): Can be Overall (os) or Progression-Free Survival
        (pfs).
        - plot_title (str): title for the plot.
        - groups_column_name (str): category to be analyzed.
        - survival_groups (list[str]): all the prefiltered groups that are
        in the category to anayze (groups_column_name).
        - facet_col_name (str|None):  Optional parameter. Category name.
        To create a facet column for each subcategory in it.
        - facet_col_groups (list|None):  Optional parameter. All the
        sucbategories in 'facet_col_name'.
        - facet_row_name (str|None):  Optional parameter. Category name.
        To create a facet row for each subcategory in it.
        - facet_row_groups (list|None):  Optional parameter. All the
        sucbategories in 'facet_row_name'.

    ## Returns a tuple of:
        - survuval_div (str): survival curve plot embedded into an html 
        'div' tag.
        - at_risk_table_div (str): : at risk by time table plot embedded 
        into an html 'div' tag.
    '''

    # Facet checkers
    is_facet_col:               bool                = (facet_col_name !=  None)
    is_facet_row:               bool                = (facet_row_name !=  None)
    
    # Creating the names where the moths are status data are dependig on the 'mode':
    months_column_name:         str                 = f"{mode}_months"
    status_column_name:         str                 = f"{mode}_status"  
   
    # If only Facet Column
    if is_facet_col and (not is_facet_row):
        plot_groups_list:       list[pd.DataFrame]  = []
        logrank_p_value:        dict                = {}        
        setted_plot_values:     list                = list(set(entry_df[groups_column_name]))
        setted_fcol_values:     list                = list(set(entry_df[facet_col_name]))
        # If Gene selected
        if ('gene' in facet_col_name) or ('gene' in groups_column_name):
            print("Is Gene")
            if 'gene' in facet_col_name:
                plot_groups:    list                = [subcat for subcat in cns.SURVIVAL_GROUPS[groups_column_name] if subcat in setted_plot_values]
                cat_orders:         dict            = {'gene':facet_col_groups}
            elif 'gene' in groups_column_name:
                plot_groups:    list                = [subcat for subcat in setted_plot_values]
                cat_orders:         dict            = {facet_col_name:facet_col_groups}


            

            print("plot_groups", plot_groups)
            print("facet_col_groups", facet_col_groups)
            print("cat_orders", cat_orders)
            
        # If Gene not selected
        else:
            print("Is not Gene")
            plot_groups:        list                = [subcat for subcat in cns.SURVIVAL_GROUPS[groups_column_name] if subcat in setted_plot_values]
            facet_col_groups:   list                = [subcat for subcat in cns.SURVIVAL_GROUPS[facet_col_name] if subcat in setted_fcol_values] 
            cat_orders:         dict                = {facet_col_name:facet_col_groups}

            print("plot_groups", plot_groups)
            print("facet_col_groups", facet_col_groups)
            print("cat_orders", cat_orders)

        for facet in facet_col_groups:
            print("\nIN facet:", facet)
            print("---------------------------")

            current_facet_df:   pd.DataFrame        = entry_df[entry_df[facet_col_name] == facet]
            # Calculate StatisticalResult object with properties 'p_value', 'summary', 'test_statistic', 'print_summary':
            current_p_value:    str                 = stats.calculate_formatted_multi_logrank_p(current_facet_df[months_column_name],                                                            
                                                                                                current_facet_df[groups_column_name],
                                                                                                current_facet_df[status_column_name])
            logrank_p_value[facet]                  = current_p_value

            for group in plot_groups:
                print("\nIN group:", group)
                print("---------------------------")
                current_group_df:   pd.DataFrame    = current_facet_df[current_facet_df[groups_column_name] == group]

                if len(current_group_df)>2:
                    print("DF bigger than 2")
                    status_values:  list[bool]          = [True if int(value)==1 else False for value in current_group_df[status_column_name]]
                    kmf:            KaplanMeierFitter   = kaplan_meier_fitter_generator(current_group_df,group,mode)
                    kme_df:         pd.DataFrame        = pd.DataFrame( data = {'timeline':             kmf.survival_function_.index,
                                                                                'Survival probability': kmf.survival_function_[group],
                                                                                'Legend':               group,
                                                                                facet_col_name:         facet})                    
                    plot_groups_list.append(kme_df)
                else:
                    pass
            

    # If only Facet Row
    elif is_facet_row and (not is_facet_col):
        pass
    
    # If no Facets
    else:
        # print("entry_df", entry_df)
        # print("mode", mode)
        # print("plot_title", plot_title)
        # print("groups_column_name", groups_column_name)
        print("survival_groups", survival_groups)

        # Calculate StatisticalResult object with properties 'p_value', 'summary', 'test_statistic', 'print_summary':
        logrank_p_value:        str                 = stats.calculate_formatted_multi_logrank_p(entry_df[months_column_name],                                                            
                                                                                                entry_df[groups_column_name],
                                                                                                entry_df[status_column_name])
        # Create a dictionary with the 'survival_groups' as keys and its relate DataFrame:
        groups_df_dict:         dict                = { group:entry_df.loc[entry_df[groups_column_name] == group] 
                                                        for group in survival_groups if group in list(entry_df[groups_column_name])}

        # KM FITTER =====================================================================================================================================

        # Create a dictionary with the 'survival_groups' as keys and its relate and fitted KaplanMeierFitter object:
        groups_kmf_dict:        dict[str:KaplanMeierFitter]  = {group:kaplan_meier_fitter_generator(groups_df_dict[group],group,mode) 
                                                                for group in survival_groups if len(groups_df_dict[group])>2}

        # Create a list of Dataframes with the survival data in each dataframe:
        plot_groups_list:       list[pd.DataFrame]  = [ pd.DataFrame(data = {   'timeline':             groups_kmf_dict[group].survival_function_.index,
                                                                                'Survival probability': groups_kmf_dict[group].survival_function_[group],
                                                                                'Legend':               group})
                                                        for group in survival_groups if len(groups_df_dict[group])>2]
        
        # if groups_column_name == 'tumor_type':
        #     print("SEROUS:", set(list(groups_df_dict['Serous']['tumor_type'])), len(groups_df_dict['Serous']['tumor_type']))
        cat_orders:             dict                = {'Legend':list(groups_kmf_dict.keys())}
        
        
    # Concat survival DataFrames. 'objs' value has to a list of DataFrames.
    plot_groups_df:             pd.DataFrame        = concat(objs=plot_groups_list, ignore_index=True)
    # print("Creating Survival Figure.................")

    # Create the plot figure:
    survival_fig:               Figure              = survival_figure_generator(plot_groups_df, 
                                                                                plot_title, 
                                                                                logrank_p_value,                                                                                 
                                                                                facet_col_name   = facet_col_name,
                                                                                entry_orders     = cat_orders,
                                                                                facet_col_groups = facet_col_groups,
                                                                                facet_row_name   = facet_row_name,
                                                                                facet_row_groups = facet_row_groups)
    if (not is_facet_col) and (not is_facet_row):
        # print("Creating Survival Table Figure...........")
        at_risk_table:          Figure              = at_risk_table_generator(survival_groups, groups_kmf_dict, plot_title)
        at_risk_table_div:      str                 = plot(at_risk_table, output_type="div", config=cns.TOOLBAR_CONFIG)

    if is_facet_col:
        if len(cat_orders[facet_col_name]) >3:
            survuval_div:               str                 = plot(survival_fig, output_type="div", config=cns.TOOLBAR_CONFIG_XL)
        else:
             survuval_div:               str                 = plot(survival_fig, output_type="div", config=cns.TOOLBAR_CONFIG_L)
    else:
        survuval_div:               str                 = plot(survival_fig, output_type="div", config=cns.TOOLBAR_CONFIG)
    
    # print("Returning Plotly figures.................")
    if (not is_facet_col) and (not is_facet_row):
        return (survuval_div, at_risk_table_div)
    else:
        return (survuval_div, "")


# =====================================================================
# POPULATION FUNCTION
# =====================================================================
    
# Pupulation bar plot
# ---------------------------------------------------------------------
def create_counting_bar_plot(entry_df:      pd.DataFrame,
                             x_column_name: str,
                             plot_title:    str,
                             entry_orders:  dict,
                             entry_x_title: str)->str:
    '''
    Create a bar plot for the subcategories population in te 
    'x_column_name' name.

    ## Parameters:
        - entry_df (pd.Dataframe): The Dataframe to be analyzed.
        - x_column_name (str): Category name from the 'entry_df'.
        - plot_title (str): title for the plot.
        - entry_orders (dict): The order to follow for the subcategories 
        when plotting the data.
        - entry_x_title (str): x axis title.

    ## Return:
        - bar_plot_div (str): population bar plot embedded into an html 
        'div' tag.
    '''

    # Set title size depending on 'plot_title' content.
    if 'EC Population' in plot_title:
        my_size: int = 25
    else:
        my_size: int = 18

    # Color orders.
    text_colors_list:       list    = ['blue', 'red', 'green', 'purple', 'darkorange']

    # Setted groups.
    groups:                 list    = list(set(entry_df[x_column_name]))

    # Filter colors depending on the 'groups' length.
    current_colors_list:    list    = text_colors_list[:len(groups)]

    # Histogram figure
    bar_fig:                Figure  = px.histogram( data_frame              = entry_df,
                                                    x                       = x_column_name,
                                                    color                   = x_column_name,
                                                    color_discrete_sequence = current_colors_list,
                                                    title                   = plot_title,
                                                    category_orders         = entry_orders,
                                                    text_auto               = True)
    # Updating x axis and plot layout.
    bar_fig.update_xaxes(   tickangle           = 30)
    bar_fig.update_layout(  showlegend          = True,
                            legend_title_text   = 'Legend',
                            title               = dict(font=dict(size=my_size)),
                            title_font_family   = "sans-serif",
                            title_x             = 0.5,
                            xaxis_title         = entry_x_title,
                            bargap              = 0,
                            font                = dict(size = 9),
                            yaxis               = dict(showgrid = True),
                            xaxis               = dict(showgrid = False))

    bar_plot_div:           str     = plot(bar_fig, output_type="div", config=cns.TOOLBAR_CONFIG)

    return bar_plot_div


# GENERATOR OF SCIKIT-SURVIVAL KAPLAN-MEIER ESTIMATOR DICT
# ---------------------------------------------------------------------
def kme_dict_generator( entry_df:     pd.DataFrame,
                        mode:         str)->dict:
    '''
    Generates a new 'KaplanMeierFitter' object labeled with the
    value from 'entry_label' parameter, and fits the model with
    the months and status data from the 'entry_df' depending on
    the entry 'mode'.
    '''

    months_column_name: str = f"{mode}_months"
    status_column_name: str = f"{mode}_status"

    kme_time, kme_survival_prob, kme_conf_int = kaplan_meier_estimator( list(entry_df[status_column_name]),
                                                                        list(entry_df[months_column_name]),
                                                                        conf_type="log-log")
    kme_dict: dict = {'time':       list(kme_time),
                      'survival':   list(kme_survival_prob),
                      'conf_low':   list(kme_conf_int[0]),
                      'conf_up':    list(kme_conf_int[1])}

    return kme_dict


# =====================================================================
# SURVIVAL FUNCTIONS FOR THE ENTIRE DATASET
# =====================================================================

# Kaplan-Meier survival plot for the entire dataset entries
# ---------------------------------------------------------------------
def plotly_survival_function(entry_kmf:     KaplanMeierFitter, 
                             x_values:      pd.Series, 
                             mode:          str, 
                             plot_title:    str)->tuple[str,str]:
    '''
    This function generate a survival curve for all the entries in the 
    dataset using the Kaplan-Meier method and a risk by time table plot, 
    and return it embedded into an html 'div' tag.

    - Kaplan-Meier estimate: is a way of computing the survival over time 
    in spite of all these difficulties associated with subjects or 
    situations. For each time interval, survival probability is calculated 
    as the number of subjects surviving divided by the number of patients 
    at risk.

    ## Parameters:
        - entry_kmf (KaplanMeierFitter): fitted KaplanMeierFitter object.
        - x_values (pd.Series): values of the survival function from 
        the 'entry_kmf' object.
        - mode (str): mode (str): can be Overall (os) or Progression-Free Survival
        (pfs).
        - plot_title (str): title for the plot.

    ## Returns a tuple of:
        - survuval_div (str): survival curve plot embedded into an html 
        'div' tag.
        - table_plot_div (str): : at risk by time table plot embedded 
        into an html 'div' tag.
    '''

    # Create an empty Figure.
    fig:            Figure              = go.Figure()

    # Add survival trace.
    fig.add_trace(go.Scatter(   x       = x_values,
                                y       = entry_kmf.survival_function_['KM Survival Curve'],
                                name    = 'Survival',
                                line    = dict(color='royalblue', width=1, shape='vh')))
    
    # Update survival trace
    fig.update_traces(mode="markers+lines", marker=dict(size=7, symbol="line-ns-open"))                                    
    
    # Add confidence intervals traces
    fig.add_trace(go.Scatter(   x       = x_values,
                                y       = entry_kmf.confidence_interval_['KM Survival Curve_upper_0.95'],
                                name    = 'Conf.Up 0.95',
                                line    = dict(color='coral', width=1, dash='dot', shape='vh')))

    fig.add_trace(go.Scatter(   x       = x_values,
                                y       = entry_kmf.confidence_interval_['KM Survival Curve_lower_0.95'],
                                name    = 'Conf.Down 0.95',
                                line    = dict(color='coral', width=1, dash='dash', shape='vh')))

    # Update plot layout
    fig.update_layout(  
                        xaxis_title     = "Months",
                        yaxis_title     = f"{mode} probability value",
                        hovermode       = "x unified",
                        legend          = dict( orientation = 'v',
                                                        # yanchor     = 'bottom',
                                                        # y           = 1.02,
                                                        # xanchor     = 'right',
                                                        # x           = 1,
                                                        font=dict(size= 11)),
                        title_x         =0.5,
                        title_font_family="sans-serif",
                        title           =dict(text=plot_title, font=dict(size=25)),
                        xaxis           = dict( zeroline    = False,
                                                domain      = [0,0.94],
                                                showgrid    = True),
                        yaxis           = dict( zeroline    = False,
                                                showgrid    = True),
                        bargap          = 0.1)
    
    # Create headers for at risk by time table.
    table_data:         list            = [['Months', '0', '10', '20', '30', '40', '50', '60']]

    # At risk by time table dataframe
    all_table_df:   pd.DataFrame    = entry_kmf.event_table

    # At risk by time table values.
    all_values:     list            = [ "At risk", 
                                        all_table_df['at_risk'].max(), 
                                        all_table_df.loc[all_table_df.index < 10]['at_risk'].min(), 
                                        all_table_df.loc[(all_table_df.index < 20)]['at_risk'].min(), 
                                        all_table_df.loc[(all_table_df.index < 30)]['at_risk'].min(), 
                                        all_table_df.loc[(all_table_df.index < 40)]['at_risk'].min(), 
                                        all_table_df.loc[(all_table_df.index < 50)]['at_risk'].min(), 
                                        all_table_df['at_risk'].min()]
    table_data.append(all_values)        

    # Create at risk by time table.
    fig_table:      Figure          = ff.create_table(table_data, height_constant=20)

    # Update table layout
    fig_table.update_layout(margin  = {'l':0, 'r':20})

    # Embedd plots into 'div' html tag.
    plot_div:       str             = plot(fig, output_type="div", config=cns.TOOLBAR_CONFIG)
    table_plot_div: str             = plot(fig_table, output_type="div")
    
    return (plot_div, table_plot_div)


# Kaplan-Meier Confidence Intervals Cumulative Density plot for the 
# entire dataset entries.
# ---------------------------------------------------------------------
def plotly_cumulative_density(entry_kmf:    KaplanMeierFitter, 
                              x_values:     pd.Series, 
                              mode:         str, 
                              plot_title:   str)->str:
    '''
    Calculate an estimated cumulative density (or proportion)
    of failures at each time point.

    -The confidence level sets the boundaries of a confidence interval, 
    this is conventionally set at 95% to coincide with the 5% convention 
    of statistical significance in hypothesis testing. In some studies 
    wider (e.g. 90%) or narrower (e.g. 99%) confidence intervals will be 
    required. This rather depends upon the nature of your study. You should 
    consult a statistician before using CI's other than 95%.

    -A 95% Cconfidence Interval is the interval that you are 95% certain 
    contains the true population value as it might be estimated from a 
    much larger study.
    
    ## Parameters:
        - entry_kmf (KaplanMeierFitter): fitted KaplanMeierFitter object.
        - x_values (pd.Series): values of the survival function from 
        the 'entry_kmf' object.
        - mode (str): mode (str): can be Overall (os) or Progression-Free Survival
        (pfs).
        - plot_title (str): title for the plot.

    ## Return:
        - plot_div (str): Confidence Interval Cumulative Density plot embedded
        into a 'div' html tag.
    '''

    fig:            Figure                  = go.Figure()

    fig.add_trace(go.Scatter(   x           = x_values,
                                y           = entry_kmf.cumulative_density_['KM Survival Curve'],
                                name        = 'Survival',
                                line        = dict(color='royalblue', width=1, shape='vh')))

    fig.update_traces(mode="markers+lines", marker=dict(size=7, symbol="line-ns-open"))                                    
    
    fig.add_trace(go.Scatter(   x           = x_values,
                                y           = entry_kmf.confidence_interval_cumulative_density_['KM Survival Curve_upper_0.95'],
                                name        = 'Conf.Up 0.95',
                                line        = dict(color='coral', width=1, dash='dot', shape='vh')))

    fig.add_trace(go.Scatter(   x           = x_values,
                                y           = entry_kmf.confidence_interval_cumulative_density_['KM Survival Curve_lower_0.95'],
                                name        = 'Conf.Down 0.95',
                                line        = dict(color='coral', width=1, dash='dash', shape='vh')))
    
    fig.update_layout(      xaxis_title     = "Months",
                            yaxis_title     = f'''{mode} Cumulative Density value''',
                            hovermode       = "x unified",
                            legend          = dict( orientation = 'v',
                                                        # yanchor     = 'bottom',
                                                        # y           = 1.02,
                                                        # xanchor     = 'right',
                                                        # x           = 1,
                                                        font=dict(size= 11)),
                            title_x         =0.5,
                            title_font_family="sans-serif",
                            title           =dict(text=plot_title, font=dict(size=25)),
                            xaxis           = dict( zeroline    = False,
                                                    domain      = [0,0.94],
                                                    showgrid    = True),
                            yaxis           = dict( zeroline    = False,
                                                    showgrid    = True),
                            bargap          = 0.1)
    
    plot_div:       str             = plot(fig, output_type="div", config=cns.TOOLBAR_CONFIG)
    
    return plot_div


