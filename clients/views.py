from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

@api_view(['GET', 'POST'])
def list_or_create_clients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        return Response(ClientSerializer(clients, many=True).data)

    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def client_detail_or_update_or_delete(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'GET':
        client_data = ClientSerializer(client).data
        client_data['projects'] = ProjectSerializer(client.projects.all(), many=True).data
        return Response(client_data)

    if request.method in ['PUT', 'PATCH']:
        serializer = ClientSerializer(client, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save(updated_at=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    client.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_project(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    user_ids = [u['id'] for u in request.data.get('users', [])]
    users = User.objects.filter(id__in=user_ids)

    if users.count() != len(user_ids):
        return Response({'detail': 'Some users not found'}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'project_name': request.data.get('project_name'),
        'client': client.id,
        'created_by': request.user.id,
        'users': user_ids,
    }

    serializer = ProjectSerializer(data=data)
    if serializer.is_valid():
        project = serializer.save()
        return Response({
            'id': project.id,
            'project_name': project.project_name,
            'client': client.client_name,
            'users': [{'id': u.id, 'name': u.username} for u in project.users.all()],
            'created_at': project.created_at.isoformat(),
            'created_by': project.created_by.username,
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_projects(request):
    projects = request.user.projects.all()
    data = [
        {
            'id': p.id,
            'project_name': p.project_name,
            'created_at': p.created_at.isoformat(),
            'created_by': p.created_by.username,
        }
        for p in projects
    ]
    return Response(data)
