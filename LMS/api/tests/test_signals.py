from unittest import mock
from django.test import TestCase
from api.models import Book, BookInfo, CheckOut, ArchivedCheckOut
from django.db.models.signals import post_save, post_delete, pre_delete
from django.contrib.auth import get_user_model


class BookSignalsTest(TestCase):

    def test_create_or_update_bookinfo_signal(self):
        with mock.patch(
            'api.signals.create_or_update_book_info',
            autospec=True
        ) as mocked_handler:
            post_save.connect(mocked_handler, sender=Book)

            dummy = Book.objects.create(
                title='Test Book',
                author='Test Author',
                ISBN='9780676978124'
            )

            mocked_handler.assert_called_once()

            mocked_handler.assert_has_calls([
                mock.call(
                    signal=post_save,
                    sender=Book,
                    instance=dummy,
                    created=True,
                    raw=mock.ANY,          
                    using=mock.ANY,
                    update_fields=mock.ANY
                )
            ])

            dummy.title = 'A New Title'
            dummy.save()

            self.assertEqual(mocked_handler.call_count, 2)

            mocked_handler.assert_has_calls(
                [
                    mock.call(
                        signal = post_save,
                        sender= Book,
                        instance= dummy,
                        created= False,
                        raw= mock.ANY,
                        using= mock.ANY,
                        update_fields= mock.ANY
                        
                    )
                ]
            )

class CheckOutSignalTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title= 'Test Book',
            author= 'Test Author',
            ISBN= '9786589008194',
            published_date = '2020-01-01'
        )

        cls.user = get_user_model().objects.create_user(
            email= 'testboy@email.com',
            password= 'secret1234'
        )
        cls.user2 = get_user_model().objects.create_superuser(
            email= 'superuser@email.com',
            password= 'secret1234'
        )
        cls.user3 = get_user_model().objects.create_user(
            email= 'mock@email.com',
            password= 'pass1234'
        )
        cls.book.info.copies = 5
        cls.book.save()

        cls.dummy_checkout = CheckOut.objects.create(
                book = cls.book,
                user = cls.user
                )
        
        cls.dummy_checkout2 = CheckOut.objects.create(
            book = cls.book,
            user = cls.user3
        )

    def test_set_due_date_signal(self):
        with mock.patch(
            'api.signals.set_due_date',
            autospec= True
        ) as mocked_handler:
            post_save.connect(mocked_handler, sender=CheckOut)

            
            self.dummy_checkout.save()
            
            mocked_handler.assert_called()
            mocked_handler.assert_has_calls([
                mock.call(
                    signal=post_save,
                    sender=CheckOut,
                    instance=self.dummy_checkout,
                    raw=mock.ANY,
                    created= mock.ANY,
                    using=mock.ANY,
                    update_fields=mock.ANY
                )
            ])
            self.assertIsNotNone(self.dummy_checkout.due_date)
            self.book.refresh_from_db()
            self.assertEqual(self.book.info.copies, 3)

    def test_update_book_copies_status_signal(self):
        with mock.patch(
            'api.signals.update_book_copies_and_status',
            autospec= True) as mocked_handler:
            post_save.connect(mocked_handler, sender=CheckOut)
            
            checkout1 = CheckOut.objects.create(
                book=self.book,
                user= self.user2)
            
            mocked_handler.assert_called()
            self.assertEqual(mocked_handler.call_count, 2)
            self.book.refresh_from_db()
            self.assertEqual(self.book.info.copies, 2)

    def test_update_book_copies_post_return_signal(self):
        with mock.patch(
            'api.signals.update_book_copies_pre_delete_return',
            autospec=True) as mocked_handler:
            pre_delete.connect(mocked_handler, sender=CheckOut)

            self.dummy_checkout.return_book()
            self.dummy_checkout.delete()

            mocked_handler.assert_called_once()
            mocked_handler.assert_has_calls([
                mock.call(
                    signal=pre_delete,
                    sender=CheckOut,
                    instance=self.dummy_checkout,
                    using=mock.ANY,
                    origin=mock.ANY
                )
            ])
            self.book.refresh_from_db()
            self.assertEqual(self.book.info.copies, 4)

    def test_create_archived_checkout_signal(self):
        with mock.patch(
            'api.signals.create_archived_checkout',
            autospec=True) as mocked_handler:
            pre_delete.connect(mocked_handler, sender=CheckOut)

            # Trigger the signal by deleting the CheckOut
            self.dummy_checkout.return_book()
            self.dummy_checkout.delete()

            mocked_handler.assert_called_once()
            mocked_handler.assert_has_calls([
                mock.call(
                    signal=pre_delete,
                    sender=CheckOut,
                    instance=self.dummy_checkout,
                    using=mock.ANY,
                    origin=mock.ANY
                )
            ])

        # Ensure an ArchivedCheckOut instance was created
        archived = ArchivedCheckOut.objects.filter(
            book=self.book,
            user_id=1).exists()
        self.assertTrue(archived)

    def test_confirm_archived_checkout_instance_signal(self):
        with mock.patch(
            'api.signals.confirm_archived_checkout_instance',
            autospec=True) as mocked_handler:
            post_delete.connect(mocked_handler, sender=CheckOut)

            # Trigger the signal by deleting the CheckOut
            self.dummy_checkout.return_book()
            self.dummy_checkout.delete()

            mocked_handler.assert_called_once()
            mocked_handler.assert_has_calls([
                mock.call(
                    signal=post_delete,
                    sender=CheckOut,
                    instance=self.dummy_checkout,
                    using=mock.ANY,
                    origin= mock.ANY
                )
            ])

        # Ensure the ArchivedCheckOut instance exists
        archived = ArchivedCheckOut.objects.filter(
            book=self.book,
            user_id=1).exists()
        self.assertTrue(archived)

