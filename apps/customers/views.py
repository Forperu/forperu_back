import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class CustomerAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un cliente
      customer = get_object_or_404(Customer, pk=pk, deleted_at__isnull=True)
      serializer = CustomerSerializer(customer)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de clientes
    customers = Customer.objects.filter(deleted_at__isnull=True)
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nuevo cliente
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    customer = get_object_or_404(Customer, pk=pk, deleted_at__isnull=True)
    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    customer = get_object_or_404(Customer, pk=pk, deleted_at__isnull=True)
    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      customer = get_object_or_404(Customer, pk=pk, deleted_at__isnull=True)
      customer.deleted_at = timezone.now()
      customer.updated_by = request.user
      customer.save()
      return Response(
        {'message': 'Customer deleted successfully'},
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      customer_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not customer_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de clientes'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        customer_ids = [int(id) for id in customer_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_customers = Customer.objects.filter(
        id__in=customer_ids,
        deleted_at__isnull=True
      )

      if existing_customers.count() != len(customer_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_customers.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} clientes eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar clientes: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )