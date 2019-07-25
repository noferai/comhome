from django.db import models


class Address(models.Model):
    address_str = models.CharField('Адрес', max_length=500)

    def __str__(self):
        return self.address_str

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Document(models.Model):
    # type_of_document
    # name
    # author
    # file
    pass
