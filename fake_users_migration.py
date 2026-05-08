"""
Script fake migration cho users và tạo migrations cho các app khác.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Fake users migration
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app = 'users'")
    cursor.execute(
        "INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0001_initial', GETDATE())"
    )
    print("Đã fake: users.0001_initial")

print("Hoàn tất!")
