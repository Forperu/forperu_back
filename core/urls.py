from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from core.api_urls import api_urlpatterns

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include("apps.users.urls")),
  # path('api/', include(api_urlpatterns)),
  path('api/', include("apps.companies.urls")),
  path('api/', include("apps.products.urls")),
  path('api/', include("apps.roles.urls")),
  path('api/', include("apps.branch_offices.urls")),
  path('api/', include("apps.brands.urls")),
  path('api/', include("apps.categories.urls")),
  path('api/', include("apps.units_of_measurement.urls")),
  path('api/', include("apps.warehouses.urls")),
  path('api/', include("apps.customers.urls")),
  path('api/', include("apps.suppliers.urls")),
  path('api/', include("apps.employees.urls")),
  path('api/', include("apps.job_positions.urls")),
  path('api/', include("apps.currencies.urls")),
  path('api/', include("apps.work_areas.urls")),
  path('api/', include("apps.exchange_rates.urls")),
  path('api/', include("apps.payment_methods.urls")),
  path('api/', include("apps.attendance_types.urls")),
  path('api/', include("apps.attendances.urls")),
  path('api/', include("apps.absence_types.urls")),
  path('api/', include("apps.absence_requests.urls")),
  path('api/', include("apps.vacations.urls")),
  path('api/', include("apps.vacation_balances.urls")),
  path('api/', include("apps.work_schedules.urls")),
  path('api/', include("apps.schedule_details.urls")),
  path('api/', include("apps.employee_schedules.urls")),
  path('api/', include("apps.holidays.urls")),
  path('api/', include("apps.overtime_requests.urls")),
  path('api/', include("apps.payrolls.urls")),
  path('api/', include("apps.employee_benefits.urls")),
  path('api/', include("apps.performance_reviews.urls")),
  path('api/', include("apps.employee_incidents.urls")),
  path('api/', include("apps.prices.urls")),
  path('api/', include("apps.quotes.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)