#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import shutil


def migration():
    TO_REMOVE = ['__pycache__', 'migrations']
    CATALOG_TO_CHECK = ['.\\apis\\', '.\\core\\']
    APPLICATION_NAME = ['apis_song', 'apis_auth', 'apis_user']
    FILE_EXECUTE = ".\\env\\Scripts\\python311.exe .\\manage.py"

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


        os.remove("./db.sqlite3")
        print(f"Usunięto baze danych: ./db.sqlite3")
    except Exception as e:
        print("Wystąpił wyjątek:", e)

    for app in APPLICATION_NAME:
        os.system(f"{FILE_EXECUTE} makemigrations { app }")

    os.system(f"{FILE_EXECUTE} makemigrations")
    os.system(f"{FILE_EXECUTE} migrate")
    os.system(f'{FILE_EXECUTE} shell -c "from apis.user.models import User; User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin\')"')

def main():
    """Run administrative tasks."""

    komenda = sys.argv[1]

    if komenda == "--run":
        os.system(".\\env\\Scripts\\python311.exe .\\manage.py runserver")
    elif komenda == "--migrate":
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
