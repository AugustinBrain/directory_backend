# Generated by Django 5.2.4 on 2025-07-24 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0004_rename_member_id1_academicbackground_member_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passwordresetotp',
            old_name='account_id',
            new_name='account',
        ),
    ]
