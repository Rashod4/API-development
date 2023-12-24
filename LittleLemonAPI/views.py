from django.shortcuts import render, get_list_or_404
from django.core import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, throttle_classes, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import MenuItem, OrderItem, Category, Cart, Order
from rest_framework import generics, status, permissions
from django.contrib.auth.models import User, Group
from .permissions import IsManager, IsDeliveryCrew
from .serializers import UserSerializer, MenuItemSerializer

# Displays only the current user
@api_view(['GET'])
def return_user(request):
    return Response({'username': request.user.username, 'email': request.user.email})


# User group management endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsManager])
def get_managers(request):
    manager_group = Group.objects.get(name="Manager")
    if request.method == "GET":
        # Returns all managers
        managers = manager_group.user_set.all()
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # Assigns the user in the payload to the manager group and returns 201-Created
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager_group.user_set.add(user)
            return Response({"message": "Added Manager"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Error must be either GET or POST request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsManager])
def remove_manager(request, userId):
    if request.method == "DELETE":
        # Removes this particular user from the manager group and returns 200 – Success if everything is okay.
        # If the user is not found, returns 404 – Not found
        user = get_object_or_404(User, pk=userId)
        manager_group = Group.objects.get(name="Manager")
        manager_group.user_set.remove(user)
        return Response({"message": f"Removed Manager {user}"}, status=status.HTTP_200_OK)
    return Response({"message": f"Could not find User"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsManager])
def get_delivery_crew(request):
    delivery_group = Group.objects.get(name="Delivery Crew")
    if request.method == "GET":
        # Returns all delivery crew
        delivery = delivery_group.user_set.all()
        serializer = UserSerializer(delivery, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # Assigns the user in the payload to delivery crew group and returns 201-Created HTTP
        username = request.data["username"]
        user = get_object_or_404(User, username=username)
        delivery_group.user_set.add(user)
        return Response({"message": "Added Delivery Crew Member"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsManager])
def remove_delivery_crew(request, userId):
    if request.method == "DELETE":
        # Removes this user from the manager group and returns 200 – Success if everything is okay.
        # If the user is not found, returns  404 – Not found
        user = get_object_or_404(User, pk=userId)
        delivery_group = Group.objects.get(name="Delivery Crew")
        delivery_group.user_set.remove(user)
        return Response({"message": f"Removed Delivery Crew Member {user}"}, status=status.HTTP_200_OK)
    return Response({"message": f"Could not find User"}, status=status.HTTP_404_NOT_FOUND)


# Menu-items endpoints

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])  # Use TokenAuthentication to ensure only managers can make changes
def get_post_menu_items(request):
    if request.method == "GET":
        # Lists all menu items. Return a 200 – Ok HTTP status code
        queryset = get_list_or_404(MenuItem)
        serializer = MenuItemSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method != "GET" and request.method == "POST":
        # Creates a new menu item and returns 201 - Created
        user = request.user
        if user.groups.filter(name="Manager").exists():
            title = request.data['title']
            title_in_database = MenuItem.objects.filter(title=title).first()
            if title_in_database:
                return Response({"message": "Duplicate menu-items are not allowed"}, status=status.HTTP_400_BAD_REQUEST)
            price = request.data['price']
            featured = bool(request.data.get('featured')) #featured variable isn't working properly
            category_name = request.data['category']
            category = get_object_or_404(Category, title=category_name)
            MenuItem.objects.create(title=title, price=price, featured=featured, category=category)
            return Response({"message": f"Added new menu-item: {title}"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Non-Manager cannot edit menu_items"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsManager])
def edit_single_menu_item(request, menu_item):
    menu_item_object = get_object_or_404(MenuItem, title=menu_item)
    if request.method == "GET":
        # Lists single menu item
        serializer = MenuItemSerializer(menu_item_object)
        return Response(serializer.data)
    elif request.method in ["PUT", "PATCH"]:
        # Updates single menu item
        serializer = MenuItemSerializer(menu_item_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        # Deletes menu item
        removed_menu_item = menu_item_object
        menu_item_object.delete()
        return Response({"message": f"removed {removed_menu_item}"})

# Cart management endpoints
#def edit_cart(request):












