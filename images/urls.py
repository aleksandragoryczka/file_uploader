from django.urls import path

from images import views

urlpatterns = [
    path('', views.ListImageView.as_view(), name='images'),
    path('create/', views.CreateImageView.as_view(), name='create_image'),
    path('expiring-link/create/', views.CreateExpiringLinkView.as_view(), name='create_expiring_link'),
    path('expiring-link/<int:image_id>', views.ListExpiringLinkView.as_view(), name='expiring_link'),
]
