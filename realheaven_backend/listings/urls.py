from django.urls import path
from .views import PropertyListView, PropertyDetailView,PropertySearchView, chatbot_api,CustomerSignupView, CustomerLoginView

urlpatterns = [
    path("properties/", PropertyListView.as_view(), name="property-list"),
    path("properties/<int:id>/", PropertyDetailView.as_view(), name="property-detail"),
    path('properties/search/', PropertySearchView.as_view(), name='property-search'),
    path("chatbot/", chatbot_api, name="chatbot_api"),
    path('signup/', CustomerSignupView.as_view(), name='customer-signup'),
    path('login/', CustomerLoginView.as_view(), name='customer-login'),
]
