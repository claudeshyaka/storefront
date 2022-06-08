from rest_framework import serializers

from .models import Collection, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "absolute_url",
            "description",
            "price",
            "product_image",
            "product_thumbnail",
        )

    