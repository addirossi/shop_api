from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.models import Product
from main.serializers import ProductSerializer


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
