# Generated by Django 3.0.3 on 2020-02-29 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("payments", "0003_auto_20200215_2048")]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="payment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="payments.Payment"
            ),
        )
    ]