# Generated by Django 2.2 on 2019-04-07 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20190408_0135'),
        ('contacts', '0001_initial'),
        ('common', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
        ('opportunity', '0001_initial'),
        ('cases', '0002_auto_20190408_0135'),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_comments', to='contacts.Contact'),
        ),
        migrations.AddField(
            model_name='comment',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='leads.Lead'),
        ),
        migrations.AddField(
            model_name='comment',
            name='opportunity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opportunity_comments', to='opportunity.Opportunity'),
        ),
        migrations.AddField(
            model_name='attachments',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_attachment', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='attachments',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_attachment', to='cases.Case'),
        ),
        migrations.AddField(
            model_name='attachments',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_attachment', to='contacts.Contact'),
        ),
        migrations.AddField(
            model_name='attachments',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachments',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_attachment', to='leads.Lead'),
        ),
        migrations.AddField(
            model_name='attachments',
            name='opportunity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opportunity_attachment', to='opportunity.Opportunity'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]