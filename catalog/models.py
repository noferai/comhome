from django.db import models


class Address(models.Model):
    address = models.CharField('Адрес', max_length=500)

    def __str__(self):
        return self.address


class Document(models.Model):
    # type_of_document
    # name
    # author
    # file
    pass
