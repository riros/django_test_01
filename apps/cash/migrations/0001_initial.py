# Generated by Django 3.0.1 on 2019-12-20 06:42

import apps.cash.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashTransaciton',
            fields=[
                ('id', models.UUIDField(db_column='Id', default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tid', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('val', models.FloatField(help_text='currency', validators=[apps.cash.validators.pay_validator], verbose_name='Amount transfer')),
                ('active', models.BooleanField(db_index=True, default=True, help_text='Transaction accepted', verbose_name='Active')),
                ('dst', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dst_user_id', to=settings.AUTH_USER_MODEL)),
                ('src', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='src_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'currency transfers',
                'verbose_name_plural': 'currency transfers',
            },
        ),
    ]
