# Generated by Django 4.0 on 2022-01-06 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0003_review'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.CharField(max_length=100)),
                ('notes', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='order.OrderItem', to='main.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to='account.user'),
        ),
    ]
