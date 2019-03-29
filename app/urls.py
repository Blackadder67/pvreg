from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('contacts_search', views.contacts_search_view, name='contacts_search'),
    path('contacts', views.contacts_view, name='contacts'),
    path('department_contacts', views.department_contacts_view, name='department_contacts'),
    path('pv', views.pv_view, name='pv'),
    path('products', views.products_view, name='products'),
    path('product/<int:id>', views.product_details_view, name='product_detail'),
    path('psur', views.psur_view, name='psur'),
    path('ct', views.ct_view, name='ct'),
    path('reg', views.reg_view, name='reg'),
    path('adrs', views.adrs_view, name='adrs'),
]
