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

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def endpoints(request):
    """
    Returns a list of all available API endpoints.
    """
    end_points = {
    'users-list': 'api/users/',  # List all users
    'user-detail': 'api/users/<int:pk>/',  # User detail by ID
    'user-create': 'api/users/',  # Create a new user
    'user-delete': 'api/users/<int:pk>/',  # Delete a user by ID
    'user-change_password': 'api/users/<int:pk>/change_password/',  # Change user's password
    'basic-token': 'api/auth/basic/',  # Basic authentication token
    'jwt-token-create': 'api/auth/jwt/',  # JWT token create
    'jwt-token-verify': 'api/auth/jwt/verify/',  # JWT token verify
    'jwt-token-refresh': 'api/auth/jwt/refresh/',  # JWT token refresh
    'book-list': 'api/books/',  # List all books
    'book-detail': 'api/books/<int:pk>/',  # Book detail by ID
    'book-info-list': 'api/book/info/',  # List all book information
    'book-info-detail': 'api/book/info/<int:pk>/',  # Book information detail by ID
    'checkout-list': 'api/checkout/',  # List all checkouts
    'checkout-detail': 'api/checkout/<int:pk>/',  # Checkout detail by ID
    'checkout-return': 'api/checkout/<int:pk>/return_book/',  # Return books, pk field is the id of the book
    'history-list': 'api/history/',  # List all history entries
    'history-detail': 'api/history/<int:pk>/',  # History detail by ID
    'endpoints': 'api/endpoints/',  # Get all API endpoints
    'api-root': 'api/',  # API root
    'return-book': 'api/books/<int:pk>/return/',  # Return a borrowed book
    'borrow-book': 'api/books/<int:pk>/checkout/',  # Checkout a book
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
    A viewset for managing BookInfo instances.
    """
    serializer_class = BookInfoSerializer
    queryset = BookInfo.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


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
        Handle book returns.
            """
        try:
            # Retrieve the book instance
            book = Book.objects.get(id=pk)
            # Retrieve the checkout instance for the specific user and book
            checkout = CheckOut.objects.filter(book__id=book.pk, user__email=request.user.email).get()
        except CheckOut.DoesNotExist:
            return Response({"error": "Checkout record not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            # Serialize the checkout data
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


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def return_book(request, pk=None):
    """
    Standalone view to return a borrowed book.
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


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrAdmin])
def borrow_book(request, pk=None):
    """
    Standalone view to borrow a book.
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
    A viewset for viewing transaction histories.
    """
    serializer_class = TransactionHistorySerializer
    queryset = ArchivedCheckOut.objects.all().order_by('-return_date')
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)
