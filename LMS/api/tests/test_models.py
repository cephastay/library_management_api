from time import sleep
from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import Book, BookInfo, CheckOut, ArchivedCheckOut
from django.contrib.auth import get_user_model
import datetime

class BookTestCase(TestCase):
    """
    Test suite for Book and Book_Info models and their related functionality.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for tests.
        """
        cls.book1 = Book.objects.create(
            title='half of a yellow sun',
            author='chimamanda adichie ngozie',
            ISBN='9780676978124',
            published_date='2008-06-03'
        )

    def test_create_book_model(self):
        """
        Test the creation of a Book instance and its attributes.
        """
        self.assertIsInstance(self.book1, Book)
        self.assertEqual(self.book1.title, 'Half Of A Yellow Sun')
        self.assertEqual(self.book1.author, 'Chimamanda Adichie Ngozie')
        self.assertRegex(
            self.book1.ISBN,
            r'(ISBN[-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})'
        )

    def test_validate_ISBN_method(self):
        """
        Test the ISBN validation method.
        """
        valid_isbn = '9780676978124'
        invalid_isbn = '1234567890123'
        
        self.book1.ISBN = valid_isbn
        self.assertIsNone(self.book1.validate_ISBN())

        self.book1.ISBN = invalid_isbn
        with self.assertRaises(ValidationError):
            self.book1.validate_ISBN()

    def test_normalization_methods(self):
        """
        Test the normalization of book title and author name during save.
        """
        book = Book.objects.create(
            title='a thousand Splendid Suns',
            author='khaled hosseini',
            ISBN='9781594489501',
            published_date='2007-05-22'
        )
        self.assertEqual(book.title, 'A Thousand Splendid Suns')
        self.assertEqual(book.author, 'Khaled Hosseini')

    def test_book_info_creation(self):
        """
        Test that a Book_Info instance is automatically created for a new Book.
        """
        self.assertTrue(hasattr(self.book1, 'info'))
        self.assertEqual(self.book1.info.copies, 0)
        self.assertFalse(self.book1.info.status)
    
    def test_book_info_creation_failure(self):
        message = ''
        with self.assertRaises(ValidationError, msg= message):
            book3 = Book.objects.create(
                title= 'Dummy Book',
                author='',
                ISBN='',
                published_date= ''
        )
            self.assertFalse(
                BookInfo.objects.filter(
                    book__title = 'Dummy Book'
                ).exists()
            )
            book7 = Book.objects.create(
                author = 'Dummy Author'
            )
            self.assertFalse(
                BookInfo.objects.filter(
                    book__author = 'Dummy Author'
                ).exists()
            )

    def test_book_info_update_status(self):
        """
        Test the update of book availability status based on copies.
        """
        self.book1.info.copies = 1
        self.book1.info.save()
        self.assertTrue(self.book1.info.status)

        self.book1.info.copies = 0
        self.book1.info.save()
        self.assertFalse(self.book1.info.status)

    def test_book_info_checkout_and_return(self):
        """
        Test the update of book copies during checkout and return.
        """
        self.book1.info.copies = 3
        self.book1.info.save()

        # Test checkout
        self.book1.info.update_book_copies_post_checkout()
        self.assertEqual(self.book1.info.copies, 2)

        # Test return
        self.book1.info.update_book_copies_post_return()
        self.assertEqual(self.book1.info.copies, 3)

    def test_checkout_when_no_copies(self):
        """
        Test behavior when a checkout is attempted with no available copies.
        """
        self.book1.info.copies = 0
        self.book1.info.save()
        with self.assertRaises(ValidationError):
            self.book1.info.update_book_copies_post_checkout()

    def test_book_info_deletion_with_book(self):
        """
        Test that deleting a Book also deletes its associated Book_Info instance.
        """
        self.book1.delete()
        with self.assertRaises(BookInfo.DoesNotExist):
            _ = BookInfo.objects.get(book=self.book1.pk)

    def test_unique_isbn_constraint(self):
        """
        Test the unique constraint on the ISBN field of the Book model.
        """
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            Book.objects.create(
                title='Another Book',
                author='Another Author',
                ISBN=self.book1.ISBN,
                published_date='2023-01-01'
            )

class CheckOutTestCase(TestCase):
    """
    
    """
    @classmethod
    def setUpTestData(cls): 

        cls.book1 = Book.objects.create(
            title='half of a yellow sun',
            author='chimamanda adichie ngozie',
            ISBN='9780676978124',
            published_date='2008-06-03',
        )
        cls.user1 = get_user_model().objects.create_user(
            email= 'testboy@email.com',
            password= 'secret1234'
        )
        cls.user2 = get_user_model().objects.create_superuser(
            email= 'testadmin@email.com',
            password= 'secret1234'
        )
        cls.book1.info.copies = 5
        cls.book1.save()

        cls.checkout1 = CheckOut.objects.create(
            book = cls.book1,
            user = cls.user1
        )
    
    def test_checkout_creation(self):
        self.assertIsInstance(self.checkout1, CheckOut)
        self.assertEqual(self.checkout1.book.title, 'Half Of A Yellow Sun')
        self.assertEqual(self.checkout1.user.email, 'testboy@email.com')
        self.assertEqual(
            str(self.checkout1.due_date),
            str(self.checkout1.get_due_date())
            )
        self.assertEqual(str(self.checkout1.status), 'pending')

    def test_cannot_check_same_book_twice_at_once(self):
        with self.assertRaises(IntegrityError):
            CheckOut.objects.create(
                user= self.user1,
                book=self.book1
            )

    def test_book_return_and_status_update(self):
        self.checkout1.return_book()
        self.assertEqual(str(self.checkout1.status), 'returned')
        self.assertEqual(
            str(self.checkout1.return_date),
            str(datetime.datetime.now().date())
        )

        self.checkout1.set_status(status='overdue')
        self.assertEqual(str(self.checkout1.status), 'overdue')

        self.checkout1.set_status(status='missing')
        self.assertEqual(str(self.checkout1.status), 'missing')

        with self.assertRaises(ValueError):
            self.checkout1.set_status(status='random')

    def test_cannot_checkout_book_unavailable_or_no_copies(self):
        self.book1.info.copies = 0
        self.book1.save()
        message = 'No copies available for checkout.'
        with self.assertRaises(ValidationError, msg=message):
            CheckOut.objects.create(
                user= self.user2,
                book = self.book1
            )
    
    def test_archived_checkout_creation_post_checkout_deletion(self):
        self.checkout1.return_book()
        self.checkout1.delete()
        archived_checkout = ArchivedCheckOut.objects.filter(
            book = self.book1,
            user = self.user1
        ).exists()
        self.assertTrue(archived_checkout)

    def test_cannot_delete_checkout_without_return_book(self):
        message = 'Sorry cannot delete as book has not been returned'
        with self.assertRaises(ValidationError, msg=message):
            self.checkout1.delete()
    