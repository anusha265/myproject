from django.urls import include, path
from pdfreorder.views import reorder_pdf

urlpatterns = [
    # Other URLs...
    path('', reorder_pdf, name='reorder_pdf'),
    path('pdfreorder/', include('pdfreorder.urls')),
]
