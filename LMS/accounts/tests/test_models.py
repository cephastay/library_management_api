from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.models import LibraryProfile

class TestCustomUserManager(TestCase):
    def test_create_user(self):
        """
        Test the creation of a standard user.
        """
        User = get_user_model()
        user = User.objects.create_user(
            email='testboy@gmail.com',
            password='secret1234'
        )
        self.assertEqual(user.email, 'testboy@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='secret1234')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='testboy@gmail.com', password='')

    def test_create_super_user(self):
        """
        Test the creation of a superuser.
        """
        User = get_user_model()

        admin_user = User.objects.create_superuser(
            email="testadminroot@yahoo.com",
            password="secret12345"
        )

        self.assertEqual(admin_user.email, "testadminroot@yahoo.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="testadminroot@yahoo.com",
                password="secret12345",
                is_superuser=False
            )

class TestCustomUserModel(TestCase):
    """
    Test the CustomUser model functionality.
    """

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            email='testboy@gmail.com',
            password='secret1234',
            first_name='Test',
            last_name='Boy'
        )

        cls.admin_user = User.objects.create_superuser(
            email='testadminroot@yahoo.com',
            password='secret12345',
            bio='I am your Admin and Librarian'
        )

    def setUp(self):
        return super().setUp()

    def test_user_creation(self):
        """
        Ensure that users and superusers are created successfully.
        """
        self.assertTrue(get_user_model().objects.filter(
            email='testboy@gmail.com').exists())
        self.assertTrue(get_user_model().objects.filter(
            email='testadminroot@yahoo.com').exists())

        self.assertIsInstance(self.user, get_user_model())
        self.assertIsInstance(self.admin_user, get_user_model())

    def test_user_password_hashed(self):
        """
        Verify that user passwords are hashed.
        """
        self.assertNotEqual(self.user.password, 'secret1234')
        self.assertNotEqual(self.admin_user.password, 'secret12345')

    def test_password_check(self):
        """
        Check that user passwords are valid.
        """
        self.assertTrue(self.user.check_password('secret1234'))
        self.assertTrue(self.admin_user.check_password('secret12345'))

    def test_email_validity(self):
        """
        Test that invalid email addresses raise a ValidationError.
        """
        with self.assertRaises(ValidationError):
            get_user_model().objects.create(
                email='jowel.com',
                password='secret1234'
            )

    def test_library_profile_creation(self):
        """
        Ensure LibraryProfile instances are created for users.
        """
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertTrue(hasattr(self.admin_user, 'profile'))
        self.assertEqual(self.user.profile.role, 'member')
        self.assertEqual(self.admin_user.profile.role, 'librarian')

    def test_disallow_empty_password(self):
        """
        Ensure that an empty password raises a ValueError.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='testboy@email.com',
                password=''
            )

    def test_bio_update(self):
        """
        Test updating the bio field of a user.
        """
        bio = """Hello, my name is TestBoy but my friends call me GrooT!"""
        admin_bio = "I am your Admin and Librarian"
        self.user.bio = bio
        self.user.save()
        self.assertEqual(self.user.bio, bio.lower())
        self.assertEqual(self.admin_user.bio, admin_bio.lower())

        # Update admin_bio
        new_bio = 'I am not Groot'
        self.admin_user.bio = new_bio
        self.admin_user.save()
        self.assertEqual(self.admin_user.bio, new_bio.lower())

    def test_profile_deletion_with_user(self):
        """
        Ensure LibraryProfile is deleted when user is deleted.
        """
        self.user.delete()
        with self.assertRaises(LibraryProfile.DoesNotExist):
            _ = LibraryProfile.objects.get(user__email='testboy@gmail.com')

        with self.assertRaises(get_user_model().DoesNotExist):
            _ = get_user_model().objects.get(email='testboy@gmail.com')