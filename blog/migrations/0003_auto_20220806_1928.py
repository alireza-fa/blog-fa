# Generated by Django 3.2 on 2022-08-06 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220806_1829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created',), 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ('-created',), 'verbose_name': 'Post Comment', 'verbose_name_plural': 'Post Comments'},
        ),
    ]