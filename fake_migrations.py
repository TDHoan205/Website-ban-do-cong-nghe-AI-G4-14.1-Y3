"""
Script để fake migrations cho database đã có sẵn.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Lấy danh sách tất cả migration đã apply trong database
with connection.cursor() as cursor:
    cursor.execute("SELECT app, name FROM django_migrations")
    applied = set((row[0], row[1]) for row in cursor.fetchall())

print("Đã apply:", applied)

# Các migrations cần fake
migrations_to_fake = [
    ('contenttypes', '0001_initial'),
    ('contenttypes', '0002_remove_content_type_name'),
    ('auth', '0001_initial'),
    ('auth', '0002_alter_permission_name_max_length'),
    ('auth', '0003_alter_user_email_max_length'),
    ('auth', '0004_alter_user_username_opts'),
    ('auth', '0005_alter_user_last_login_null'),
    ('auth', '0006_require_contenttypes_0002'),
    ('auth', '0007_alter_validators_add_error_messages'),
    ('auth', '0008_alter_user_username_max_length'),
    ('auth', '0009_alter_user_last_name_max_length'),
    ('auth', '0010_alter_group_name_max_length'),
    ('auth', '0011_update_proxy_permissions'),
    ('auth', '0012_alter_user_first_name_max_length'),
    ('admin', '0001_initial'),
    ('admin', '0002_logentry_remove_auto_add'),
    ('admin', '0003_logentry_add_action_flag_choices'),
    ('sessions', '0001_initial'),
]

with connection.cursor() as cursor:
    for app, name in migrations_to_fake:
        if (app, name) not in applied:
            cursor.execute(
                "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, GETDATE())",
                [app, name]
            )
            print(f"Đã fake: {app}.{name}")
        else:
            print(f"Đã tồn tại: {app}.{name}")

print("\nHoàn tất!")
