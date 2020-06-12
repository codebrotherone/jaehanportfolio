from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    # Home + Nav Bar Pages
    path('', views.PostList.as_view(), name='home'),
    path('posts/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('gallery', views.Gallery.as_view(), name='gallery'),
    path('about', views.ProfileList.as_view(), name='about'),
    path('projects', views.ComingSoonView.as_view(), name='projects'),
    # Data Science Stuff
    path('covid', views.CovidTimeSeries.as_view(), name='covid'),
    path('covid/folium', views.CovidFoliumView.as_view(), name='covid_folium'),
    path('covid/bokeh', views.CovidBokehView.as_view(), name='covid_bokeh'),
    # Notebooks
    path('notebooks', views.NotebooksHome.as_view(), name='notebooks'),
    path('notebooks/euler_11', views.ProjectEuler11.as_view(), name='euler_11'),
    path('notebooks/euler_14', views.ProjectEuler14.as_view(), name='euler_14'),
    # Placeholders
    path('coming/soon', views.ComingSoonView.as_view(), name='coming_soon')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
