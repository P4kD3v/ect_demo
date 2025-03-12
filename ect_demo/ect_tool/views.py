#   App Name:   Endometrial Cancer Tool v5
#   Author:     Xavier Llobet Navàs
#   Content:    ECT views
#
# - This file contains all the Django framework views for the 
#    Endometrial Cancer Tool (ECT).
#
# - The views are divided in different fields/sections:
#
#   - Admin
#   - Authentication
#   - Home
#   - Overview
#   - Genes
#   - Custom Panel
#   - Tools
#   - Other Apps
#
# - Not all the sections are available for all users. Not registered
#   users only can see Home an Overview fields. Registered users can 
#   also see Genes, Custom Plot and Other Apps sections. Admin users
#   can see everything said before, plus an admin site to manage
#   users and dataset update.
#
# - Admin and authentication sites cover the user management. Admin
#   site for user modification or user deletion.
#
# - Home site for a summary of the ECT purpose and the data used.
#
# - Overview, Genes and Custom Plot fields, are fields where the user
#   can play with forms to do different statistical analysis related
#   to Endometrial Cancer (EC), and get a result as a plot with no
#   need of statistical knowledge
#
# - Each function in this file is related to one view, that also is 
#   included as a path in the ECT url patterns from urls.py file.
#
# =====================================================================
# IMPORTS
# =====================================================================

from            django.shortcuts            import  render, redirect
from            copy                        import  deepcopy
import          pandas                          as  pd
from            pandas                      import  concat
from .  import  ut_constants                    as  cns
from .  import  plotly_survival_plots           as  sp
from .  import  ut_survival                     as  surv
from .  import  ut_survival_stats               as  ss
from .  import  ut_stats                        as  us
import          html


# =====================================================================
# HOME FIELD VIEW
# =====================================================================

# Home view:
# ---------------------------------------------------------------------
def index(request):
    '''
    This function return the home view hwere to see a brief
    description of the Endometrial Cancer Tool porpuse and 
    manage the post requests for search into the PubMed, NCBI,
    HGNC, Ensembl and TCGA databases, and redirect to this
    pages with the resulting search.
    '''

    # If POST request method:
    if request.method == 'POST':

        # If PubMed search:
        if 'pubmed_submit' in request.POST:

            search_word:    str     = request.POST["pubmed_input"]
            link:           str     = "https://pubmed.ncbi.nlm.nih.gov/?term="
            search_link:    str     = link+search_word

            return redirect(search_link)
        
        # If NCBI search:
        if 'ncbi_submit' in request.POST:

            search_word:    str     = request.POST["ncbi_input"]
            link:           str     = "https://www.ncbi.nlm.nih.gov/gene/?term="
            search_link:    str     = link+search_word

            return redirect(search_link)
        
        # If HGNC search:
        if 'hgnc_submit' in request.POST:

            search_word:    str     = request.POST["hgnc_input"]
            link:           str     = "https://www.genenames.org/tools/search/#!/?query="
            search_link:    str     = link+search_word

            return redirect(search_link)
        
        # If Ensembl search:
        if 'ensembl_submit' in request.POST:

            search_word:    str     = request.POST["ensembl_input"]
            link:           str     = f"https://www.ensembl.org/Human/Search/Results?q={search_word};site=ensembl;facet_species=Human;page=1"

            return redirect(link)
        
        # If TCGA search:
        if 'tcga_submit' in request.POST:

            search_word:    str     = request.POST["tcga_input"]
            link:           str     = "https://portal.gdc.cancer.gov/genes/"
            search_link:    str     = link+search_word

            return redirect(search_link)
        
        # If TCGA search:
        if 'uniprot' in request.POST:

            # Has to be an Accession 
            search_word:    str     = request.POST["uniprot"]
            link:           str     = "https://rest.uniprot.org/uniprotkb/search?format=fasta&includeIsoform=true&query=accession%3A"
            search_link:    str     = link+search_word

            return redirect(search_link)       
    
    # If GET request method:
    else:

        context:            dict    = {'title':   'Home',
                                       'type':    'home'}

        return render(request, 'ect_tool/base_home.html', context)
    

# =====================================================================
# OVERVIEW FIELD VIEWS
# =====================================================================

# Overview view:
# ---------------------------------------------------------------------
def overview(request):
    '''
    This function return the overview view and its dorms for survival
    and infiltration analysis
    Also return a brief description of the field, and two 
    plots as a summary of the ECT data used in that field.
    '''

    # If GET request method:
    if request.method == 'GET':

        # Template context variables
        context:                dict            = { 'title':            'Overview',
                                                    'type':             'survival'}

        return render(request, 'ect_tool/base_overview.html', context)


