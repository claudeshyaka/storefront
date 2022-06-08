from django.urls import path, include

from store import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/<slug:collection_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
]