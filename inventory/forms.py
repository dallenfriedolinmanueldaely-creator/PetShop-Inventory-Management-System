from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Product, StockIn, StockOut
from .decorators import get_user_role


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'pet', 'category', 'price', 'stock', 'date_added', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Royal Canin Adult Cat'}),
            'pet': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '50000', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': '0'}),
            'date_added': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'name': 'Nama Produk',
            'pet': 'Jenis Hewan',
            'category': 'Kategori',
            'price': 'Harga (Rp)',
            'stock': 'Stok Awal',
            'date_added': 'Tanggal Ditambahkan',
            'photo': 'Foto Produk',
        }
        help_texts = {
            'stock': 'Stok awal saat produk ditambahkan. Ubah stok lewat transaksi Stock In / Stock Out.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if 'stock' in self.fields:
                del self.fields['stock']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Price cannot be negative!')
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('Stock cannot be negative!')
        return stock

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = ['product', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan jumlah stok masuk', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Catatan opsional'}),
        }
        labels = {'product': 'Pilih Produk', 'quantity': 'Jumlah Masuk', 'notes': 'Catatan'}

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty and qty <= 0:
            raise forms.ValidationError('Quantity must be greater than 0!')
        return qty

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = ['product', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan jumlah stok keluar', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Catatan opsional'}),
        }
        labels = {'product': 'Pilih Produk', 'quantity': 'Jumlah Keluar', 'notes': 'Catatan'}

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        if product and quantity:
            if quantity <= 0:
                raise forms.ValidationError('Quantity must be greater than 0!')
            if quantity > product.stock:
                raise forms.ValidationError(
                    f'Insufficient stock! Available: {product.stock}, requested: {quantity}'
                )
        return cleaned_data

class UserCreateForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ulangi password'}),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Peran (Role)',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    photo = forms.ImageField(
        required=False,
        label='Foto Profil',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama depan'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama belakang'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and get_user_role(user) != 'owner':
            choices = [(val, label) for val, label in self.ROLE_CHOICES if val != 'owner']
            self.fields['role'].choices = choices

    def clean_password1(self):
        p1 = self.cleaned_data.get('password1')
        if p1:
            validate_password(p1, self.instance)
        return p1

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Password tidak cocok!')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    new_password = forms.CharField(
        label='Password Baru (opsional)',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kosongkan jika tidak ingin mengubah'}),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Peran (Role)',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    photo = forms.ImageField(
        required=False,
        label='Foto Profil',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and get_user_role(user) != 'owner':
            choices = [(val, label) for val, label in self.ROLE_CHOICES if val != 'owner']
            self.fields['role'].choices = choices

    def clean_new_password(self):
        pwd = self.cleaned_data.get('new_password')
        if pwd:
            validate_password(pwd, self.instance)
        return pwd

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('new_password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
