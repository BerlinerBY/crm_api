from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from .models import Task
import sys
sys.path.append("..")
from accounts.models import User
from . import permissions
from django.forms.models import model_to_dict


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    if request.method == 'POST':
        token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = AccessToken(token_str)
        user_id = token['user_id']
        req_user = User.objects.get(id=user_id)
        user_role = req_user.is_staff

        data = request.data
        data["employee"] = 1
        if user_role == False:
            data["customer"] = User.objects.get(id=user_id).id
        else:
            data["customer"] = User.objects.get(id=data["customer"]).id

        serializer = TaskSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
                {"error": "You must be authenticated to create a collection."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def read_tasks(request):
    if request.method == 'GET':
        token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = AccessToken(token_str)
        user_id = token['user_id']
        req_user = User.objects.get(id=user_id)
        if req_user.is_superuser:
            # superuser can see all tasks
            tasks = Task.objects.filter()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        elif req_user.is_superuser == False and req_user.is_staff == True:
            # staff can see own and raw tasks
            tasks = Task.objects.filter(employee__in = (1, user_id))
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        elif req_user.is_superuser == False and req_user.is_staff == False:
            # customer can see only own tasks
            tasks = Task.objects.filter(customer=user_id)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  
        else:
            return Response(
                {'error': "You have not permission for it"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(
            {"error": "You must be authenticated to view your collections."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def read_task(request, task_id):
    if request.method == 'GET':
        token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = AccessToken(token_str)
        user_id = token['user_id']
        req_user = User.objects.get(id=user_id)
        if req_user.is_superuser:
            task = Task.objects.filter(id=task_id)
            serializer = TaskSerializer(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        elif req_user.is_superuser == False and req_user.is_staff == True:
            task = Task.objects.get(id=task_id)
            serializer = TaskSerializer(task)
            if serializer.data['employee'] == 1 or serializer.data['employee'] == user_id:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'tas': serializer.employee,
                }, status=status.HTTP_404_NOT_FOUND)
        elif req_user.is_superuser == False and req_user.is_staff == False:
            task = Task.objects.filter(
                customer=user_id,
                id=task_id)
            serializer = TaskSerializer(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  
        else:
            return Response(
                {'error': "You have not permission for it"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(
            {"error": "You must be authenticated to view your collections."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

# new_methods, which need tests
@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated and permissions.IsStaff])
def get_task(request, task_id):
    if request.method == 'POST':
        token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = AccessToken(token_str)
        user_id = token['user_id']
        req_user = User.objects.get(id=user_id)
        
        if req_user.is_superuser:
            return Response(
                {'error': "You have not permission for it"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            task = Task.objects.get(id=task_id)

            if model_to_dict(task)['employee'] == 1:
                data = model_to_dict(task)
                data['employee'] = user_id
                data['status'] = 1
                serializer = TaskSerializer(task, data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK) 
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {'error': "You have not permission for it"},
                    status=status.HTTP_400_BAD_REQUEST
                )


    return Response(
            {"error": "You must be authenticated to view your collections."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['PUT'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated and permissions.IsStaff])
def update_task(request, task_id):
    if request.method == 'PUT':
        token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = AccessToken(token_str)
        user_id = token['user_id']
        req_user = User.objects.get(id=user_id)

        if req_user.is_superuser == False:
            return Response(
                {'error': "You have not permission for it"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else: 
            task = Task.objects.get(
                employee=user_id,
                id=task_id
            )
            if model_to_dict(task)['status'] == 2:
                return Response(
                    {'error': "This task can't be updated, because they was close"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
            {"error": "You must be authenticated to view your collections."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['PUT'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated and permissions.IsStaff])
def close_task(request, task_id):
    if request.method == 'PUT':
        token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = AccessToken(token_str)
        user_id = token['user_id']
        req_user = User.objects.get(id=user_id)

        if req_user.is_superuser:
            return Response(
                {'error': "You have not permission for it"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            task = Task.objects.get(
                employee=user_id,
                id=task_id
            )
            serializer = TaskSerializer(task, data=(request.data | {'status':2}))
            if serializer.data['report'] == '':
                return Response(
                    {'error': "Task doesn't be closed with empty report"},
                    status=status.HTTP_409_CONFLICT # Check status
                )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK) 

    return Response(
            {"error": "You must be authenticated to view your collections."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )