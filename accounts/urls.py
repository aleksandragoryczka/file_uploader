from django.urls import include, path

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls'))
]
