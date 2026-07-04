from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User

from django.db import IntegrityError

from django.db.models.deletion import ProtectedError

from django.template.loader import render_to_string

from django.urls import reverse
from decimal import Decimal
from datetime import date
from .models import Product, StockIn, StockOut, TransactionHistory, UserProfile
from .forms import ProductForm, UserCreateForm
from .algorithms import (
    linear_search, binary_search_by_nama,
    bubble_sort, selection_sort, insertion_sort
)

class PetshopDSATests(TestCase):
    def setUp(self):
        self.p1 = Product.objects.create(name="Royal Canin Fit 32", pet="Cat", category="Food", price=Decimal("79000"), stock=10)
        self.p2 = Product.objects.create(name="Royal Canin Kitten", pet="Cat", category="Food", price=Decimal("85000"), stock=5)
        self.p3 = Product.objects.create(name="Whiskas Tuna", pet="Cat", category="Food", price=Decimal("38000"), stock=20)
        self.p4 = Product.objects.create(name="Pedigree Puppy", pet="Dog", category="Food", price=Decimal("95000"), stock=3)
        self.p5 = Product.objects.create(name="Beaphar Vitamin Dog", pet="Dog", category="Vitamins", price=Decimal("125000"), stock=15)
        self.user = User.objects.create_user(username='teststaff', password='testpassword')

    def test_linear_search(self):
        products = Product.objects.all()
        results = linear_search(products, "royal", field="name")
        self.assertEqual(len(results), 2)
        names = [p.name for p in results]
        self.assertIn("Royal Canin Fit 32", names)
        self.assertIn("Royal Canin Kitten", names)

        results_cat = linear_search(products, "food", field="category")
        self.assertEqual(len(results_cat), 4)

        results_ws = linear_search(products, "  Whiskas   ", field="name")
        self.assertEqual(len(results_ws), 1)

    def test_binary_search_prefix(self):
        products = Product.objects.all()

        results = binary_search_by_nama(products, "Royal")
        self.assertEqual(len(results), 2)
        names = [p.name for p in results]
        self.assertIn("Royal Canin Fit 32", names)
        self.assertIn("Royal Canin Kitten", names)

        results_exact = binary_search_by_nama(products, "Whiskas Tuna")
        self.assertEqual(len(results_exact), 1)
        self.assertEqual(results_exact[0].name, "Whiskas Tuna")

        results_none = binary_search_by_nama(products, "Nonexistent")
        self.assertEqual(len(results_none), 0)

    def test_bubble_sort(self):
        products = list(Product.objects.all())

        sorted_by_price_asc = bubble_sort(products, field="price", ascending=True)
        prices_asc = [p.price for p in sorted_by_price_asc]
        self.assertEqual(prices_asc, sorted(prices_asc))

        sorted_by_stock_desc = bubble_sort(products, field="stock", ascending=False)
        stocks_desc = [p.stock for p in sorted_by_stock_desc]
        self.assertEqual(stocks_desc, sorted(stocks_desc, reverse=True))

    def test_selection_sort(self):
        products = list(Product.objects.all())

        sorted_by_price_asc = selection_sort(products, field="price", ascending=True)
        prices_asc = [p.price for p in sorted_by_price_asc]
        self.assertEqual(prices_asc, sorted(prices_asc))

        sorted_by_name_desc = selection_sort(products, field="name", ascending=False)
        names_desc = [p.name.lower() for p in sorted_by_name_desc]
        self.assertEqual(names_desc, sorted(names_desc, reverse=True))

    def test_insertion_sort(self):
        products = list(Product.objects.all())

        sorted_by_stock_asc = insertion_sort(products, field="stock", ascending=True)
        stocks_asc = [p.stock for p in sorted_by_stock_asc]
        self.assertEqual(stocks_asc, sorted(stocks_asc))

        sorted_by_name_asc = insertion_sort(products, field="name", ascending=True)
        names_asc = [p.name.lower() for p in sorted_by_name_asc]
        self.assertEqual(names_asc, sorted(names_asc))

    def test_stock_in_transaction_adds_stock(self):
        initial_stock = self.p1.stock
        qty_to_add = 15

        StockIn.objects.create(
            product=self.p1,
            quantity=qty_to_add,
            recorded_by=self.user,
            notes="Testing Stock In"
        )

        self.p1.refresh_from_db()
        self.assertEqual(self.p1.stock, initial_stock + qty_to_add)

        tx_history = TransactionHistory.objects.filter(product=self.p1, transaction_type='IN').first()
        self.assertIsNotNone(tx_history)
        self.assertEqual(tx_history.quantity, qty_to_add)

    def test_stock_out_transaction_reduces_stock(self):
        initial_stock = self.p1.stock
        qty_to_deduct = 4

        StockOut.objects.create(
            product=self.p1,
            quantity=qty_to_deduct,
            recorded_by=self.user,
            notes="Testing Stock Out"
        )

        self.p1.refresh_from_db()
        self.assertEqual(self.p1.stock, initial_stock - qty_to_deduct)

        tx_history = TransactionHistory.objects.filter(product=self.p1, transaction_type='OUT').first()
        self.assertIsNotNone(tx_history)
        self.assertEqual(tx_history.quantity, qty_to_deduct)

    def test_stock_out_transaction_raises_value_error_on_insufficient_stock(self):
        initial_stock = self.p1.stock
        qty_excess = initial_stock + 10

        with self.assertRaises(ValueError):
            StockOut.objects.create(
                product=self.p1,
                quantity=qty_excess,
                recorded_by=self.user,
                notes="Testing Stock Out Excess"
            )

        self.p1.refresh_from_db()
        self.assertEqual(self.p1.stock, initial_stock)

    def test_product_form_edit_excludes_stock(self):
        form_data = {
            'name': 'Updated Product Name',
            'pet': self.p1.pet,
            'category': self.p1.category,
            'price': self.p1.price,
            'date_added': self.p1.date_added,
        }
        form = ProductForm(form_data, instance=self.p1)
        self.assertTrue(form.is_valid(), form.errors)
        updated_product = form.save()
        self.assertEqual(updated_product.name, 'Updated Product Name')
        self.assertEqual(updated_product.stock, 10)

    def test_product_form_creation_negative_stock(self):
        form_data = {
            'name': 'New Product',
            'pet': 'Cat',
            'category': 'Food',
            'price': Decimal('5000'),
            'stock': -5,
            'date_added': date.today(),
        }
        form = ProductForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)
        self.assertEqual(form.errors['stock'][0], 'Stock cannot be negative!')

    def test_weak_password_validation_in_create_form(self):
        form_data = {
            'username': 'newuser123',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@rawr.petshop.id',
            'password1': '123',
            'password2': '123',
            'role': 'staff',
        }
        form = UserCreateForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_privilege_escalation_in_create_form(self):
        admin_user = User.objects.create_user(username='subadmin', password='testpassword123')
        profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        profile.role = 'admin'
        profile.save()

        form = UserCreateForm(user=admin_user)
        role_choices = dict(form.fields['role'].choices)
        self.assertNotIn('owner', role_choices)
        self.assertIn('admin', role_choices)
        self.assertIn('staff', role_choices)

    def test_negative_stock_database_constraint(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Illegal Negative Stock Product",
                pet="Cat",
                category="Food",
                price=Decimal("100"),
                stock=-10
            )

    def test_product_deletion_integrity_protection(self):
        StockIn.objects.create(
            product=self.p1,
            quantity=5,
            recorded_by=self.user,
            notes="Initial Protection Test In"
        )

        with self.assertRaises(ProtectedError):
            self.p1.delete()

    def test_product_form_template_renders(self):
        factory = RequestFactory()
        request = factory.get('/products/add/')
        request.user = self.user

        class MockResolverMatch:
            url_name = 'add_product'
        request.resolver_match = MockResolverMatch()

        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        profile.role = 'admin'
        profile.save()

        context = {
            'form': ProductForm(),
            'action': 'Add',
            'user_role': 'admin',
            'page_title': 'Add Product',
        }
        html = render_to_string('inventory/product_form.html', context, request=request)
        self.assertIn('<form', html)
        self.assertIn('name="name"', html)
        self.assertIn('action', context)

    def test_logout_post_only(self):
        self.client.login(username='teststaff', password='testpassword')

        response_get = self.client.get(reverse('logout'))
        self.assertEqual(response_get.status_code, 405)

        response_post = self.client.post(reverse('logout'))
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse('login'))

    def test_stock_out_add_view_handles_validation_error(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        profile.role = 'staff'
        profile.save()

        self.client.login(username='teststaff', password='testpassword')

        response = self.client.post(reverse('stock_out_add'), {
            'product': self.p1.pk,
            'quantity': self.p1.stock + 10,
            'notes': 'Exceeding'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Insufficient stock")
