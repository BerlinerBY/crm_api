from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User
from . import permissions


@api_view(["GET"])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def get_info(request):
    if request.method == "GET":
        token_str = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token = AccessToken(token_str)
        user_id = token['user_id']
        queryset = User.objects.get(id=user_id)
        serializer = UserSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated and permissions.IsSuperuser])
def reg_employee(request):
    if request.method == 'POST':
        data = request.data | {"is_staff": True}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload = {
                'user_id': user.id,
                'username': user.email
            }
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated and permissions.IsStaff])
def reg_customer(request):
    if request.method == 'POST':
        data = request.data | {"is_staff": False}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload = {
                'user_id': user.id,
                'username': user.email
            }
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def get_employees(request):
    if request.method == 'GET':
        employees = User.objects.filter(is_staff=True, is_superuser=False)
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated and permissions.IsStaff])
def get_customers(request):
    if request.method == 'GET':
        employees = User.objects.filter(is_staff=False)
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)