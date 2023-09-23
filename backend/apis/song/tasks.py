from celery import shared_task
from yt_dlp import YoutubeDL
from PIL import Image

from core.settings import OUTPUT_AUDIO_PATH, OUTPUT_TEMP_PATH, OUTPUT_IMAGE_PATH, MEDIA_URL_THUMBNAIL

from apis.song.DlerMedia.progress_hooks import youtube_progress_hooks
from .models.TaskProgress import DownloadProgress
from .models.Song import Song
import os

@shared_task(bind=True)
def adownload(
                self,
                url: str,
                objectId: str,
                thumbnail_outputDir: str,
                outputSongPathTemplate: str,
                homePath: str = OUTPUT_AUDIO_PATH,
                tempPath: str = OUTPUT_TEMP_PATH
            ) -> bool:

    """
        `url: str`                      - url address from which the audio will be downloaded
        `objectId: str`                 - id of the object which will be updated
        `thumbnail_outputDir: str`      - path to the directory where thumbnails will be saved
        `outputSongPathTemplate: str`   - template for the path where the audio will be saved
        `homePath: str`                 - path to the directory where the audio will be saved
        `tempPath: str`                 - path to the directory where the audio will be saved
    """

    progress    = DownloadProgress.objects.get(id=objectId)

    ydl_opt = {
        'format': 'bestaudio/best',  # Wybór najlepszej jakości audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Jeśli chcesz mp3 zamiast mp4
            'preferredquality': '192',  # Jakość audio
        }],
        'progress_hooks': [lambda x: youtube_progress_hooks(x, objectId)],
        'paths': {
            'home': homePath,
            'temp': tempPath,
        },
        'writethumbnail': True,
        'quiet': True,
        'outtmpl': outputSongPathTemplate
    }

    resolutions = [(256, 144), (640, 360), (854, 480), (1280, 720)]

    with YoutubeDL(ydl_opt) as ydl:
        progress.status = progress.CODE_DOWNLOADING

        dl = ydl.download(url)

        if dl:
            progress.status = progress.CODE_ERROR
            progress.save()

        else:
            original_image_file = f'{homePath}{objectId}.webp'

            song = Song.objects.get(id=objectId)
            image = Image.open(original_image_file)

            if not os.path.exists(thumbnail_outputDir):
                os.makedirs(thumbnail_outputDir)

            for res in resolutions:
                resized_image = image.resize(res)
                resized_image.save(f'{thumbnail_outputDir}thumbnail_{res[1]}p.webp')

            image.save(f'{thumbnail_outputDir}thumbnail_original.webp')

            song.thumbnail_file = f'{MEDIA_URL_THUMBNAIL}thumbnail_original.webp'
            song.save()

            progress.status = progress.CODE_FINISHED
            progress.estimated_wait_time = None
            progress.save()

            os.remove(original_image_file)


    return True
