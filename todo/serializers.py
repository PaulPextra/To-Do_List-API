from rest_framework import serializers
from . models import Todo

class TodoSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = ('id', 'user','username', 'title', 'body', 'date', 'time', 'completed', 'created_at',)
        
class FutureSerializer(serializers.Serializer):
    date = serializers.DateField()
        