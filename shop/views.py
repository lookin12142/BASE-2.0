# shop/views.py

from rest_framework import viewsets , generics
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound
from .models import Category, Product, Customer, Order, OrderItem, Mascota, EmergencyHistory
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer, MascotaSerializer, EmergencyHistorySerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

import json

# ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
    


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EmergencyHistoryListCreate(generics.ListCreateAPIView):
    queryset = EmergencyHistory.objects.all()
    serializer_class = EmergencyHistorySerializer

    def perform_create(self, serializer):
        try:
            customer = Customer.objects.get(id=self.request.data['customer_id'])
            mascota = Mascota.objects.get(id=self.request.data['mascota_id'])
        except Customer.DoesNotExist:
            raise NotFound('Customer not found.')
        except Mascota.DoesNotExist:
            raise NotFound('Mascota not found.')
        
        serializer.save(customer=customer, mascota=mascota)

class EmergencyHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyHistory.objects.all()
    serializer_class = EmergencyHistorySerializer


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_email = data['email']
            items = data['items']

            # Obtener o crear el cliente
            customer, created = Customer.objects.get_or_create(
                email=customer_email, defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'address': data['address'],
                }
            )

            # Crear la orden
            order = Order.objects.create(customer=customer, paid=True)

            # Crear los items de la orden
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order, product=product, quantity=item['quantity'], price=product.price
                )

            # Enviar el recibo por correo
            send_mail(
                'Recibo de tu compra',
                f'Gracias por tu compra. Tu número de orden es {order.id}.',
                settings.DEFAULT_FROM_EMAIL,
                [customer_email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Orden creada y recibo enviado'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
