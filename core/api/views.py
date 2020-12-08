# ViewSets define the view behavior.
from rest_framework import viewsets

from core.api.serializers import ProductSerializer
from core.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer