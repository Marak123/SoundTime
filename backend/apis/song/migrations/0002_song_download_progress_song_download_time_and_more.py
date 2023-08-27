# Generated by Django 4.2.4 on 2023-08-24 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis_song', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='download_progress',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='download_time',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='error_details',
            field=models.CharField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='estimated_wait_time',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='queue_position',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apis_song.album'),
        ),
        migrations.AlterField(
            model_name='song',
            name='extractor',
            field=models.IntegerField(blank=True, choices=[(0, 'file', 'File'), (1, 'youtube', 'YouTube'), (2, 'soundcloud', 'SoundCloud'), (3, 'spotify', 'Spotify'), (4, 'vimeo', 'Vimeo')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'queued', 'Queued'), (1, 'downloading', 'Downloading'), (2, 'finished', 'Finished'), (3, 'error', 'Error')], default=0, null=True),
        ),
    ]
