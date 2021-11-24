from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password, check_password
from . serializers import CustomUserSerializer, ChangePasswordSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer())
@api_view(['GET','POST'])
def users(request):
    if request.method == 'GET':
        all_users = User.objects.filter(is_active=True)
        serializer = CustomUserSerializer(all_users, many=True)
        data = {
            "message":"success",
            "data":serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(
                                        serializer.validated_data['password']) # Hashing Password
            user = User.objects.create(**serializer.validated_data) # Unpacking validated_date
            
            user_serializer = CustomUserSerializer(user)
            data = {
                "message":"success",
                "data":user_serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            error = {
                "message":"failed",
                "error":serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
       
@swagger_auto_schema(methods=['PUT','DELETE'], request_body=CustomUserSerializer())    
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    """
    Takes in user id and returns the http response depending on the http method.
    
    Args:
    user_id: Interger
    
    Allowed methods:
    GET- Get the details of a single user
    PUT- Allows the user details to be edited
    DELETE- This logic deletes the user record from the database
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        error = {
            "message":"failed",
            "error":f"User with id {user_id} does not exist"
        } # prepare the response data
        return Response(error, status=status.HTTP_404_NOT_FOUND) # send the response
    
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        data = {
            "message": "Success",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data, partial=True) # Partial because we want to PATCH
        
        if serializer.is_valid():
            if 'password' in serializer.validated_data.keys():
                raise ValidationError("Unable to change password")
            serializer.save()
            data = {
                "message":"success",
                "data":serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            error = {
                "message":"failed",
                "errors":serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == "DELETE":
            user.delete()
            return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        
@swagger_auto_schema(methods=['POST'], request_body=LoginSerializer())
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                if user.is_active:
                    serializer = CustomUserSerializer(user)
                    data = {
                        "message":"Login Successful",
                        "data":serializer.data
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    error = {
                        "message":"Please activate your account",
                    }
            
                    return Response(error, status=status.HTTP_401_UNAUTHORIZED) 
            else:
                error = {
                        "errors":serializer.errors
                    }
            
                return Response(error, status=status.HTTP_401_UNAUTHORIZED)
 
        
@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if check_password(old_password, user.password):
                user.set_password(serializer.validated_data['new_password']) # sets and hashes the new password
                user.save()
                return Response({"message":"success"}, status=status.HTTP_200_OK)
            else:
                error = {
                'message':'failed',
                "errors":"Old password not correct"
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST)   
        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 
        