from django.contrib import admin

from book.models import Book, ReadingSession


admin.site.register(Book)
admin.site.register(ReadingSession)
