import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.payment_methods.models import PaymentMethod
from apps.payment_methods.serializers import PaymentMethodSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class PaymentMethodAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una método de pago
      paymentMethod = get_object_or_404(PaymentMethod, pk=pk, deleted_at__isnull=True)
      serializer = PaymentMethodSerializer(paymentMethod)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de métodos de pago
    paymentMethods = PaymentMethod.objects.filter(deleted_at__isnull=True)
    serializer = PaymentMethodSerializer(paymentMethods, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva método de pago
    serializer = PaymentMethodSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    paymentMethod = get_object_or_404(PaymentMethod, pk=pk, deleted_at__isnull=True)
    serializer = PaymentMethodSerializer(paymentMethod, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    paymentMethod = get_object_or_404(PaymentMethod, pk=pk, deleted_at__isnull=True)
    serializer = PaymentMethodSerializer(paymentMethod, data=request.data, partial=True)
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
      paymentMethod = get_object_or_404(PaymentMethod, pk=pk, deleted_at__isnull=True)
      paymentMethod.deleted_at = timezone.now()
      paymentMethod.updated_by = request.user
      paymentMethod.save()
      return Response(
        {'message': 'PaymentMethod deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      paymentMethod_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not paymentMethod_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de métodos de pago'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        paymentMethod_ids = [int(id) for id in paymentMethod_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de métodos de pago no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      jxisting_PaymentMethods = PaymentMethod.objects.filter(
        id__in=paymentMethod_ids,
        deleted_at__isnull=True
      )

      if jxisting_PaymentMethods.count() != len(paymentMethod_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = jxisting_PaymentMethods.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} métodos de pago eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar métodos de pago: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )