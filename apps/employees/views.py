import json
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class EmployeeAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un empleado
      employee = get_object_or_404(Employee, pk=pk, deleted_at__isnull=True)
      serializer = EmployeeSerializer(employee)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de empleados
    employees = Employee.objects.filter(deleted_at__isnull=True)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    try:
      data = request.data.dict()  # Para leer campos simples del formData
      files = request.FILES

      serializer = EmployeeSerializer(data=data)
      if serializer.is_valid():
        employee = serializer.save()

        # Procesar documentos nuevos
        for key, uploaded_file in files.items():
          if key.startswith("document_"):
            employee.add_uploaded_file(uploaded_file)

        employee.save()
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      traceback.print_exc()
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def put(self, request, pk, format=None):
    employee = get_object_or_404(Employee, pk=pk, deleted_at__isnull=True)
    data = request.data.dict()
    files = request.FILES

    serializer = EmployeeSerializer(employee, data=data, partial=True)
    if serializer.is_valid():
      employee = serializer.save(updated_at=timezone.now())

      # Eliminar documentos si vienen marcados
      documents_to_delete = request.data.get("documents_to_delete")
      if documents_to_delete:
        import json
        try:
          ids = json.loads(documents_to_delete)
          for doc_id in ids:
            employee.remove_document(doc_id)
        except Exception:
          pass

      # Agregar documentos nuevos
      for key, uploaded_file in files.items():
        if key.startswith("document_"):
          employee.add_uploaded_file(uploaded_file)

      employee.save()
      return Response(EmployeeSerializer(employee).data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    employee = get_object_or_404(Employee, pk=pk, deleted_at__isnull=True)
    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      employee = get_object_or_404(Employee, pk=pk, deleted_at__isnull=True)
      employee.deleted_at = timezone.now()
      employee.save()
      return Response(
        {'message': 'Employee deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      employee_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not employee_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de empleados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        employee_ids = [int(id) for id in employee_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_employees = Employee.objects.filter(
        id__in=employee_ids,
        deleted_at__isnull=True
      )

      if existing_employees.count() != len(employee_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_employees.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} empleados eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar empleados: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )