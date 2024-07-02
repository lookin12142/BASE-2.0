
from rest_framework import serializers
from .models import Category, Product, Customer, Order, OrderItem, Mascota, EmergencyHistory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'



class EmergencyHistorySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    mascota = MascotaSerializer()

    class Meta:
        model = EmergencyHistory
        fields = '__all__'