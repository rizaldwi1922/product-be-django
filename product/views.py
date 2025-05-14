from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, AddToCartSerializer
# Create your views here.


class ProductListView(APIView):
    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

class CartView(APIView):
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['productId']
            quantity = serializer.validated_data['quantity']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=404)

            cart = request.session.get('cart', {})
            product_key = str(product_id)

            if product_key in cart:
                cart[product_key]['quantity'] += quantity
            else:
                cart[product_key] = {
                    "id": product_id,
                    "product": product.name,
                    "quantity": quantity
                }

            request.session['cart'] = cart
            request.session.modified = True
            return Response(cart, status=201)

        return Response(serializer.errors, status=400)