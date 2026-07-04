import os
# pyrefly: ignore [missing-import]
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petshop_inventory.settings')
django.setup()

# pyrefly: ignore [missing-import]
from inventory.models import Product, TransactionHistory, StockIn, StockOut, ActivityLog  # noqa: E402

print(" Mengisi data contoh ke database...\n")

TransactionHistory.objects.all().delete()
StockIn.objects.all().delete()
StockOut.objects.all().delete()
ActivityLog.objects.all().delete()
Product.objects.all().delete()
print("  Data lama dihapus.\n")

products = [
    # MAKANAN KUCINGNYA
    {'name': 'Royal Canin Indoor Pouch 85g', 'pet': 'Cat', 'category': 'Food', 'price': 25000,   'stock': 50, 'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Indoor 400g',      'pet': 'Cat', 'category': 'Food', 'price': 79000,   'stock': 60, 'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Indoor 2kg',       'pet': 'Cat', 'category': 'Food', 'price': 339000,  'stock': 12, 'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Indoor 4kg',       'pet': 'Cat', 'category': 'Food', 'price': 649000,  'stock': 20, 'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Indoor 10kg',      'pet': 'Cat', 'category': 'Food', 'price': 1499000, 'stock': 5,  'date_added': date(2026, 6, 6)},
    {'name': 'Whiskas Tuna Pouch 85g',      'pet': 'Cat', 'category': 'Food', 'price': 12000,  'stock': 45, 'date_added': date(2026, 6, 6)},
    {'name': 'Whiskas Adult Tuna 480g',     'pet': 'Cat', 'category': 'Food', 'price': 38000,  'stock': 35, 'date_added': date(2026, 6, 6)},
    {'name': 'Whiskas Adult Tuna 1.2kg',    'pet': 'Cat', 'category': 'Food', 'price': 85000,  'stock': 1, 'date_added': date(2026, 6, 6)},
    {'name': 'Whiskas Adult Tuna 3kg',      'pet': 'Cat', 'category': 'Food', 'price': 195000, 'stock': 12, 'date_added': date(2026, 6, 6)},
    {'name': 'Whiskas Adult Tuna 7kg',      'pet': 'Cat', 'category': 'Food', 'price': 420000, 'stock': 6,  'date_added': date(2026, 6, 6)},
    {'name': 'Me-O Tuna Pouch 80g',         'pet': 'Cat', 'category': 'Food', 'price': 10000,  'stock': 50, 'date_added': date(2026, 6, 6)},
    {'name': 'Me-O Adult Tuna 400g',        'pet': 'Cat', 'category': 'Food', 'price': 30000,  'stock': 40, 'date_added': date(2026, 6, 6)},
    {'name': 'Me-O Adult Tuna 1.1kg',       'pet': 'Cat', 'category': 'Food', 'price': 78000,  'stock': 30, 'date_added': date(2026, 6, 6)},
    {'name': 'Me-O Adult Tuna 3kg',         'pet': 'Cat', 'category': 'Food', 'price': 175000, 'stock': 0, 'date_added': date(2026, 6, 6)},
    {'name': 'Me-O Adult Tuna 7kg',         'pet': 'Cat', 'category': 'Food', 'price': 390000, 'stock': 5,  'date_added': date(2026, 6, 6)},

    # MAKANAN ANJINGNYA
    {'name': 'Royal Canin Mini Adult 800g',  'pet': 'Dog', 'category': 'Food', 'price': 115000,  'stock': 50, 'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Mini Adult 2kg',   'pet': 'Dog', 'category': 'Food', 'price': 265000,  'stock': 15, 'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Medium Adult 4kg', 'pet': 'Dog', 'category': 'Food', 'price': 485000,  'stock': 25, 'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Maxi Adult 10kg',  'pet': 'Dog', 'category': 'Food', 'price': 1085000, 'stock': 6,  'date_added': date(2026, 6, 6)},
    {'name': 'Royal Canin Maxi Adult 15kg',  'pet': 'Dog', 'category': 'Food', 'price': 1625000, 'stock': 2,  'date_added': date(2026, 6, 6)},
    {'name': 'Pedigree Adult Beef 400g',    'pet': 'Dog', 'category': 'Food', 'price': 28000,  'stock': 45, 'date_added': date(2026, 6, 6)},
    {'name': 'Pedigree Adult Beef 1.5kg',   'pet': 'Dog', 'category': 'Food', 'price': 95000,  'stock': 30, 'date_added': date(2026, 6, 6)},
    {'name': 'Pedigree Adult Beef 3kg',     'pet': 'Dog', 'category': 'Food', 'price': 185000, 'stock': 18, 'date_added': date(2026, 6, 6)},
    {'name': 'Pedigree Adult Beef 10kg',    'pet': 'Dog', 'category': 'Food', 'price': 525000, 'stock': 8,  'date_added': date(2026, 6, 6)},
    {'name': 'Pedigree Adult Beef 20kg',    'pet': 'Dog', 'category': 'Food', 'price': 975000, 'stock': 3,  'date_added': date(2026, 6, 6)},
    {'name': 'Pro Plan Puppy Chicken 800g', 'pet': 'Dog', 'category': 'Food', 'price': 95000,  'stock': 25, 'date_added': date(2026, 6, 6)},
    {'name': 'Pro Plan Puppy Chicken 2.5kg', 'pet': 'Dog', 'category': 'Food', 'price': 255000, 'stock': 0, 'date_added': date(2026, 6, 6)},
    {'name': 'Pro Plan Adult 3kg',          'pet': 'Dog', 'category': 'Food', 'price': 325000, 'stock': 15, 'date_added': date(2026, 6, 6)},
    {'name': 'Pro Plan Adult 7kg',          'pet': 'Dog', 'category': 'Food', 'price': 675000, 'stock': 10, 'date_added': date(2026, 6, 6)},
    {'name': 'Pro Plan Adult 15kg',         'pet': 'Dog', 'category': 'Food', 'price': 1295000, 'stock': 4,  'date_added': date(2026, 6, 6)},

    # VITAMIN KUCINGNYA
    {'name': 'Nutri-Vet Multi-Vite Cat',     'pet': 'Cat', 'category': 'Vitamins', 'price': 85000,  'stock': 25, 'date_added': date(2026, 6, 6)},
    {'name': 'Virbac Nutri Plus Gel Cat',    'pet': 'Cat', 'category': 'Vitamins', 'price': 145000, 'stock': 18, 'date_added': date(2026, 6, 6)},
    {'name': 'Beaphar Top 10 Cat',           'pet': 'Cat', 'category': 'Vitamins', 'price': 125000, 'stock': 20, 'date_added': date(2026, 6, 6)},
    {'name': 'Vetoquinol Enisyl-F Cat',      'pet': 'Cat', 'category': 'Vitamins', 'price': 185000, 'stock': 5,  'date_added': date(2026, 6, 6)},
    {'name': 'Nutriplus Gel Cat',            'pet': 'Cat', 'category': 'Vitamins', 'price': 140000, 'stock': 15, 'date_added': date(2026, 6, 6)},

    # VITAMIN ANJINGNYA
    {'name': 'Nutri-Vet Multi-Vite Dog',     'pet': 'Dog', 'category': 'Vitamins', 'price': 95000,  'stock': 22, 'date_added': date(2026, 6, 6)},
    {'name': 'Virbac Nutri Plus Gel Dog',    'pet': 'Dog', 'category': 'Vitamins', 'price': 145000, 'stock': 16, 'date_added': date(2026, 6, 6)},
    {'name': 'Beaphar Top 10 Dog',           'pet': 'Dog', 'category': 'Vitamins', 'price': 135000, 'stock': 19, 'date_added': date(2026, 6, 6)},
    {'name': 'VetriScience Canine Plus',     'pet': 'Dog', 'category': 'Vitamins', 'price': 215000, 'stock': 10, 'date_added': date(2026, 6, 6)},
    {'name': 'NaturVet All-In-One Dog',      'pet': 'Dog', 'category': 'Vitamins', 'price': 175000, 'stock': 14, 'date_added': date(2026, 6, 6)},

    # GROOMING KUCINGNYA
    {'name': 'Bio-Groom Cat Shampoo',        'pet': 'Cat', 'category': 'Grooming', 'price': 110000, 'stock': 20, 'date_added': date(2026, 6, 6)},
    {'name': 'Beaphar Cat Shampoo',          'pet': 'Cat', 'category': 'Grooming', 'price': 85000,  'stock': 24, 'date_added': date(2026, 6, 6)},
    {'name': 'TropiClean Cat Shampoo',       'pet': 'Cat', 'category': 'Grooming', 'price': 145000, 'stock': 15, 'date_added': date(2026, 6, 6)},

    # GROOMING ANJINGNYA
    {'name': 'Bio-Groom Dog Shampoo',        'pet': 'Dog', 'category': 'Grooming', 'price': 115000, 'stock': 18, 'date_added': date(2026, 6, 6)},
    {'name': 'Beaphar Dog Shampoo',          'pet': 'Dog', 'category': 'Grooming', 'price': 90000,  'stock': 8,  'date_added': date(2026, 6, 6)},
    {'name': 'TropiClean Dog Shampoo',       'pet': 'Dog', 'category': 'Grooming', 'price': 150000, 'stock': 14, 'date_added': date(2026, 6, 6)},

    # TOYS KUCINGNYA
    {'name': 'Cat Teaser Feather Wand',      'pet': 'Cat', 'category': 'Toys', 'price': 45000,  'stock': 3,  'date_added': date(2026, 6, 6)},
    {'name': 'Interactive Cat Ball',         'pet': 'Cat', 'category': 'Toys', 'price': 65000,  'stock': 4,  'date_added': date(2026, 6, 6)},
    {'name': 'Catnip Plush Mouse',           'pet': 'Cat', 'category': 'Toys', 'price': 35000,  'stock': 6,  'date_added': date(2026, 6, 6)},
    {'name': 'Tunnel Play Cat Toy',          'pet': 'Cat', 'category': 'Toys', 'price': 125000, 'stock': 9,  'date_added': date(2026, 6, 6)},
    {'name': 'Interactive Laser Cat Toy',    'pet': 'Cat', 'category': 'Toys', 'price': 175000, 'stock': 0, 'date_added': date(2026, 6, 6)},

    # TOYS ANJINGNYA
    {'name': 'Kong Classic Dog Toy',         'pet': 'Dog', 'category': 'Toys', 'price': 145000, 'stock': 18, 'date_added': date(2026, 6, 6)},
    {'name': 'Rope Tug Dog Toy',             'pet': 'Dog', 'category': 'Toys', 'price': 55000,  'stock': 28, 'date_added': date(2026, 6, 6)},
    {'name': 'Squeaky Bone Dog Toy',         'pet': 'Dog', 'category': 'Toys', 'price': 65000,  'stock': 24, 'date_added': date(2026, 6, 6)},
    {'name': 'Interactive Treat Puzzle',     'pet': 'Dog', 'category': 'Toys', 'price': 185000, 'stock': 12, 'date_added': date(2026, 6, 6)},
    {'name': 'Rubber Chew Ball',             'pet': 'Dog', 'category': 'Toys', 'price': 85000,  'stock': 20, 'date_added': date(2026, 6, 6)},

    # AKSESORIS KUCINGNYA
    {'name': 'Cat Collar Bell Pink',         'pet': 'Cat', 'category': 'Accessories', 'price': 35000,  'stock': 35, 'date_added': date(2026, 6, 6)},
    {'name': 'Reflective Cat Collar',        'pet': 'Cat', 'category': 'Accessories', 'price': 45000,  'stock': 3, 'date_added': date(2026, 6, 6)},
    {'name': 'Cat Harness Set',              'pet': 'Cat', 'category': 'Accessories', 'price': 95000,  'stock': 1, 'date_added': date(2026, 6, 6)},
    {'name': 'Portable Cat Carrier',         'pet': 'Cat', 'category': 'Accessories', 'price': 275000, 'stock': 8,  'date_added': date(2026, 6, 6)},
    {'name': 'Cat ID Tag Stainless',         'pet': 'Cat', 'category': 'Accessories', 'price': 25000,  'stock': 40, 'date_added': date(2026, 6, 6)},

    # AKSESORIS ANJINGNYA
    {'name': 'Dog Collar Leather',           'pet': 'Dog', 'category': 'Accessories', 'price': 85000,  'stock': 5, 'date_added': date(2026, 6, 6)},
    {'name': 'Reflective Dog Leash',         'pet': 'Dog', 'category': 'Accessories', 'price': 75000,  'stock': 2,  'date_added': date(2026, 6, 6)},
    {'name': 'Dog Harness Premium',          'pet': 'Dog', 'category': 'Accessories', 'price': 145000, 'stock': 18, 'date_added': date(2026, 6, 6)},
    {'name': 'Portable Dog Carrier',         'pet': 'Dog', 'category': 'Accessories', 'price': 325000, 'stock': 6,  'date_added': date(2026, 6, 6)},
    {'name': 'Dog ID Tag Stainless',         'pet': 'Dog', 'category': 'Accessories', 'price': 30000,  'stock': 3, 'date_added': date(2026, 6, 6)},
]

for i, data in enumerate(products, 1):
    p = Product.objects.create(**data)
    if p.stock == 0:
        status = 'Out of Stock'
    elif p.stock <= 5:
        status = '[!] Low Stock  '
    else:
        status = 'OK          '
    print(f"  [{i:02d}] {status}  {p.name:<35} ({p.pet} / {p.category}) - Stok: {p.stock}")

total = Product.objects.count()
low = Product.objects.filter(stock__gt=0, stock__lte=5).count()
out = Product.objects.filter(stock=0).count()

print(f"""

  Miawww! {total} produk berhasil dimasukkan.
      Stok OK      : {total - low - out} produk
      [!] Low Stock   : {low} produk
      Out of Stock : {out} produk

      thank you have a nice day!!!
""")
