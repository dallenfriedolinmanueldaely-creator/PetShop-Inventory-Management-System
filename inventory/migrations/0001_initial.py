from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Barang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_barang', models.CharField(max_length=200, verbose_name='Nama Barang')),
                ('kategori', models.CharField(
                    choices=[
                        ('Makanan', 'Makanan'),
                        ('Vitamin', 'Vitamin'),
                        ('Grooming', 'Grooming'),
                        ('Mainan', 'Mainan'),
                        ('Aksesoris', 'Aksesoris'),
                    ],
                    max_length=50,
                    verbose_name='Kategori',
                )),
                ('harga', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Harga (Rp)')),
                ('stok', models.IntegerField(default=0, verbose_name='Jumlah Stok')),
                ('tanggal_masuk', models.DateField(default=django.utils.timezone.now, verbose_name='Tanggal Masuk')),
                ('foto_produk', models.ImageField(blank=True, null=True, upload_to='produk/', verbose_name='Foto Produk')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Barang',
                'verbose_name_plural': 'Data Barang',
                'ordering': ['-created_at'],
            },
        ),
    ]