# Overview Survival
# ---------------------------------------------------------------------
def overview_survival(request):
    '''
    This function return the progression-free survival overview
    with the plots of the field selected previously in the
    overview survival form.
    '''

    # Sorting the survival dataframe by the PFS
    sorted_survival_df:    pd.DataFrame         = cns.SURVIVAL.sort_values(by='pfs_months', ascending=True)

    # If POST request method:
    if request.method == 'POST':            
        try:
            # If if 'show' in POST request keys:
            if 'show' in request.POST:                
                # Set mode:
                mode:               str         = request.POST['survival_type']
                clinical_category:  str         = request.POST['clinical_category']

                # For Kaplan-Meier PFS Survival for entire dataset entries, with no care to clinical data
                if clinical_category == 'all':

                    context:        dict        = surv.km_all_survival_helper(sorted_survival_df, mode)

                    return render(request, 'ect_tool/base_overview_survival_all.html', context)  
                                               
                # For Kaplan-Meier PFS Survival for single clinical category       
                else:
                    
                    # Entire category name:
                    main_category:  str         = cns.CATEGORIES_DICT[clinical_category]
                    
                    # Molecular subtype categories:
                    subtype_catgs:  list[str]   = cns.SURVIVAL_GROUPS[clinical_category]
                    
                    context:        dict        = surv.km_category_survival_helper( sorted_survival_df, 
                                                                                    mode,
                                                                                    clinical_category,
                                                                                    main_category,
                                                                                    subtype_catgs,
                                                                                    clinical_category)

                    return render(request, 'ect_tool/base_overview_survival_category.html', context)
                            
        except Exception as ex:
            print(type(ex))    # the exception type
            print(ex.args)     # arguments stored in .args
            print(ex)
                
            return render(request, 'ect_tool/base_overview_survival.html')
    
    # If GET request method:    
    else:
        return render(request, 'ect_tool/base_overview_survival.html')
    


#  Clinical subcategory statistics view:
# ---------------------------------------------------------------------
def clinical_subcategory(request):
    '''
    This function return a survival analysis related to the clinical 
    subcataegory selected. Te analysis will be done for the rest of
    categories.
    For example, if Grade-1 is the selected subcategory, the analysis
    will be done for all the clinical categories except Grade.
    '''

    clinical_category:          str         = request.POST['category']
    target_categories:          list[str]   = [ 'grade',
                                                'tumor_type',
                                                'mol_subtype',
                                                'stage',
                                                'bmi_status',
                                                'radiotherapy',
                                                'age_group']
    target_categories.remove(clinical_category)
    subcategories_dict:         dict        = cns.CAT_AND_SUBCAT[clinical_category]
    context:                    dict        = {}
    # If POST request
    if request.method == 'POST':
        try:
            # Filtering if progresion or orverall survival:
            if 'pfs' in request.POST:               
                subcategory:    str         = request.POST['pfs']
                mode:           str         = 'pfs'
            if 'os' in request.POST:
                print('In os')
                subcategory:    str         = request.POST['os']
                mode:           str         = 'os'
            
            # Filter dadataframe
            subcategory_df:     pd.DataFrame= cns.SURVIVAL.loc[cns.SURVIVAL[clinical_category] == subcategory]

            # Create all the template context variables
            context:            dict        = ss.survival_statistics_generator( subcategory_df, 
                                                                                mode, 
                                                                                clinical_category, 
                                                                                subcategory, 
                                                                                subcategories_dict,
                                                                                target_categories)
            context['clinical_category']    = clinical_category
            context['type']                 = 'category_statistics'
            context['subcategories']        = cns.SURVIVAL_GROUPS[clinical_category]
            context['category_title']       = cns.CATEGORIES_DICT[clinical_category]
            context['subcategory_title']    = cns.CAT_AND_SUBCAT[clinical_category][subcategory]
            context['survival_mode_title']  = cns.SURVIVAL_MODES[mode]

            return render(request, 'ect_v5/base_overview_survival_category_stats.html', context)
                
        except Exception as ex:
            print(type(ex))    # the exception type
            print(ex.args)     # arguments stored in .args
            print(ex)               

            return render(request, 'ect_v5/base_overview_survival_category_stats.html')
        
    # If GET request
    else:

        return render(request, 'ect_v5/base_overview_survival_category_stats.html', context)

# =====================================================================
# HELP FIELD VIEW
# =====================================================================

# Help view:
# ---------------------------------------------------------------------
def help_guide(request):
    '''
    This function returns an andministrator and user guide.
    '''
    # If GET request method:
    if request.method == 'GET':

        context:            dict    = {'title':   'ECT Guide',
                                       'type':    'help_guide'}

        return render(request, 'ect_tool/base_help.html', context)
