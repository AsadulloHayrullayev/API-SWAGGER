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
    
    @swagger_auto_schema(
        operation_description="Delete a product by ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="ID of the product to delete",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={204: "Product deleted successfully", 404: "Product not found"},
    )

    def delete(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_description="Update a product by ID",
        request_body=ProductSerializer,
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="ID of the product to update",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: ProductSerializer, 404: "Product not found"},
    )
    
    def put(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)