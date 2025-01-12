from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.reverse import reverse
from datetime import datetime, timedelta
import isbnlib


class Book(models.Model):
    """Model for storing book details."""
    title: str = models.CharField(
        max_length=200,
        unique=True,
        help_text="Title of the book."
    )
    author: str = models.CharField(
        max_length=75,
        help_text="Author of the book."
    )
    ISBN: str = models.CharField(
        max_length=13,
        unique=True,
        help_text="ISBN (10 or 13 characters)."
    )
    published_date: models.DateField = models.DateField(
        blank=True,
        null=True,
        help_text="Publication date of the book."
    )

    def __str__(self) -> str:
        return f"{self.title.title()} by {self.author.title()}"

    def get_absolute_url(self) -> str:
        return reverse('book-detail', kwargs={'pk': self.pk})

    def validate_ISBN(self) -> None:
        """Validates the ISBN using isbnlib."""
        if self.ISBN and not (isbnlib.is_isbn10(self.ISBN) or isbnlib.is_isbn13(self.ISBN)):
            raise ValidationError("Invalid ISBN")

    def normalize_book_title(self) -> None:
        """Converts book title to title case."""
        self.title = self.title.title()

    def normalize_author_name(self) -> None:
        """Converts author's name to title case."""
        self.author = self.author.title()

    def save(self, *args, **kwargs) -> None:
        self.validate_ISBN()
        self.normalize_author_name()
        self.normalize_book_title()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class BookInfo(models.Model):
    """Stores additional information about books."""
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='info',
        help_text="Associated book."
    )
    copies: int = models.PositiveSmallIntegerField(
        default=0,
        help_text="Number of available copies."
    )
    date_added: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text="Date added to inventory."
    )
    status: bool = models.BooleanField(
        default=False,
        help_text="Availability status."
    )

    def __str__(self) -> str:
        return f"{self.book.title}, copies: {self.copies}"

    def update_status(self) -> bool:
        """Updates availability status based on copies."""
        self.status = self.copies >= 1
        return self.status

    def update_book_copies_post_return(self) -> int:
        """Increments copies when a book is returned."""
        self.copies += 1
        self.update_status()
        return self.copies

    def update_book_copies_post_checkout(self) -> int:
        """Decrements copies after checkout."""
        if self.copies > 0:
            self.copies -= 1
        else:
            raise ValidationError("No copies available for checkout.")
        self.update_status()
        return self.copies

    def save(self, *args, **kwargs) -> None:
        self.update_status()
        super().save(*args, **kwargs)


class CheckOut(models.Model):
    """Tracks active book checkouts."""
    class Status(models.TextChoices):
        MISSING = 'missing', 'Missing'
        PENDING = 'pending', 'Pending'
        RETURNED = 'returned', 'Returned'
        OVERDUE = 'overdue', 'Overdue'

    book = models.ForeignKey(
        to=Book,
        on_delete=models.RESTRICT,
        related_name='bookcheckouts',
        help_text='Book to be borrowed.'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.RESTRICT,
        related_name="usercheckouts",
        help_text="User borrowing the book."
    )
    checkout_date = models.DateField(
        auto_now_add=True,
        help_text="Checkout date."
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text='Due date for return.'
    )
    return_date = models.DateField(
        null=True,
        blank=True,
        help_text='Return date.'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text='Checkout status.'
    )

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.email} on {self.checkout_date}"

    def get_due_date(self) -> datetime:
        """Calculates due date based on a grace period."""
        return self.checkout_date + timedelta(days=15)

    def can_checkout(self) -> None:
        """Validates if the book is available for checkout."""
        if not self.book.info.status:
            raise ValidationError("Book not available for checkout.")

    def return_book(self) -> None:
        """Marks the book as returned."""
        if self.status == self.Status.RETURNED:
            raise ValidationError("Book already returned.")
        self.status = self.Status.RETURNED
        self.return_date = datetime.now().date()
        self.save()

    def set_status(self, status: str) -> None:
        """Updates the status."""
        if status in [choice[0] for choice in self.Status.choices]:
            self.status = status
            self.save()
        else:
            raise ValueError(f"Invalid status: {status}")

    def delete(self, *args, **kwargs):
        if self.status != self.Status.RETURNED:
            raise ValidationError("Book has not been returned.")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.can_checkout()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['user', 'book']
        


class ArchivedCheckOut(models.Model):
    """Tracks completed checkouts for archival purposes."""
    book = models.ForeignKey(
        Book,
        on_delete=models.RESTRICT,
        related_name='checkouts',
        help_text='Archived book.'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.RESTRICT,
        related_name="user_checkouts",
        help_text="User who borrowed the book."
    )
    checkout_date = models.DateField(
        help_text="Checkout date."
    )
    return_date = models.DateField(
        help_text='Return date.'
    )
