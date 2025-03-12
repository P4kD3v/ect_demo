#   App Name:   Endometrial Cancer Tool v5.
#   Author:     Xavier Llobet Navàs.
#   Content:    ECT statistics.
#
# - This file contains functions for statistical analysis. The
#   functions are:
#
#   - calculate_formatted_mannwhitneyu(): calculate and format 
#     Mann-Whitney U pvalue, ans return it as string.
#   - calculate_formatted_R_and_pearsonr(): calculate and format Pearson 
#     correlation coefficient and p-value for testing non-correlation.
#   - calculate_formatted_logrank_p(): calculate and format logrank
#     test pvalue.
#   - calculate_formatted_multi_logrank_p(): calculate and format 
#     multivariate logrank test pvalue.
#   - global_stats(): generate global statistics for Overview and Genes
#     sections.
#   - plotly_counting_bar_plot(): create a counting bar plot for the 
#     entry dataframe. Used by 'global_stats' function. 
#
# - Other modules used are:
#
#   - ut_database
#   - ut_constants
#
# =====================================================================
# IMPORTS
# =====================================================================

from    plotly.graph_objs       import  Figure
from    plotly.offline          import  plot
import  plotly.express          as      px
import  plotly.graph_objs       as      go
import  pandas                  as      pd
from    .                       import  ut_constants        as cns
from    scipy.stats             import  mannwhitneyu, pearsonr
from    lifelines.statistics    import  logrank_test, multivariate_logrank_test

# Caluclate and format Mann-hitney U pvalue.
# ---------------------------------------------------------------------
def calculate_formatted_mannwhitneyu(values_list_1: list|pd.Series,
                                     values_list_2: list|pd.Series)->str:
    '''
    Perform the Mann-Whitney U rank test on two independent samples.
    Return a formatted Mann-Whitney pvalue.

    ## Parameters:
        - values_list_1 (list|pd.Series): First array of values.
        - values_list_s (list|pd.Series): Second array of values.
        
    ## Return:
        - format_pval (str): formatted pvalues as string.
    '''

    # Calculate pvalue.
    U1, pval                        = mannwhitneyu( values_list_1, 
                                                    values_list_2, 
                                                    method = "auto")
    
    pval_rounded                    = round(pval, 3)
    format_rounded_pval:    str     = "{:e}".format(pval_rounded)
    
    # Format pvlaue.
    format_pval:            str     = "{:e}".format(pval)

    return format_pval


# Caluclate and format Pearson pvalue and correlation coeficient.
# ---------------------------------------------------------------------
def calculate_formatted_R_and_pearsonr( values_list_2: list,
                                        values_list_1: list)->tuple[str,float]:
    '''
    Calculate and format Pearson correlation coefficient and p-value 
    for testing non-correlation.

    - The Pearson correlation coefficient measures the linear relationship
    between two datasets. Like other correlation coefficients, this one 
    varies between -1 and +1 with 0 implying no correlation. 
    Correlations of -1 or +1 imply an exact linear relationship. 
    
    Positive correlations imply that as x increases, so does y. 
    Negative correlations imply that as x increases, y decreases.

    ## Parameters:
        - values_list_1 (list): First list of values.
        - values_list_2 (list): Second list of values.
        
    ## Returns a tuple of:
        - p_value (str): formatted pvalue.
        - corr_coef (float): rounded correlation coeficient.
    '''

    # Pearson correlation.
    pearson_values  = pearsonr(values_list_2, values_list_1)

    # Rounded correlation coeficient.
    corr_coef       = round(pearson_values[0], 3)

    # Formatted pvalue.
    p_value         = "{:e}".format(pearson_values[1], 4)

    return (p_value, corr_coef)


# Caluclate logrank test pvalue.
# ---------------------------------------------------------------------
def calculate_formatted_logrank_p(  group_1_months: list|pd.Series,
                                    group_2_months: list|pd.Series,
                                    group_1_status: list|pd.Series,
                                    group_2_status: list|pd.Series)->str:
    '''
    Measures on whether two intensity processes are different. 
    That is, given two event series, determines whether the data generating 
    processes are statistically different.

    ## Parameters:
        - group_1_months (list|pd.Series): array of months for group 1.
        - group_2_months (list|pd.Series): array of months for group 2.
        - group_1_status (list|pd.Series): array of status for group 1.
        - group_2_status (list|pd.Series): array of status for group 2.
        
    ## Return:
        - p_value (str): formatted pvalue.
    '''

    # Calculate logrank pvalue
    logrank                             = logrank_test(group_1_months,
                                                       group_2_months,
                                                       group_1_status,
                                                       group_2_status)
    
    lgrank_rounded                      = round(float(logrank.p_value), 3)
    logrank_rounded_p_value :   str     = "{:e}".format(lgrank_rounded)

    # Formatted pvalue.
    logrank_p_value :           str     = "{:e}".format(logrank.p_value)

    return logrank_p_value


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



# Plotly counting Bar plot
# ---------------------------------------------------------------------
def plotly_counting_bar_plot(   entry_df:         pd.DataFrame, 
                                x_column_name:    str,
                                y_column_name:    str,
                                axis_range:       list[int])->str:
    '''
    Create a bar plot for the entry dataframe. Used by global_stats()
    function.
    Use the entry value 'x_column_name' to set the categories
    for the plot x axis, and 'y_column_name' to set the values for
    the y axis.

    ## Parameters:
        - entry_df (pd.DataFrame): the dataframe to be analyzed.
        - x_column_name (str): name for the dataframe category that have 
        to be placed in the x axis.
        - y_column_name (str): name for the dataframe category that have 
        to be placed in the y axis.
        - axis_range (list[int]): range of values for the y axis.
        
    ## Return:
        bar_plot_div (str): bar plot embedden into a 'div' html tag.
    '''

    # print('before histogram')
    bar_fig:        Figure  = px.histogram( data_frame  = entry_df,
                                            x           = x_column_name,
                                            y           = y_column_name,
                                            title       = '',
                                            text_auto   = True,
                                            nbins       = 7)
    
    layout                  = go.Layout(margin=go.layout.Margin( t = 25,
                                                                 l = 0))
    bar_fig.layout          = layout

    bar_fig.update_xaxes(   tickangle           = 50)
    bar_fig.update_layout(  width               = 270,
                            height              = 220,
                            showlegend          = False,
                            xaxis_title         = '',
                            yaxis_title         = y_column_name,
                            yaxis_range         = axis_range,
                            bargap              = 0.1,
                            font                = dict(size = 12),
                            yaxis               = dict(showgrid = True),
                            xaxis               = dict(showgrid = False),
                            paper_bgcolor       = 'rgba(0,0,0,0)',
                            plot_bgcolor        = 'rgba(0,0,0,0)')
    
    bar_fig.update_traces(  marker_color        = 'rgb(178, 216, 236)', 
                            marker_line_color   = 'rgb(8,48,107)',
                            marker_line_width   = 1.5, 
                            opacity             = 0.6)
    
    

    bar_plot_div:   str     = plot(bar_fig, output_type="div", config={'displayModeBar': False})

    return bar_plot_div
