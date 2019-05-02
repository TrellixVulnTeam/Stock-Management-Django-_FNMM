"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from product import views

urlpatterns = [
    path('', views.w_index, name="w_index"),
    path('about/', views.w_about, name="w_about"),
    path('facebook/', RedirectView.as_view(url='http://facebook.com'), name="facebook"),
    path('instagram/', RedirectView.as_view(url='http://instagram.com'), name="instagram"),
    path('linkdn/', RedirectView.as_view(url='https://www.linkedin.com/in/atrai-group-a5519174/'), name="linkdn"),
    path('projects/', views.w_projects, name="w_projects"),
    path('contact/', views.w_contact, name="w_contact"),
    path('show_products/', views.w_products, name="w_products"),
    path('machineries/', views.w_machineries, name="w_machineries"),
    path('software/', views.index, name="software"),
    path('pdf/', views.pdf, name="pdf"),
    path('logout_success/', views.logout_success, name="logout_success"),
    path('add_product/', views.products, name="products"),
    path('history/', views.history, name="history"),
    path('edit_product_success/', views.edit_products_success, name="edit_products"),
    path('purchase_product_success/', views.purchase_products_success, name="purchase_products"),
    path('edit_member_success/', views.edit_member_success, name="edit_member"),
    path('edit_supplier_success/', views.edit_supplier_success, name="edit_supplier"),
    path('update_product/', views.update_product, name="update_product"),
    path('supplier_payment/', views.supplier_payment, name="supplier_payment"),
    path('product_list/', views.product_list, name="product_list"),
    path('add_member/', views.add_member, name="add_member"),
    path('add_supplier/', views.add_supplier, name="add_supplier"),
    path('team_list/', views.team_list, name="team_list"),
    path('supplier_team_list/', views.supplier_team_list, name="supplier_team_list"),
    url(r'^member_list/(?P<id>\w{0,50})/$', views.member_list),
    url(r'^supplier_list/(?P<id>\w{0,50})/$', views.supplier_list),
    url(r'^changes/(?P<id>\w{0,50})/$', views.show_changes),
    url(r'^delete_product/(?P<id>\w{0,50})/$', views.delete_product),
    url(r'^delete_member/(?P<id>\w{0,50})/$', views.delete_member),
    url(r'^delete_supplier/(?P<id>\w{0,50})/$', views.delete_supplier),
    url(r'^full_pay/(?P<id>\w{0,50})/$', views.full_pay_supplier_success),
    url(r'^edit_product/(?P<id>\w{0,50})/$', views.edit_product),
    url(r'^purchase_product/(?P<id>\w{0,50})/$', views.purchase_product),
    url(r'^edit_member/(?P<id>\w{0,50})/$', views.edit_member),
    url(r'^edit_supplier/(?P<id>\w{0,50})/$', views.edit_supplier),
    url(r'^pay_supplier/(?P<id>\w{0,50})/$', views.pay_supplier),
]
