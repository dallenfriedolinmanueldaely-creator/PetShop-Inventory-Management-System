# 🐾 Sistem Manajemen Inventori Petshop Berbasis Web
### Menggunakan Algoritma Searching dan Sorting (Struktur Data & Algoritma)

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Framework](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite Database](https://img.shields.io/badge/SQLite-3.0+-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap Styling](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](#)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](#)
[![Git Version Control](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](#)
[![GitHub Repository](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](#)

*An aesthetic, high-performance, and feature-rich Web-based Inventory Management System designed specially for pet shops, powered by Django and enhanced with custom-implemented Searching and Sorting algorithms.* 🐈🐶
</div>

---

## 📖 Project Overview

This repository hosts a web-based **Petshop Inventory Management System**. Built to fulfill the final project requirements for the **Data Structures and Algorithms (Struktur Data & Algoritma)** course, this system highlights how core algorithms (like Linear/Binary Search and Bubble/Selection/Insertion Sort) are applied to build robust, interactive, and optimized web interfaces.

The application enables petshop owners and staff to manage product inventories (specifically for Cat & Dog products such as Food, Vitamins, Grooming, Toys, and Accessories), log transaction history (Stock In/Out), view graphical analytics, and perform comprehensive exports to Excel and CSV.

---

## ✨ Key Features

- **📊 Premium Interactive Dashboard**: Beautiful stats cards displaying total products, active stock volume, low/out-of-stock items, and visual category breakdown utilizing **Chart.js**.
- **🔍 Advanced Search & Filter System**: Search items by name, category, or pet type using either **Linear Search** or **Binary Search**.
- **🔄 Algorithmic Sorting**: Sort the catalog dynamically by Name, Price, or Stock using custom-coded sorting routines: **Bubble Sort**, **Selection Sort**, and **Insertion Sort**.
- **🪵 Transaction Ledger**: Atomic Stock In and Stock Out records keeping database integrity in check. It raises validation errors if staff try to deduct more stock than available.
- **📄 Professional Reports**: Single-click downloads for inventory logs as custom-formatted CSV or highly stylized Excel (`.xlsx`) files.
- **🛡️ Activity Auditing**: A built-in user activity logging system (login/logout tracker, product modifications, and file export logs).
- **👥 Role-Based Access Control (RBAC)**: Secure middlewares and custom decorators implementing specific privileges for **Owner**, **Admin**, and **Staff**.

---

## 🖼️ Application Preview

### 🖥️ Dashboard View
![Dashboard Preview](https://raw.githubusercontent.com/username/repo-name/main/docs/screenshots/dashboard.png)
*A sleek, modern administrative dashboard with real-time stock analytics and charts.*

### 📦 Product Catalog
![Product Catalog Preview](https://raw.githubusercontent.com/username/repo-name/main/docs/screenshots/catalog.png)
*Advanced filters for search fields, sorting fields, sorting order, and choice of algorithms.*

---

## 🛠️ Tech Stack & Dependencies

- **Backend Logic**: Python 3.11+
- **Web Framework**: Django 4.2.x (with custom Class/Function decorators for RBAC)
- **Database Engine**: SQLite3
- **Frontend Styling**: Bootstrap 5.3, Bootstrap Icons, Animate.css, & custom premium CSS variables.
- **Visualization**: Chart.js (via CDN)
- **Data Export Utilities**: `openpyxl` & python native `csv` package

---

## 🧮 Understanding the Algorithms

Rather than relying on database-level processing (SQL commands like `ORDER BY` or `LIKE`), searching and sorting in this catalog are processed in python memory using custom-designed algorithms:

### 1. Searching Algorithms
<details>
<summary><b>🔍 Linear Search <code>O(n)</code></b></summary>

- **How it works**: Traverses the list of products element by element from beginning to end to find matches.
- **Pros**: Very robust; works on unsorted lists and handles any data field.
- **Cons**: Sluggish for large datasets because it scales linearly with the number of products.
</details>

<details>
<summary><b>⚡ Binary Search <code>O(log n)</code></b></summary>

- **How it works**: Repeatedly divides the search interval in half. Requires the product list to be sorted by **Name** beforehand.
- **Pros**: Extremely fast search operations, even on massive data ranges.
- **Cons**: Only applicable for the **Name** search field in this implementation.
</details>

### 2. Sorting Algorithms
<details>
<summary><b>🫧 Bubble Sort <code>O(n²)</code></b></summary>

- **How it works**: Compares adjacent products and swaps them if they are in the wrong order. This repeats until no more swaps are needed.
- **Pros**: Easy to implement; has early-termination optimization if the data is already sorted.
- **Cons**: High average-case time complexity, making it slow for massive product catalogs.
</details>

<details>
<summary><b>📌 Selection Sort <code>O(n²)</code></b></summary>

- **How it works**: Divides the list into a sorted part and unsorted part. Repeatedly finds the minimum/maximum element from the unsorted part and swaps it to the front.
- **Pros**: Performs a minimal number of writes/swaps compared to Bubble Sort.
- **Cons**: Always runs in $O(n^2)$ time regardless of the initial order.
</details>

<details>
<summary><b>🃏 Insertion Sort <code>O(n²)</code></b></summary>

- **How it works**: Builds the sorted list one item at a time by sliding each product into its correct position relative to the already sorted portion.
- **Pros**: Highly efficient for small datasets or lists that are already partially sorted.
- **Cons**: Inefficient for completely unsorted, random, or reversed datasets.
</details>

---

## 💻 Algorithmic Integration

All filters and catalog configurations are parsed inside `inventory/views.py` through the function `_apply_product_filters()`:

```python
# Extract parameters from GET request
keyword = request.GET.get('q', '').strip()
search_algo = request.GET.get('search_algo', 'linear')
sort_algo = request.GET.get('sort_algo', 'bubble')
sort_by = request.GET.get('sort_by', '')
sort_order = request.GET.get('sort_order', 'asc')

# 1. Search Stage
if keyword:
    if search_algo == 'binary' and search_field == 'name':
        products = binary_search_by_nama(products, keyword)
    else:
        products = linear_search(products, keyword, field=search_field)

# 2. Sort Stage
if sort_by:
    ascending = (sort_order == 'asc')
    if sort_algo == 'selection':
        products = selection_sort(products, field=sort_by, ascending=ascending)
    elif sort_algo == 'insertion':
        products = insertion_sort(products, field=sort_by, ascending=ascending)
    else:
        products = bubble_sort(products, field=sort_by, ascending=ascending)
```

---

## 📂 Folder Structure

```bash
Pet Shop Management System/
│
├── inventory/                  # Core App Folder
│   ├── migrations/             # Database Schemas
│   ├── static/                 # Static Assets (Images, Logo, Stylesheets)
│   ├── templates/              # HTML Templates (Inheriting base.html)
│   ├── admin.py                # Admin Registration
│   ├── algorithms.py           # Custom Searching & Sorting Implementation
│   ├── constants.py            # Global Constants (e.g. Low stock threshold)
│   ├── context_processors.py   # Global Context Variables (Alert indicators)
│   ├── decorators.py           # Custom decorators for RBAC (Role authorization)
│   ├── forms.py                # Form definitions (Products, User Create/Edit)
│   ├── models.py               # Models definition (Product, Transactions, Logs)
│   ├── urls.py                 # App Route URL configurations
│   ├── views.py                # App Logic and Controller views
│   └── tests.py                # App Test Suite
│
├── petshop_inventory/          # Project settings module
│   ├── settings.py             # Django main settings
│   ├── urls.py                 # Root URL Router
│   └── wsgi.py                 # WSGI configurations
│
├── db.sqlite3                  # Database File
├── manage.py                   # Django CLI Runner
├── requirements.txt            # Package Dependencies
├── seed_data.py                # Database Seeding Utility
└── setup_roles.py              # User Accounts and Groups Setup Utility
```

---

## 🗄️ Database Schema (ERD)

The database schema is highly optimized, linking core models to ensure transactional safety and comprehensive audit trails.

```
+------------------+         +------------------+         +--------------------+
|     Product      | <-----+ |     StockIn      | <-----+ | TransactionHistory |
+------------------+         +------------------+         +--------------------+
| pk (ID)          |         | pk (ID)          |         | pk (ID)            |
| name             |         | product_id (FK)  |         | product_id (FK)    |
| pet              |         | quantity         |         | transaction_type   |
| category         |         | date             |         | quantity           |
| price            |         | notes            |         | date               |
| stock            |         | recorded_by (FK) |         | notes              |
| photo            |         +------------------+         | recorded_by (FK)   |
| date_added       |                                      +--------------------+
+------------------+         +------------------+
                             |     StockOut     |
                             +------------------+
                             | pk (ID)          |
                             | product_id (FK)  |
                             | quantity         |
                             | date             |
                             | notes            |
                             | recorded_by (FK) |
                             +------------------+
```
*(An image representation can be placed under `docs/erd.png` inside your repository).*

---

## 🚀 Setup & Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/username/repo-name.git
cd "Pet Shop Manajement System"
```

### 2. Configure Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (CMD):
.\venv\Scripts\activate.bat
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Package Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Setup Default User Roles & Groups
Initialize administrative and staff groups and create default accounts:
```bash
python setup_roles.py
```

### 6. Seed Sample Data
Populate the database with 66 realistic products and clean up old records:
```bash
python seed_data.py
```

---

## 🎮 Running the Application

Start the local development server:
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/` to access the application.

---

## 🔑 Demo Access Credentials

The roles setup utility provides these pre-seeded accounts for testing:

| Username | Password | Role | Description |
| :--- | :--- | :--- | :--- |
| **`owner`** | `owner123` | **Owner** | Full privileges including User Management |
| **`admin`** | `admin123` | **Admin** | Managing products and transactions, cannot edit Owner |
| **`staff1`**| `staff123` | **Staff** | Restricted to inventory view and Stock In/Out |

### 👥 User Roles Specifications
1. **👑 Owner**: The master role. Can add new admins, modify all users, view activity logs, export data, and delete any items.
2. **🛡️ Admin**: Can view logs and export product data. Can create, edit, and delete staff accounts. Admins are blocked from altering the Owner's account.
3. **💼 Staff**: Dedicated field operators. Restricted to recording incoming/outgoing inventory items. Staff have no access to the user directory, admin configurations, or activity logs.

---

## 🧑‍💻 Contributors & Team

Meet the minds behind this project:

- **Dallen Friedolin Manuel Daely** — Developer & Algorithms Architect
- **Nabila F Andina Lubis** — UI/UX Designer & Templates Developer
- **Hani Septiani** — Database Administrator & Quality Assurance

---

## 💝 Acknowledgement

Special thanks to our course advisors and instructors for guidance throughout the semester. Built with love, a furry cat by our side, and a warm cup of coffee. ☕🐱

*Copyright &copy; 2026. All rights reserved.*
