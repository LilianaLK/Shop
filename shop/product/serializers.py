import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


from .models import Product


# class ProductModel:
#     def __init__(self, name, content):
#         self.name = name
#         self.content = content

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=("name","cost","articul","weight","material", "description", "cat", "slug", "time_create", "time_update")

# class ProductDetailSerializer(serializers.ModelSerializer):
#     pk_name = serializers.SerializerMethodField()
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#         def get_pk_name(self, obj):
#             return f'{obj.pk.name}'


    # name = serializers.CharField(max_length=255)
    # cost = serializers.IntegerField()
    # articul = serializers.IntegerField()
    # weight = serializers.FloatField()
    # material = serializers.CharField(max_length=100)
    # description = serializers.CharField()
    # time_create = serializers.DateTimeField(read_only=True)
    # time_update = serializers.DateTimeField(read_only=True)
    # is_published = serializers.BooleanField(default=True)
    # cat_id = serializers.IntegerField()


# def encode():
#     model = ProductModel('ring', 'Content:bestring')
#     model_sr = ProductSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"name":"ring","content":"Musk"}')
#     data = JSONParser().parse(stream)
#     serializer = ProductSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)


