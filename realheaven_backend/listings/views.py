from django.shortcuts import render
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .real_estate_chatbot import extract_query_details, search_properties, format_chatbot_response


logger = logging.getLogger(__name__)

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_query = data.get("query", "").strip()

            if not user_query:
                return JsonResponse({"error": "No query provided"}, status=400)

            filters = extract_query_details(user_query)

            # If the response is a chatbot message (not property search)
            if "message" in filters:
                return JsonResponse(filters, status=200)
           
            response = search_properties(filters)
            
            if not response:
                logger.warning(f"No properties found for query: {user_query}")
                return JsonResponse({"message": "No properties match your search. Try refining your query."}, status=200)
            
            
            formatted_response = format_chatbot_response(filters, response.get("properties", []), response.get("message"))
            print("Final API response: ", formatted_response)
            return JsonResponse(formatted_response, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received in chatbot API.")
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            logger.exception(f"Unexpected error in chatbot API: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    elif request.method == "GET":
        # Example test query
        example_query = "Show me houses with 5 bedrooms in San Jose under $3,000,000."
        filters = extract_query_details(example_query)
        return JsonResponse({"filters": filters}, status=200)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = "id"

class PropertySearchView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        # Start with all properties
        queryset = Property.objects.all()

        # Get the query parameters from the request
        street_address = self.request.query_params.get('street_address', None)
        zip_code = self.request.query_params.get('zip_code', None)
        property_type = self.request.query_params.get('property_type', None)

        # Filter based on the provided parameters
        if street_address:
            queryset = queryset.filter(street_address__icontains=street_address)  # Case-insensitive address search
        if zip_code:
            queryset = queryset.filter(zip_code=str(zip_code))  # Exact match for zip code
        if property_type:
            queryset = queryset.filter(property_type__iexact=property_type)  # Case-insensitive exact match for property type

        return queryset
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
from django.contrib.auth.hashers import check_password

class CustomerSignupView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)


class PropertyListingTypeView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        listing_type = self.request.query_params.get('listing_type')
        if listing_type:
            return Property.objects.filter(listing_type__iexact=listing_type)
        return Property.objects.all()