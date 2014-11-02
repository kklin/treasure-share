# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('donor', models.CharField(max_length=20)),
                ('amount', models.IntegerField(default=0)),
                ('creation_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dribble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('percentage', models.DecimalField(max_digits=2, decimal_places=2)),
                ('delay', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('members', models.ManyToManyField(to='treasure.Profile', through='treasure.Membership')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='membership',
            name='profile',
            field=models.ForeignKey(to='treasure.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='recips',
            field=models.ForeignKey(to='treasure.Recipients'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='donation',
            name='charities',
            field=models.ForeignKey(to='treasure.Recipients'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='donation',
            name='dribble',
            field=models.ForeignKey(to='treasure.Dribble'),
            preserve_default=True,
        ),
    ]
