# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.BooleanField(default=False)),
                ('avatar_image', models.CharField(max_length=255, null=True, blank=True)),
                ('_avatar_crop', models.CharField(max_length=255, null=True, db_column=b'avatar_crop', blank=True)),
                ('avatar_original', models.CharField(max_length=255, null=True, blank=True)),
                ('avatar_temp', models.CharField(max_length=255, null=True, blank=True)),
                ('avatar_type', models.CharField(max_length=10, null=True, blank=True)),
                ('signature', models.CharField(max_length=255, null=True, blank=True)),
                ('articles', models.PositiveIntegerField(default=0)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('following', models.PositiveIntegerField(default=0)),
                ('follower', models.PositiveIntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('fans', models.ManyToManyField(related_name='fans_set', to=settings.AUTH_USER_MODEL)),
                ('follows', models.ManyToManyField(related_name='follows_set', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
            bases=(models.Model,),
        ),
    ]
