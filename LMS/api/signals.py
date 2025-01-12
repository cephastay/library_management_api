from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from api.models import Book, BookInfo, CheckOut, ArchivedCheckOut
from django.core.exceptions import MultipleObjectsReturned

@receiver(post_save, sender=Book)
def create_or_update_book_info(sender, instance, created, **kwargs):
    """
    A signal to create a book info entry after a book was created
    """
    if created:
        BookInfo.objects.get_or_create(
            book=instance
            )
    elif hasattr(instance, 'info'):
        instance.info.save()

@receiver(post_save, sender=CheckOut)
def set_due_date(sender, instance, **kwargs):
    """
    Automatically set the due date before saving a new checkout instance.
    """
    if not instance.due_date:
        instance.due_date = instance.get_due_date()
        instance.save()

@receiver(post_save, sender=CheckOut)
def update_book_copies_and_status(sender, instance, created, **kwargs):
    """
    A signal to update the number of book copies available post_checkout
    """
    if created:
        borrowed_book_info = BookInfo.objects.get(
            book = instance.book
        )
        borrowed_book_info.update_book_copies_post_checkout()
        borrowed_book_info.save()

@receiver(pre_delete, sender=CheckOut)
def update_book_copies_pre_delete_return(sender, instance, using, origin, **kwargs):
    """
    This signal updates the copies of a book once it is returned
    """
    borrowed_book_info = BookInfo.objects.get(
        book = instance.book
    )
    borrowed_book_info.update_book_copies_post_return()
    borrowed_book_info.save()

@receiver(pre_delete, sender= CheckOut)
def create_archived_checkout(sender, instance, using, origin, **kwargs):
    """
    Create entries in Archived Checkout Model Table post deletion
    """
    ArchivedCheckOut.objects.create(
        book = instance.book,
        user = instance.user,
        checkout_date = instance.checkout_date,
        return_date = instance.return_date
    )

@receiver(post_delete, sender= CheckOut)
def confirm_archived_checkout_instance(sender, instance, **kwargs):
    try:
        ArchivedCheckOut.objects.get_or_create(
        book = instance.book,
        user = instance.user,
        checkout_date = instance.checkout_date,
        return_date = instance.return_date    
    )
    except MultipleObjectsReturned:
        ArchivedCheckOut.objects.filter(
            book = instance.book,
            user = instance.user,
            checkout_date = instance.checkout_date,
            return_date = instance.return_date           
        ).first()

