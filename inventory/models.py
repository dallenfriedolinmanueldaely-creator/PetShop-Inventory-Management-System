from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def role_label(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

class Product(models.Model):
    PET_CHOICES = [
        ('Cat', 'Cat'),
        ('Dog', 'Dog'),
    ]

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Vitamins', 'Vitamins'),
        ('Grooming', 'Grooming'),
        ('Toys', 'Toys'),
        ('Accessories', 'Accessories'),
    ]

    name = models.CharField(max_length=200, verbose_name='Product Name')
    pet = models.CharField(max_length=10, choices=PET_CHOICES, default='Cat', verbose_name='Pet Type')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Price (Rp)')
    stock = models.IntegerField(default=0, verbose_name='Stock Quantity')
    date_added = models.DateField(default=timezone.now, verbose_name='Date Added')
    photo = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Product Photo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

        constraints = [
            models.CheckConstraint(check=models.Q(stock__gte=0), name='stock_cannot_be_negative')
        ]

    def __str__(self):
        return f"{self.name} ({self.pet} - {self.category})"

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    @property
    def stock_status(self):
        if self.stock == 0:
            return 'Out of Stock'
        elif self.stock <= 5:
            return 'Low Stock'
        else:
            return 'Available'

class StockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_in_records')
    quantity = models.PositiveIntegerField(verbose_name='Quantity In')
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"In: {self.product.name} +{self.quantity}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            with transaction.atomic():
                super().save(*args, **kwargs)
                Product.objects.filter(pk=self.product.pk).update(stock=models.F('stock') + self.quantity)
                self.product.refresh_from_db()
                TransactionHistory.objects.create(
                    product=self.product,
                    transaction_type='IN',
                    quantity=self.quantity,
                    notes=self.notes or f"Stock in: {self.product.name}",
                    recorded_by=self.recorded_by
                )
        else:
            super().save(*args, **kwargs)

class StockOut(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_out_records')
    quantity = models.PositiveIntegerField(verbose_name='Quantity Out')
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Out: {self.product.name} -{self.quantity}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            with transaction.atomic():
                current = Product.objects.select_for_update().get(pk=self.product.pk)
                if current.stock < self.quantity:
                    raise ValueError(
                        f"Stok tidak mencukupi! Tersedia: {current.stock}, diminta: {self.quantity}"
                    )
                super().save(*args, **kwargs)
                Product.objects.filter(pk=self.product.pk).update(stock=models.F('stock') - self.quantity)
                self.product.refresh_from_db()
                TransactionHistory.objects.create(
                    product=self.product,
                    transaction_type='OUT',
                    quantity=self.quantity,
                    notes=self.notes or f"Stock out: {self.product.name}",
                    recorded_by=self.recorded_by
                )
        else:
            super().save(*args, **kwargs)

class TransactionHistory(models.Model):
    TYPE_CHOICES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='transaction_history')
    transaction_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"[{self.transaction_type}] {self.product.name} {self.quantity}"

class ActivityLog(models.Model):
    ACTIVITY_CHOICES = [
        ('PRODUCT_ADDED', 'Product Added'),
        ('PRODUCT_UPDATED', 'Product Updated'),
        ('PRODUCT_DELETED', 'Product Deleted'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('EXPORT_CSV', 'Export CSV'),
        ('EXPORT_XLSX', 'Export Excel'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, blank=True)
    user_role = models.CharField(max_length=20, blank=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.activity_type}] {self.username} @ {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    @property
    def activity_label(self):
        return dict(self.ACTIVITY_CHOICES).get(self.activity_type, self.activity_type)
