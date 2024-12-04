from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'drugs'
handler404 = 'djangoProject.views.page_not_found'


urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='index'),
    path('admin/', admin.site.urls),
    path('drugs/create/', views.create_drug, name='create_drug'),
    path('drugs/<str:drug_id>/update/', views.update_drug, name='update_drug'),
    path('drugs/<str:drug_id>/delete/', views.delete_drug, name='delete_drug'),
    path('drugs/<str:drug_id>/', views.get_drug, name='get_drug'),
    path('drugs/', views.get_drugs, name='get_drugs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
