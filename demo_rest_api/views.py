
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo
data_list.append({'id': str(uuid.uuid4()), 'name': 'User04', 'email': 'user04@example.com', 'is_active': True})

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        return Response(data_list, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def get_object(self, item_id):
        for item in data_list:
            if item.get('id') == item_id:
                return item
        return None

    def put(self, request, item_id):
        data = request.data

        if 'id' not in data:
            return Response({'error': 'El campo id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        if data['id'] != item_id:
            return Response({'error': 'El identificador de la URL y el cuerpo deben coincidir.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos: name y email.'}, status=status.HTTP_400_BAD_REQUEST)

        item = self.get_object(item_id)
        if item is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item.clear()
        item['id'] = item_id
        item['name'] = data['name']
        item['email'] = data['email']
        item['is_active'] = data.get('is_active', item.get('is_active', True))

        return Response({'message': 'Elemento reemplazado correctamente.', 'data': item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        data = request.data

        item = self.get_object(item_id)
        if item is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if 'id' in data and data['id'] != item_id:
            return Response({'error': 'No se puede modificar el identificador.'}, status=status.HTTP_400_BAD_REQUEST)

        for field in ['name', 'email', 'is_active']:
            if field in data:
                item[field] = data[field]

        return Response({'message': 'Elemento actualizado correctamente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = self.get_object(item_id)
        if item is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False
        return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)
