# Generated by Django 3.1.3 on 2021-02-06 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kmuhelper', '0049_email_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='produkt',
            name='lieferant_url',
            field=models.URLField(blank=True, default='', verbose_name='Lieferantenurl (Für Nachbestellungen)'),
        ),
    ]
