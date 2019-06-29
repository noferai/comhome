from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import Account
from common.models import User, Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE, RequestPriorityChoices
from phonenumber_field.modelfields import PhoneNumberField


class Lead(models.Model):
    name = models.CharField('ФИО', max_length=255)
    gender = models.CharField('Пол', max_length=10, choices=RequestPriorityChoices.choices, blank=True, null=True)
    date_of_birth = models.CharField('Дата рождения', max_length=10)
    email = models.EmailField()
    phone = models.CharField('Телефон', max_length=255)
    status = models.CharField(_("Status of Lead"), max_length=255,
                              blank=True, null=True, choices=LEAD_STATUS)


    # TODO: Разобраться с остальными полями
    source = models.CharField(_("Source of Lead"), max_length=255,
                              blank=True, null=True, choices=LEAD_SOURCE)
    address = models.ForeignKey(Address, related_name='leadaddress', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField('Примечания', blank=True, null=True)
    assigned_to = models.ManyToManyField(User, related_name='lead_assigned_users')
    teams = models.ManyToManyField(Team)
    account_name = models.CharField(max_length=255, null=True, blank=True)
    opportunity_amount = models.DecimalField(
        _("Opportunity Amount"), decimal_places=2, max_digits=12,
        blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='lead_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField('Добавлен', auto_now_add=True)
    is_active = models.BooleanField(default=False)
    enquery_type = models.CharField(max_length=255, blank=True, null=True)



    class Meta:
        ordering =['-created_on']

    def __str__(self):
        return self.name
