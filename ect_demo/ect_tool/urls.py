#   App Name:   Endometrial Cancer Tool v5
#   Author:     Xavier Llobet Navàs
#   Content:    ECT urls
#
# - This file contains all the paths for Endometrial Cancer Tool
#   will use to serve the views:
#
# =====================================================================
# IMPORTS
# =====================================================================

from django.urls                import path, include
from django.conf                import settings
from django.conf.urls.static    import static
from .                          import views

# =====================================================================
# PATHS
# =====================================================================

app_name        = 'ect'
urlpatterns     = [
    
        path("accounts/", include("django.contrib.auth.urls")),
        
        # ex: /ect_tool/
        path(   '',                                    
                views.index,                        
                name='index'),
        path(   'ect_tool/',                             
                views.index,                        
                name='index'),

        # /ect_tool/help_guide/
        path(   'ect_tool/help_guide/',                    
                views.help_guide,                     
                name='help_guide'),

        # /ect_tool/overview/
        path(   'ect_tool/overview/',                    
                views.overview,                     
                name='overview'),

        # /ect_tool/overview_survival/
        path(   'ect_tool/overview_survival/',                         
                views.overview_survival,                  
                name='overview_survival'),

        # /ect_tool/clinical_subcategory/
        path(   'ect_tool/clinical_subcategory/',                         
                views.clinical_subcategory,                  
                name='clinical_subcategory'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)