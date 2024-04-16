from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order, OrderItem, WarehouseItem


class OrderViews(APIView):
    def get(self, request):
        orders = Order.objects.all()
        return Response([{
                'id': order.id,
                'address': order.address,
                'created_at': order.created_at,
                'modified_at': order.modified_at,
            } for order in orders
        ])
    
    def post(self, request):
        address = request.data.get('address')
        order = Order.objects.create(
            address=address, created_at=datetime.now(), modified_at=datetime.now()
        )
        return Response({
            'id': order.id,
            'address': order.address,
            'created_at': order.created_at,
            'modified_at': order.modified_at,
        })


class OrderItemViews(APIView):
    def get(self, request):
        order_id = request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        return Response([{
                'id': order_item.id,
                'order_id': order.id,
                'product_id': order_item.product_id,
                'quantity': order_item.quantity,
                'price': order_item.price,
            } for order_item in order_items
        ])
    
    def post(self, request):
        order_id = request.query_params.get('order_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        price = request.data.get('price')
        order_item = OrderItem.objects.create(
            order_id=order_id, product_id=product_id, quantity=quantity, price=price
        )
        return Response({
            'id': order_item.id,
            'order_id': order_item.order_id,
            'product_id': order_item.product_id,
            'quantity': order_item.quantity,
            'price': order_item.price,
        })
    
    def patch(self, request):
        order_item_id = request.data.get('order_item_id')
        quantity = request.data.get('quantity')
        
        order_item = OrderItem.objects.filter(id=order_item_id)[0]
        
        warehouse_item_q = WarehouseItem.objects.all()
        warehouse_item_c = WarehouseItem.objects.count()
        warehouse_item = []
        for i in range(warehouse_item_c):
            warehouse_item.append(warehouse_item_q[i])
        
        j = 0
        while j < warehouse_item_c:
            if warehouse_item[j].product_id == order_item.product_id:
                warehouse_item[j].quantity -= quantity
                
                order_item.quantity = quantity
                order_item.price = warehouse_item[j].price * order_item.quantity
                
                # Do simultaneously
                order_item.save(), warehouse_item[j].save()
                
                return Response({
                    'id': order_item.id,
                    'order_id': order_item.order_id,
                    'product_id': order_item.product_id,
                    'quantity': order_item.quantity,
                    'price': order_item.price,
                })

            
            j += 1
        
        raise ValueError('Go buy in another store so much!')
        