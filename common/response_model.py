from rest_framework import serializers, viewsets

class CustomResponse(serializers.Serializer):
    code = serializers.IntegerField(default=400)
    response = serializers.BooleanField(default=False)
    data = serializers.DictField(default=None, allow_null=True)
    messages = serializers.ListField(default=None, allow_null=True)