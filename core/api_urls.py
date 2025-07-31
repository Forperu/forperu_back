from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.branch_offices.views import BranchOfficeViewSet
from apps.brands.views import BrandViewSet
from apps.categories.views import CategoryViewSet
from apps.companies.views import CompanyViewSet
from apps.currencies.views import CurrencyViewSet
from apps.customers.views import CustomerViewSet
from apps.employees.views import EmployeeViewSet
from apps.exchange_rates.views import ExchangeRateViewSet
from apps.job_positions.views import JobPositionViewSet
from apps.payment_methods.views import PaymentMethodViewSet
from apps.products.views import ProductViewSet
from apps.roles.views import RoleViewSet
from apps.suppliers.views import SupplierViewSet
from apps.units_of_measurement.views import UnitOfMeasurementViewSet
from apps.warehouses.views import WarehouseViewSet
from apps.work_areas.views import WorkAreaViewSet

router = DefaultRouter()
router.register(r'branch-offices', BranchOfficeViewSet, basename='branch-offices')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'currencies', CurrencyViewSet, basename='currencies')
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'exchange-rates', ExchangeRateViewSet, basename='exchange-rates')
router.register(r'job-positions', JobPositionViewSet, basename='job-positions')
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-methods')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'units-of-measurement', UnitOfMeasurementViewSet, basename='units-of-measurement')
router.register(r'warehouses', WarehouseViewSet, basename='warehouses')
router.register(r'work-areas', WorkAreaViewSet, basename='work-areas')

api_urlpatterns = [
  path('', include(router.urls)),
]