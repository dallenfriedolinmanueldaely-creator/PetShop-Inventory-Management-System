from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    """
    Migrasi: Tambah field hewan pada Barang,
    tambah model BarangMasuk, BarangKeluar, dan HistoriTransaksi.
    """

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Tambah field hewan ke model Barang
        migrations.AddField(
            model_name='barang',
            name='hewan',
            field=models.CharField(
                choices=[('Kucing', ' Kucing'), ('Anjing', ' Anjing')],
                default='Kucing',
                max_length=10,
                verbose_name='Jenis Hewan'
            ),
        ),

        # Model BarangMasuk
        migrations.CreateModel(
            name='BarangMasuk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.PositiveIntegerField(verbose_name='Jumlah Masuk')),
                ('tanggal', models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Transaksi')),
                ('keterangan', models.TextField(blank=True, null=True, verbose_name='Keterangan')),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi_masuk', to='inventory.barang', verbose_name='Barang')),
                ('dicatat_oleh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Dicatat Oleh')),
            ],
            options={'ordering': ['-tanggal'], 'verbose_name': 'Barang Masuk', 'verbose_name_plural': 'Data Barang Masuk'},
        ),

        # Model BarangKeluar
        migrations.CreateModel(
            name='BarangKeluar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.PositiveIntegerField(verbose_name='Jumlah Keluar')),
                ('tanggal', models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Transaksi')),
                ('keterangan', models.TextField(blank=True, null=True, verbose_name='Keterangan')),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi_keluar', to='inventory.barang', verbose_name='Barang')),
                ('dicatat_oleh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Dicatat Oleh')),
            ],
            options={'ordering': ['-tanggal'], 'verbose_name': 'Barang Keluar', 'verbose_name_plural': 'Data Barang Keluar'},
        ),

        # Model HistoriTransaksi
        migrations.CreateModel(
            name='HistoriTransaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis', models.CharField(choices=[('IN', ' Masuk'), ('OUT', ' Keluar')], max_length=3, verbose_name='Jenis Transaksi')),
                ('jumlah', models.PositiveIntegerField(verbose_name='Jumlah')),
                ('tanggal', models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Transaksi')),
                ('keterangan', models.TextField(blank=True, null=True, verbose_name='Keterangan')),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histori', to='inventory.barang', verbose_name='Barang')),
                ('dicatat_oleh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Dicatat Oleh')),
            ],
            options={'ordering': ['-tanggal'], 'verbose_name': 'Histori Transaksi', 'verbose_name_plural': 'Histori Transaksi'},
        ),
    ]
