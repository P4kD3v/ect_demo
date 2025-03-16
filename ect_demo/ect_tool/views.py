#   App Name:   Endometrial Cancer Tool (Demo)
#   Author:     Xavier Llobet Navàs
#   Content:    ECT (Demo) views
#
# - This file contains all the Django framework views for the 
#   Endometrial Cancer Tool (Demo).
#
# - The views are divided in different fields/sections:
#
#   - Home
#   - EC Tool
#   - Cite Us
#
# - Home site for a summary of the ECT purpose and the data used.
#
# - EC Tool (Demo), can plot with no need of statistical knowledge, Progression-Free
#   and Overall survival for some clinical categories.
#
# =====================================================================
# IMPORTS
# =====================================================================

from            django.shortcuts            import  render
import          pandas                          as  pd
from .  import  ut_constants                    as  cns
from .  import  ut_survival                     as  surv


# =====================================================================
# HOME FIELD VIEW
# =====================================================================

# Home view:
# ---------------------------------------------------------------------
def index(request):
    '''
    This function return the home view were to see a brief
    description of the Endometrial Cancer Tool (Demo) purpose.
    '''

    if request.method == 'GET':
        
        # Template context date
        context:    dict    = { 'title':    'Endometrial Cancer Tool (Demo)',
                                'field':    'home'}

        return render(request, 'ect_tool/base_home.html', context)
    
    if request.method == 'POST':

        # Template context date
        context:    dict    = { 'title':    'Endometrial Cancer Tool (Demo)',
                                'field':    'home'}

        return render(request, 'ect_tool/base_home.html', context)
    
# ---------------------------------------------------------------------
def ect(request):
    '''
    View to generate plots about Endometrial Cancer with TCGA data.
    '''

    if request.method == 'GET':

        # Template context date
        context:    dict    = { 'title':    'Endometrial Cancer Tool (Demo)',
                                'field':    'ect'}

        return render(request, 'ect_tool/base_ect.html', context)

    # New
    if request.method == 'POST':

        # Get input values
        mode:           str             = request.POST['survival_type']
        clinical_cat:   str             = request.POST['clinical_category']

        # Sorting the survival dataframe by the PFS
        df:             pd.DataFrame    = cns.SURVIVAL
        sorted_df:      pd.DataFrame    = df.sort_values(by=f'{mode}_months', ascending=True)

        # Entire category name:
        main_category:  str             = cns.CATEGORIES_DICT[clinical_cat]
                    
        # Molecular subtype categories:
        subtype_catgs:  list[str]       = cns.SURVIVAL_GROUPS[clinical_cat]
        
        # Template context data
        context:        dict            = surv.km_category_survival_helper( sorted_df, 
                                                                            mode,
                                                                            clinical_cat,
                                                                            main_category,
                                                                            subtype_catgs)
        
        context['title']                = 'Endometrial Cancer Tool (Demo)'
        context['field']                = 'ect'

        return render(request, 'ect_tool/base_ect.html', context)
    
# ---------------------------------------------------------------------
def cite_us(request):
    '''
    View that shows how to cite this web application.
    '''

    if request.method == 'GET':
        # Template context date
        context:    dict    = { 'title':    'Endometrial Cancer Tool (Demo)',
                                'field':    'cite_us'}

        return render(request, 'ect_tool/base_cite_us.html', context)

    if request.method == 'POST':
        # Template context date
        context:    dict    = { 'title':    'Endometrial Cancer Tool (Demo)',
                                'field':    'cite_us'}

        return render(request, 'ect_tool/base_cite_us.html', context)