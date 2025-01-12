from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response

from api.serializers import (
    BookSerializer,
    BookInfoSerializer,
    CheckOutSerializer,
    TransactionHistorySerializer,
)
from api.models import Book, BookInfo, CheckOut, ArchivedCheckOut
from utils.custom_permissions import IsOwnerOrAdmin
from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def endpoints(request):
    """
    Returns a list of all available API endpoints.
    """
    end_points = {
    'users-list': 'api/users/',  # List all users
    'user-detail': 'api/users/<int:pk>/',  
    'user-create': 'api/users/',  
    'user-delete': 'api/users/<int:pk>/',  
    'user-change_password': 'api/users/<int:pk>/change_password/', 
    
    'basic-token': 'api/token/basic/',  # Basic authentication token
    'jwt-token-create': 'api/token/jwt/',  # JWT token create
    'jwt-token-verify': 'api/token/jwt/verify/',  # JWT token verify
    'jwt-token-refresh': 'api/token/jwt/refresh/',  # JWT token refresh

    'book-list': 'api/books/',  # List all books
    'book-detail': 'api/books/<int:pk>/',
    'book-info-list': 'api/booksinfo/',  # List all book information
    'book-info-detail': 'api/booksinfo/<int:pk>/',  # Book information detail by ID
    'borrow-book': 'api/books/<int:pk>/checkout/',  #Borrow Book by ID
    'return-book': 'api/books/<int:pk>/return/', #Return Book by Id

    'checkout-list': 'api/checkout/',  # List all active checkouts
    'checkout-detail': 'api/checkout/<int:pk>/',  
    'checkout-return': 'api/checkout/<int:pk>/return_book/',  # Return books, pk field is the id of the book

    'history-list': 'api/checkout_history/',  #list user checkout history
    'endpoints': 'api/endpoints/', 
}

    return Response(end_points, status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Book instances.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['author', 'published_date']
    search_fields = ['title', 'author', 'ISBN']
    ordering_fields = ['published_date']

    def get_queryset(self):
        if self.request.method == 'GET':
            return self.queryset.filter(info__status=True).order_by('-info__copies')
        return super().get_queryset()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  
        self.perform_destroy(instance) 

        return Response(
            {"message": f"{instance.__class__.__name__} instance deleted."},
            status=status.HTTP_204_NO_CONTENT
        )


class BookInfoViewSet(viewsets.ModelViewSet):
    """
    A view for managing extra information about Books in the database.
    """
    serializer_class = BookInfoSerializer
    queryset = BookInfo.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CheckOutViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing book checkouts.
    """
    serializer_class = CheckOutSerializer
    queryset = CheckOut.objects.all().order_by('-checkout_date')
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    def get_permissions(self):
        if self.action in ['update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action == 'return_book':
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()
    
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the instance to be deleted
        self.perform_destroy(instance)  # Perform the deletion

        return Response(
            {"message": f"{instance.__class__.__name__} instance deleted."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['get', 'post'], url_name='return', permission_classes=[IsOwnerOrAdmin, permissions.IsAuthenticated])
    def return_book(self, request, pk=None):
        """
        Handle book returns. The id supplied is that of the Book that was 
        Borrowed Instead of the checkout id. If a checkout exists for that 
        book by the user making the request then they can return the book.
        """
        try:
            # Retrieve the book instance
            book = Book.objects.get(id=pk)

            # Retrieve the checkout instance for the specific user and book
            checkout = CheckOut.objects.filter(book__id=book.pk, user__email=request.user.email).get()
        except CheckOut.DoesNotExist:
            return Response({"error": "Checkout record not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            # Serialize the checkout data that was retrieved
            serializer = self.serializer_class(checkout)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            if checkout.status == 'Returned':
                # If the book is already marked as returned, delete the record
                checkout.delete()
                return Response({"detail": "Book already returned and record deleted."}, status=status.HTTP_200_OK)

            # Mark the book as returned 
            checkout.return_book()  
            checkout.delete()
            return Response({"detail": "Borrowed book returned successfully."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
        method='get',
        operation_summary='Return a borrowed Book',
        operation_description='View Information about Book to be returned',
        responses={200:BookSerializer}
)
@swagger_auto_schema(
    method='post',
    operation_summary='Return a borrowed Book',
    operation_description='Mark a borrowed book as returned and archive checkout',
    responses={200: "Borrowed Book Returned Successfully."}
)
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def return_book(request, pk=None):
    """
    Standalone view to return a borrowed book. Takes the primary key of the book then finds a checkout instance per the user if it exists. Before proceeding to return the book.
    """
    try:
        book = Book.objects.get(pk=pk)
        user = request.user
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
    
    

    if request.method == "GET":
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        try:
            checkout = CheckOut.objects.get(book=book.pk, user=user.pk)
        except CheckOut.DoesNotExist:
            return Response({"error": "Checkout record not found or Book Returned"}, status=status.
HTTP_404_NOT_FOUND)

        if checkout.Status == 'Returned':
            checkout.delete()
            return Response({"detail": "Book already returned and record deleted."}, status=status.HTTP_200_OK)

        checkout.return_book()
        checkout.delete()
        return Response({"detail": "Borrowed Book returned successfully."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
        method='get',
        operation_summary='Borrow a Book',
        operation_description='View Information about Book to be borrowed',
        responses={200:BookSerializer}
)
@swagger_auto_schema(
    method='post',
    operation_summary='Borrow a Book',
    operation_description='Checks if a Book is available checks it out.',
    responses={201: CheckOutSerializer}
)
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrAdmin])
def borrow_book(request, pk=None):
    """
    Standalone view to borrow a book. Takes the id of the book and checks it's 
    status. If the book is available then proceed to borrow the book. 
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = {"book": book.pk, "user": request.user.pk}
        serializer = CheckOutSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This view returns the checkout history of an authenticated user.
    """
    serializer_class = TransactionHistorySerializer
    queryset = ArchivedCheckOut.objects.all().order_by('-return_date')
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        elif self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response("Sorry Anonymous Users not Allowed", status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
