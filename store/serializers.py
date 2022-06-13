from rest_framework import serializers

from .models import Collection, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "stock_unit",
            "sale_price",
            "purchase_price",
            "inventory",
            "absolute_url",
            "description",
            "product_image",
            "product_thumbnail",
        )

    