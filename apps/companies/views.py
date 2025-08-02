import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class CompanyAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
      if pk:
          # Detalle de una compañía
          company = get_object_or_404(Company, pk=pk, deleted_at__isnull=True)
          serializer = CompanySerializer(company)
          return Response(serializer.data, status=status.HTTP_200_OK)
      
      # Listado de compañías
      companies = Company.objects.filter(deleted_at__isnull=True)
      serializer = CompanySerializer(companies, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
      # Creación de nueva compañía
      serializer = CompanySerializer(data=request.data)
      if serializer.is_valid():
          serializer.save(created_by=request.user)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
      # Actualización completa
      company = get_object_or_404(Company, pk=pk, deleted_at__isnull=True)
      serializer = CompanySerializer(company, data=request.data)
      if serializer.is_valid():
          serializer.save(updated_by=request.user)
          return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
      # Actualización parcial
      company = get_object_or_404(Company, pk=pk, deleted_at__isnull=True)
      serializer = CompanySerializer(company, data=request.data, partial=True)
      if serializer.is_valid():
          serializer.save(updated_by=request.user)
          return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
      if pk:
          # Eliminación individual (soft delete)
          company = get_object_or_404(Company, pk=pk, deleted_at__isnull=True)
          company.deleted_at = timezone.now()
          company.updated_by = request.user
          company.save()
          return Response(
              {'message': 'Company deleted successfully'}, 
              status=status.HTTP_204_NO_CONTENT
          )
      
      # Eliminación múltiple (opcional)
      return self._delete_multiple(request)

  def _delete_multiple(self, request):
      try:
          company_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])
          
          if not company_ids:
              return Response(
                  {'error': 'No se proporcionaron IDs de compañías'},
                  status=status.HTTP_400_BAD_REQUEST
              )

          try:
              company_ids = [int(id) for id in company_ids]
          except (ValueError, TypeError):
              return Response(
                  {'error': 'IDs de compañías no válidos'},
                  status=status.HTTP_400_BAD_REQUEST
              )

          existing_companies = Company.objects.filter(
              id__in=company_ids,
              deleted_at__isnull=True
          )

          if existing_companies.count() != len(company_ids):
              return Response(
                  {'error': 'Algunos IDs no existen o ya fueron eliminados'},
                  status=status.HTTP_400_BAD_REQUEST
              )

          updated = existing_companies.update(
              deleted_at=timezone.now(),
              updated_by=request.user
          )

          return Response({
              'message': f'{updated} compañías eliminadas exitosamente',
              'deleted_count': updated
          }, status=status.HTTP_200_OK)

      except Exception as e:
          traceback.print_exc()
          return Response(
              {'error': f'Error al eliminar compañías: {str(e)}'},
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )