from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .models import Post, Comment, PostImage, UserProfile
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Product, ProductCount, Cart
import json

import urllib
import json
from requests.utils import requote_uri


class CustomObtainAuthToken(ObtainAuthToken):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def put(self, request):
        print("invoked puttttt")
        if request.user.is_authenticated:
            s = UserSerializer(instance=request.user, data=request.POST)
        if s.is_valid():
            s.save()
            return Response(
                {'message': 'profile edited!'}, status=201)
        else:
            return Response(
                {'message': 'you are not login!'}, status=401)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # url: http://127.0.0.1:8000/posts/post_of_logged_in_user/
    @action(detail=False, methods=['get'])
    def post_of_logged_in_user(self, request):
        print(request.data)
        user = request.user
        queryset = Post.objects.filter(user=user.id)
        serializer = PostSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # url: http://127.0.0.1:8000/posts/post_of_selected_user/?selected_id=1
    @action(detail=False, methods=['get'])
    def post_of_selected_user(self, request, *args, **kwargs):
        print(request.GET['selected_id'])
        selected_user = int(request.GET['selected_id'])
        queryset = Post.objects.filter(user=selected_user)
        serializer = PostSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # url: http://127.0.0.1:8000/posts/1/update_post_likes/?latest_like=10
    @action(detail=True, methods=['post'])
    def update_post_likes(self, request, *args, **kwargs):
        print("invoked")
        latest_like = int(request.GET['latest_like'])
        print(latest_like)
        post = self.get_object()
        print(post)
        queryset = Post.objects.filter(id=post.id)
        queryset.update(likes=latest_like)
        serializer = PostSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # TODO: query with different rules


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        userId = int(request.data.get("userId"))
        cartId = int(request.data.get("cartId"))

        cart = Cart.objects.filter(id=cartId)[0]
        user = User.objects.filter(id=userId)[0]

        order = Order(user=user,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            phone=request.data.get("phone"),
            address=request.data.get("address"))
        order.save()

        productCountsSet = cart.productCounts.all()
        for i in range(len(productCountsSet)):
            productCount = productCountsSet[i]
            orderProductCount = OrderProductCount(order=order, 
                                                product=productCount.product, 
                                                count=productCount.count)
            productCount.delete()
            orderProductCount.save()

        queryset = Order.objects.filter(pk=order.pk)
        serializer = OrderSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer


def update_products_view(request: HttpRequest) -> JsonResponse:
    # url = "http://makeup-api.herokuapp.com/api/v1/products.json"
    # url = requote_uri(url)
    # connection = urllib.request.urlopen(url)
    with open('./oshare/makeup.json', encoding="utf8") as f:
        response = json.load(f)
    # response = json.load(connection)
    # print(response)
    for x in response:
        try:
            Product.objects.get(id=x['id'])
        except Product.DoesNotExist:
            price = 0.0
            if x['price'] != None:
                price = float(x['price'])
            new_product = Product(
                id=int(x['id']),
                name=x['name'],
                brand=x['brand'],
                category=x['category'],
                product_type=x['product_type'],
                price=price,
                price_sign=x['price_sign'],
                currency=x['currency'],
                img_link=x['image_link'],
                description=x['description'],
            )
            new_product.save()
    return JsonResponse({})


class ProductCountViewSet(viewsets.ModelViewSet):
    queryset = ProductCount.objects.all()
    serializer_class = ProductCountSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.count = request.data.get("count")
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def addToCart(self, request, *args, **kwargs):
        cartId = int(request.data.get("cartId"))
        productId = int(request.data.get("productId"))
        product = Product.objects.get(id=productId)
        cart = Cart.objects.get(id=cartId)

        try:
            cart_product = ProductCount.objects.get(product=product, cart=cart)
            cart_product.count += 1
            cart_product.save()
        except ProductCount.DoesNotExist:
            cart_product = ProductCount(product=product, count=1, cart=cart)
            cart_product.save()

        queryset = ProductCount.objects.none()
        queryset |= ProductCount.objects.filter(pk=cart_product.pk)
        serializer = ProductCountSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def search_product(self, request):
        print("request", request.data)
        queryset = Product.objects.all()
        print("entered the search product function, queryset", len(queryset))
        keys = request.GET.keys()
        if 'id' in keys:
            serializer = ProductSerializer(Product.objects.get(id=request.GET['id']), many=False,
                                           context={'request': request})
            return JsonResponse({'response': serializer.data})
        if 'name' in keys:
            queryset = queryset.filter(name=request.GET['name'])
            print("queryset after name", len(queryset))
        if 'brand' in keys:
            queryset = queryset.filter(brand=request.GET['brand'])
            print("queryset after brand", len(queryset), request.GET['brand'])
        if 'category' in keys:
            queryset = queryset.filter(category=request.GET['category'])
            print("queryset after category", len(queryset))
        if 'type' in keys:
            queryset = queryset.filter(product_type=request.GET['type'])
            print("queryset after type", len(queryset))
        if 'price_greater_than'in keys:
            queryset = queryset.filter(
                price__gte=request.GET['price_greater_than'])
        if 'price_less_than'in keys:
            queryset = queryset.filter(
                price__lte=request.GET['price_less_than'])
        if 'input' in keys:
            print("input", request.GET['input'])
            str = request.GET['input'].split(" ")
            tempset = Product.objects.none()
            for word in str:
                print("word in input", word)
                result = queryset.filter(name__contains=word)
                tempset = result.union(tempset)
            queryset = tempset
        print("queryset in the search product", len(queryset))
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        # return Response(serializer.data)
        return JsonResponse({'response': serializer.data})


'''
def get_product_view(request: HttpRequest) -> JsonResponse:
    queryset = Product.objects.filter()
    keys = request.GET.keys()
    if 'id' in keys:
        serializer = ProductSerializer(Product.objects.get(id=request.GET['id']), many=False,
                                       context={'request': request})
        return JsonResponse({'response': serializer.data})
    if 'name' in keys:
        queryset = queryset.filter(name=request.GET['name'])
    if 'brand' in keys:
        queryset = queryset.filter(brand=request.GET['brand'])
    if 'category' in keys:
        queryset = queryset.filter(category=request.GET['category'])
    if 'type' in keys:
        queryset = queryset.filter(product_type=request.GET['type'])
    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    return JsonResponse({'response': serializer.data})
'''
'''
def add_to_cart_view(request: HttpRequest) -> JsonResponse:
    data = {}
    try:
        product_id = request.GET['id']
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=request.user)
    except Exception:
        data["error"] = 'Fail to add to cart'
        return JsonResponse(data)

    try:
        cart_product = ProductCount.objects.get(product=product, cart=cart)
        cart_product.count += 1
        cart_product.save()
    except ProductCount.DoesNotExist:
        cart_product = ProductCount(product=product, count=1, cart=cart)
        cart_product.save()
        cart.products.add(cart_product)

    cart.total += 1
    cart.save()
    data["cart_count"] = cart.total
    data["status"] = 'add to cart succeeded!'

    return JsonResponse(data)


'''