from rest_framework import serializers
from api.models import Book, BookInfo, CheckOut, ArchivedCheckOut

import isbnlib
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import status

User = get_user_model()

class BookSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Book model.
    Handles validation, creation, and updating of Book instances.
    """
    book_info = serializers.HyperlinkedRelatedField(
        view_name='bookinfo-detail',
        read_only=True,
        source='info'
    )
    book_copies = serializers.IntegerField(
        source='info.copies',
        required=False
    )
    can_checkout = serializers.ReadOnlyField(
        source='info.status'
    )

    class Meta:
        model = Book
        fields = [
            'url', 'title', 'author', 'ISBN', 'published_date',
            'book_copies', 'can_checkout', 'book_info'
        ]

    def validate_book_copies(self, value):
        """
        Ensures book copies are a positive integer.
        """
        if not (isinstance(value, int) and value > 0):
            raise serializers.ValidationError("Copies must be a positive integer.")
        return value

    def validate_ISBN(self, value):
        """
        Validates the ISBN to ensure it is either a valid ISBN-10 or ISBN-13.
        """
        if not (isbnlib.is_isbn13(value) or isbnlib.is_isbn10(value)):
            raise serializers.ValidationError(f"The ISBN {value} is invalid.")
        return value

    def validate_published_date(self, value):
        """
        Ensures the published_date is not in the future.
        """
        if value and value > datetime.now().date():
            raise serializers.ValidationError("Unpublished books are not allowed.")
        return value

    def create(self, validated_data):
        """
        Creates a new Book instance and optionally updates BookInfo if copies are provided.
        """
        extra_info = validated_data.pop('info', None)
        instance = super().create(validated_data)

        if extra_info:
            book_info = BookInfo.objects.get(book=instance)
            book_info.copies = extra_info['copies']
            book_info.save()

        return instance

    def update(self, instance, validated_data):
        """
        Updates a Book instance and optionally updates BookInfo if copies are provided.
        """
        extra_info = validated_data.pop('info', None)

        # Update book fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        # Update book_info if provided
        if extra_info:
            book_info = BookInfo.objects.get(book=instance)
            book_info.copies = extra_info.get('copies', book_info.copies)
            book_info.save()

        instance.save()
        return instance


class BookInfoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the BookInfo model.
    Provides additional details about the book's availability and copies.
    """
    available = serializers.ReadOnlyField(source='status')
    book_detail = serializers.HyperlinkedRelatedField(
        view_name='book-detail',
        read_only=True,
        lookup_field='pk',
        source='book'
    )
    title = serializers.ReadOnlyField(source='book.title')
    author = serializers.ReadOnlyField(source='book.author')

    class Meta:
        model = BookInfo
        fields = ['title', 'author', 'book_detail', 'available', 'copies', 'url']
        extra_kwargs = {
            "url": {"view_name": "bookinfo-detail", "lookup_field": "pk"}
        }


class CheckOutSerializer(serializers.ModelSerializer):
    """
    Serializer for the CheckOut model.
    Manages the borrowing process of books.
    """

    book_title = serializers.ReadOnlyField(source='book.title')
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = CheckOut
        fields = [
            'book', 'book_title','user', 'checkout_date', 'due_date',
            'return_date', 'status', 'id'
        ]
        read_only_fields = ['due_date', 'status', 'return_date']


    def validate(self, attrs):
        """
        Ensures the book is available for checkout and checks if the user has already checked out the book.
        """
        book_id = attrs['book']  # Get the book ID
        try:
            book = Book.objects.get(id=book_id.id)  # Retrieve the Book instance
        except Book.DoesNotExist:
            raise serializers.ValidationError({"book": "Sorry, the book does not exist."})

        # Check if the book is available
        if not book.info.status:
            raise serializers.ValidationError(
                {"book": f"The book '{book.title}' is currently unavailable for checkout."}
            )

        return attrs

    def create(self, validated_data):
        """
        Overrides the create method to handle book instance and ensure the book exists.
        """
        book_id = validated_data.pop('book')  # Get the book ID
        user = validated_data['user']  # Get the user
        try:
            book_instance = Book.objects.get(id=book_id.id)  
        except Book.DoesNotExist:
            raise serializers.ValidationError({"book": "Sorry, the book does not exist."})

        # Attempt to create the checkout instance
        try:
            checkout_instance = CheckOut.objects.create(
                book=book_instance,
                user=user
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {"checkout": "Sorry You might have borrowed this Book already."}
            )
        return checkout_instance



































    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    

    
    
    

class TransactionHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for ArchivedCheckOut model.
    Displays past transaction details for books.
    """
    user = serializers.ReadOnlyField(source='user.email')
    book = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = ArchivedCheckOut
        fields = '__all__'
        
