import csv
from django.http.response import HttpResponse
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from admin.pagination import CustomPagination
from users.authentication import JWTAuthentication
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderGenericAPIView(
        generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

    def post(self, request):
        return Response({
            'data': self.create(request).data
        })

    def put(self, request, pk=None):
        return Response({
            'data': self.partial_update(request, pk).data
        })

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class ExportAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'

        orders = Order.objects.all()
        writer = csv.writer(response)

        writer.writerow(
            ['ID', 'Name', 'Email', 'Product Title', 'Price', 'Quantity'])

        for order in orders:
            writer.writerow(
                [order.id, order.name, order.email, '', '', ''])

            orderItems = OrderItem.objects.all().filter(order_id=order.id)

            for item in orderItems:
                writer.writerow(
                    ['', '', '', item.product_title, item.price, item.quantity])

        return response
