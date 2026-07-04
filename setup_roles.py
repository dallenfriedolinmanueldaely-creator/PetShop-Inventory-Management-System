import os
# pyrefly: ignore [missing-import]
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petshop_inventory.settings')
django.setup()

# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User, Group  # noqa: E402
# pyrefly: ignore [missing-import]
from inventory.models import UserProfile  # noqa: E402

for group_name in ('Owner', 'Admin', 'Staff'):
    Group.objects.get_or_create(name=group_name)

print("Groups Owner, Admin, dan Staff berhasil dibuat/diverifikasi.")

if not User.objects.filter(username='dllnfmd').exists():
    dllnfmd_user = User.objects.create_superuser(
        username='dllnfmd',
        password='owner123',
        first_name='Dallen',
        last_name='',
        email='dllnfmd@rawr.petshop.id'
    )

    profile, _ = UserProfile.objects.get_or_create(user=dllnfmd_user)
    profile.role = 'owner'
    profile.save()

    print("User 'dllnfmd' dibuat | role: Owner")

else:
    dllnfmd_user = User.objects.get(username='dllnfmd')
    profile, _ = UserProfile.objects.get_or_create(user=dllnfmd_user)

    if profile.role != 'owner':
        profile.role = 'owner'
        profile.save()

    print("[INFO] User 'dllnfmd' sudah ada, role dipastikan: Owner")


# ── OWNER

if not User.objects.filter(username='owner').exists():
    owner_user = User.objects.create_superuser(
        username='owner',
        password='owner123',
        first_name='Pet',
        last_name='Owner',
        email='owner@rawr.petshop.id'
    )

    profile, _ = UserProfile.objects.get_or_create(user=owner_user)
    profile.role = 'owner'
    profile.save()

    print("User 'owner' dibuat | role: Owner")

else:
    owner_user = User.objects.get(username='owner')
    profile, _ = UserProfile.objects.get_or_create(user=owner_user)

    if profile.role != 'owner':
        profile.role = 'owner'
        profile.save()

    print("[INFO] User 'owner' sudah ada, role dipastikan: Owner")


# ── ADMIN
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_user(
        username='admin',
        password='admin123',
        first_name='Admin',
        last_name='PetShop',
        email='admin@rawr.petshop.id'
    )

    profile, _ = UserProfile.objects.get_or_create(user=admin_user)
    profile.role = 'admin'
    profile.save()

    admin_user.groups.add(Group.objects.get(name='Admin'))

    print("User 'admin' dibuat | role: Admin")

else:
    admin_user = User.objects.get(username='admin')
    profile, _ = UserProfile.objects.get_or_create(user=admin_user)

    if profile.role != 'admin':
        profile.role = 'admin'
        profile.save()

    print("[INFO] User 'admin' sudah ada, role dipastikan: Admin")


# ── STAFF

if not User.objects.filter(username='staff1').exists():
    staff_user = User.objects.create_user(
        username='staff1',
        password='staff123',
        first_name='Staff',
        last_name='PetShop',
        email='staff1@rawr.petshop.id'
    )

    profile, _ = UserProfile.objects.get_or_create(user=staff_user)
    profile.role = 'staff'
    profile.save()

    staff_user.groups.add(Group.objects.get(name='Staff'))

    print("User 'staff1' dibuat | role: Staff")

else:
    staff_user = User.objects.get(username='staff1')
    profile, _ = UserProfile.objects.get_or_create(user=staff_user)

    if profile.role != 'staff':
        profile.role = 'staff'
        profile.save()

    print("[INFO] User 'staff1' sudah ada, role dipastikan: Staff")

print("\nRawrr!!!")
print("\n[INFO] Akun telah tersedia yaaak")