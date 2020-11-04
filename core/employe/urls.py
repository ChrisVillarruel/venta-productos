from django.urls import path
from core.employe.views.category.views import *
from core.employe.views.dashboard.views import *
from core.employe.views.product.views import *
from core.employe.views.client.views import *
from core.employe.views.test.views import *
from core.employe.views.sale.views import *

# -> Le colocamos un nombre a nuestro modulo urls para hacer referencia especificamente a estas url
app_name = 'erp'

urlpatterns = [
    # category
    path('category/list/', CategoryListView.as_view(), name='category-list'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/form/', CategoryFormView.as_view(), name='category-form'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # product
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    # clients
    path('client/', ClientView.as_view(), name='client'),
    # tests
    path('test/', TestView.as_view(), name='test'),
    # sales
    path('sale/create', SaleCreateView.as_view(), name='create-sale')
]
