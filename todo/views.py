from . models import Todo
from . serializers import TodoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


# Creating our Views
@swagger_auto_schema(methods=['POST'],request_body=TodoSerializer())
@api_view(['GET','POST'])
def todos(request):
    if request.method=='GET':
        all_todos = Todo.objects.all()
        serializer = TodoSerializer(all_todos, many=True)
        data = {
            "message":"success",
            "data":serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            data = {
                "message":"success",
                "data":serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            error = {
                "message":"failed",
                "error":serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
@swagger_auto_schema(methods=['PUT','DELETE'],request_body=TodoSerializer())    
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, todo_id):
    """
    Takes in todo id and returns the http response depending on the http method.
    
    Args:
    todo_id: Interger
    
    Allowed methods:
    GET- Get the details of a single user Todo
    PUT- Allows the user Todo to be edited
    DELETE- This logic deletes the user todo record from the database
    """
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        error = {
            "message":"failed",
            "error":f"Todo with id {todo_id} does not exist"
        } # prepare the response data
        return Response(error, status=status.HTTP_404_NOT_FOUND) # send the response
    
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        data = {
            "message": "Success",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data, partial=True) # Partial because we want to PATCH
        
        if serializer.is_valid():
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
            todo.delete()
            return Response({"message":"success"}, status=status.HTTP_204_NO_CONTENT)
        