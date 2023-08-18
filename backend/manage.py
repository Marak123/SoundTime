#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import shutil

# def check_user():
#     from apis.user.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username="admin").exists() else print("`Admin` user exist")

def migration():
    TO_REMOVE = ['__pycache__', 'migrations']
    CATALOG_TO_CHECK = ['/django/apis/', '/django/core/']
    APPLICATION_NAME = ['apis_song', 'apis_auth', 'apis_user']
    FILE_EXECUTE = "python /django/manage.py"

    import subprocess
    from django.db import connection

    try:
        for folder in CATALOG_TO_CHECK:
            directories=[d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

            for d in directories:
                r = os.path.join(folder, d)
                if d in TO_REMOVE:
                    shutil.rmtree(r, ignore_errors=True)
                    print(f"Usunięto folder: {r}")
                else:
                    dirIn=[d for d in os.listdir(r) if os.path.isdir(os.path.join(r, d))]
                    for dIn in dirIn:
                        if dIn in TO_REMOVE:
                            shutil.rmtree(os.path.join(r, dIn), ignore_errors=True)
                            print(f"Usunięto folder: {os.path.join(r, dIn)}")


        # os.remove("./db.sqlite3")
        # print(f"Usunięto baze danych: ./db.sqlite3")

        # shutil.rmtree("../db_data", ignore_errors=True)
        # print(f"Usunięto baze danych: ../db_data")

        # shutil.rmtree("../data", ignore_errors=True)
        # print(f"Usunięto file storage: ../data")

        # os.system(f"django-admin sqlflush")

        try:
            # subprocess.run([FILE_EXECUTE + ' flush'], check=True, cwd='/django', shell=True)

            with connection.cursor() as cursor:
                cursor.execute("DROP SCHEMA public CASCADE;")
                cursor.execute("CREATE SCHEMA public;")

        except subprocess.CalledProcessError as e:
            print(f"Error clearing database: {e}")
            exit(-1)
        else:
            print("Database is clear.")

    except Exception as e:
        print("Wystąpił wyjątek:", e)
        exit(-1)

    # for app in APPLICATION_NAME:
    #     os.system(f"{FILE_EXECUTE} migrate { app } zero")

    for app in APPLICATION_NAME:
        os.system(f"{FILE_EXECUTE} makemigrations { app }")

    os.system(f"{FILE_EXECUTE} makemigrations")
    os.system(f"{FILE_EXECUTE} migrate")
    os.system(f'{FILE_EXECUTE} shell -c "from apis.user.models import User; User.objects.create_superuser("admin", "admin@example.com", "admin") if not User.objects.filter(username="admin").exists() else print("`Admin` user exist")')

def main():
    """Run administrative tasks."""

    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        os.system("pip manage.py runserver --bind 0.0.0.0:8000")
    elif len(sys.argv) > 1 and sys.argv[1] == "--migrate":
        migration()
    else:

        """
            DEFAULT FILE
        """

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)

        """
            DEFAULT FILE
        """


if __name__ == "__main__":
    main()
