"""
Django command to wait for the database to be available.
"""
import time
import os
import sys
import shutil
import subprocess

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""

        TO_REMOVE = ['__pycache__', 'migrations']
        CATALOG_TO_CHECK = ['/django/apis/', '/django/core/']
        APPLICATION_NAME = ['apis_song', 'apis_auth', 'apis_user']
        FILE_EXECUTE = "python /django/manage.py"


        try:
            for folder in CATALOG_TO_CHECK:
                directories=[d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

                for d in directories:
                    r = os.path.join(folder, d)
                    if d in TO_REMOVE:
                        shutil.rmtree(r, ignore_errors=True)
                        self.stdout.write(f"Removed directory: {r}")
                    else:
                        dirIn=[d for d in os.listdir(r) if os.path.isdir(os.path.join(r, d))]
                        for dIn in dirIn:
                            if dIn in TO_REMOVE:
                                shutil.rmtree(os.path.join(r, dIn), ignore_errors=True)
                                self.stdout.write(f"Removed directory: {os.path.join(r, dIn)}")


            # os.remove("./db.sqlite3")
            # print(f"Usunięto baze danych: ./db.sqlite3")

            # shutil.rmtree("../db_data", ignore_errors=True)
            # print(f"Usunięto baze danych: ../db_data")

            # shutil.rmtree("../data", ignore_errors=True)
            # print(f"Usunięto file storage: ../data")

            # os.system(f"django-admin sqlflush")

            try:
                # use django-extensions package to reset database
                subprocess.run([FILE_EXECUTE + '  reset_db --noinput --close-sessions'], check=True, cwd='/django', shell=True)

            except subprocess.CalledProcessError as e:
                self.stderr.write(f"Error clearing database: {e}")
            else:
                self.stdout.write("Database is clear.")

        except OperationalError as e:
            self.stderr.write("Error: ", e)

        try:
            # make migrations all apps
            for app in APPLICATION_NAME:
                subprocess.run([f"{FILE_EXECUTE} makemigrations { app }"], check=True, cwd='/django', shell=True)

            subprocess.run([f"{FILE_EXECUTE} makemigrations"], check=True, cwd='/django', shell=True)
            subprocess.run([f"{FILE_EXECUTE} migrate"], check=True, cwd='/django', shell=True)
            subprocess.run([f"{FILE_EXECUTE} createsuperuser --no-input"], check=False, cwd='/django', shell=True)


        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error creating migrations: {e}")