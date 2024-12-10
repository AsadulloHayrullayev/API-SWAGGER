from django.shortcuts import render
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

def index(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products' : products})


class HelloWorldAPIView(APIView):
    @swagger_auto_schema(
        operation_description= "A simple example endpoint",
        responses={200: openapi.Response("A response description")},
    )
    
    def get(self, request, *args, **kwargs):
        return Response({'message': "Hello world"})



class ProductListAPIView(APIView):
    @swagger_auto_schema(
        operation_description= "Get all product list",
        responses={200: ProductSerializer(many=True)},
    )
    
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer},
    )

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    