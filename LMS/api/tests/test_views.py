from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Book, CheckOut, ArchivedCheckOut

User = get_user_model()

class EndpointsTestCase(APITestCase):
    def test_endpoints_list(self):
        url = reverse('endpoints')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users-list', response.data)


class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@email.com', password='password123')
        self.admin = User.objects.create_superuser(email='admin@gmail.com', password='adminpassword')
        self.book = Book.objects.create(title='Test Book', author='Author A', ISBN='0-8436-1072-7')
        self.url = reverse('book-list')

    def test_list_books(self):
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_and_retrieve_book_as_admin(self):
        # self.client.force_authenticate(user=self.admin)
        # data = {
            # 'title': 'New Book',
            # 'author': 'Author B',
            # 'ISBN': '9788535938050',
            # 'published_date': '1967-08-01'
        # }
        # Post a new book
        # response_post = self.client.post(path=self.url, data=data)
        # self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        # created_book_id = response_post.data['id']  

        # Retrieve the newly created book
        # url_detail = reverse('book-detail', kwargs={'pk': created_book_id})
        # response_get = self.client.get(path=url_detail)
        # self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        # Verify that the returned data matches the posted data
        # self.assertEqual(response_get.data['title'], data['title'])
        # self.assertEqual(response_get.data['author'], data['author'])
        # self.assertEqual(response_get.data['ISBN'], data['ISBN'])
        # # self.assertEqual(response_get.data['published_date'], data['published_date'])

    def test_create_book_as_non_admin(self):
        data = {'title': 'New Book', 'author': 'Author B', 'ISBN': '0987654321'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CheckOutViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@email1.com', password='password123')
        self.book = Book.objects.create(title='Test Book', author='Author A', ISBN='0205080057')
        self.book.info.copies = 5
        self.book.save()
        self.checkout = CheckOut.objects.create(book=self.book, user=self.user)
        self.client.force_authenticate(user=self.user)
        self.url_list = reverse('checkout-list')

    def test_list_checkouts(self):
        response = self.client.get(path=self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_checkout_and_retrieve(self):
        # Post a new checkout
        # data = {'book': self.book.id, 'user': self.user.id}
        # response_post = self.client.post(path=self.url_list, data=data)
        # self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        # created_checkout_id = response_post.data['id']  # Assuming the response includes the checkout's ID

        # Retrieve the newly created checkout
        # url_detail = reverse('checkout-detail', kwargs={'pk': created_checkout_id})
        # response_get = self.client.get(path=url_detail)
        # self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        # Verify that the returned data matches the posted data
        # self.assertEqual(response_get.data['book'], data['book'])
        # self.assertEqual(response_get.data['user'], data['user'])


class BorrowReturnBookTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@email.com', password='password123')
        self.book = Book.objects.create(title='Test Book', author='Author A', ISBN='0205080057')
        self.book.info.copies = 5
        self.book.save()
        self.checkout = CheckOut.objects.create(book=self.book, user=self.user)
        self.url_return = reverse('return_book', kwargs={"pk": self.book.id})
        self.url_borrow = reverse('borrow_book', kwargs={"pk": self.book.id})

    def test_return_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(path=self.url_return)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Uncomment and implement once user borrowing logic is set
    # def test_borrow_book(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post(path=self.url_borrow)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TransactionHistoryViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@email.com', password='password123')
        self.admin = User.objects.create_superuser(email='admin@email.com', password='adminpassword')
        self.book = Book.objects.create(title='Test Book', author='Author A', ISBN='0205080057')
        self.book.info.copies = 5
        self.book.save()
        self.checkout = CheckOut.objects.create(book=self.book, user=self.user)
        self.archived_checkout = ArchivedCheckOut.objects.create(
            user=self.user, book=self.book, checkout_date='2012-01-01', return_date='2012-01-03'
        )
        self.url = reverse('history-list')

    def test_list_transaction_history(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_access(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
