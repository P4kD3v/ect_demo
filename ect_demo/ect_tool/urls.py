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

        # /ect_tool/ect/
        path(   'ect_tool/ect/',                    
                views.ect,                     
                name='ect'),

        # /ect_tool/cite_us/
        path(   'ect_tool/cite_us/',                    
                views.cite_us,                     
                name='cite_us'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)