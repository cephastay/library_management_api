from django.contrib import admin
from api.models import Book, BookInfo, CheckOut, ArchivedCheckOut


class BookInfoInLine(admin.StackedInline):
    """
    Inline admin view for the BookInfo model.
    Allows editing BookInfo directly from the Book admin interface.
    """
    model = BookInfo
    extra = 0  # No extra empty inline forms by default.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    Includes an inline display of the related BookInfo model.
    """
    inlines = [BookInfoInLine]
    list_display = ('title', 'author', 'published_date', 'ISBN')  # Example fields
    search_fields = ('title', 'author', 'ISBN')  # Allow search by these fields
    list_filter = ('published_date',)  # Filter books by their publication date


@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CheckOut model.
    Allows managing the checkout records of books.
    """
    list_display = ('book', 'user', 'status', 'checkout_date', 'due_date','return_date')
    list_filter = ('status', 'checkout_date', 'return_date')
    search_fields = ('book__title', 'user__email')  # Assumes related borrower is a user model
    date_hierarchy = 'checkout_date'  # Adds navigation by checkout date
    ordering = ('-checkout_date',)  # Orders by most recent checkout first

    # Custom actions for CheckOut
    actions = ['mark_as_returned']

    def mark_as_returned(self, request, queryset):
        """
        Custom action to mark selected checkouts as returned.
        """
        updated_count = queryset.filter(status='borrowed').update(status='returned', return_date=None)
        self.message_user(request, f"{updated_count} checkout(s) successfully marked as returned.")
    mark_as_returned.short_description = "Mark selected checkouts as returned"


@admin.register(ArchivedCheckOut)
class ArchivedCheckOutAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ArchivedCheckOut model.
    Manages archived checkout records of books.
    """
    list_display = ('book', 'user', 'checkout_date', 'return_date')
    list_filter = ('checkout_date', 'return_date')
    search_fields = ('book__title', 'user__email')
    date_hierarchy = 'return_date'  # Navigation by the date when checkout was archived
    ordering = ('-return_date',)  # Orders by most recent archival first

    def has_add_permission(self, request):
        """
        Disallow adding new archived checkout records manually.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Allow deleting archived checkout records.
        """
        return True
