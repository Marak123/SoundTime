from core.settings import OUTPUT_AUDIO_PATH, OUTPUT_IMAGE_PATH, MEDIA_URL_AUDIO, MEDIA_URL_THUMBNAIL

from apis.song.models.TaskProgress import DownloadProgress
from apis.song.models.Song import Song

import json

def youtube_progress_hooks(info, idObject: str):
    float_or_default = lambda x, y: float(x) if x is not None else y
    devide_or_default = lambda x, y, z: float(x) / float(y) if x is not None and y is not None else z

    progress    = DownloadProgress.objects.get(id=idObject)

    if info['status'] == "downloading":

        progress.estimated_wait_time = float_or_default(info.get('eta', None), progress.estimated_wait_time)
        progress.download_time       = float_or_default(info.get('elapsed', None), progress.download_time)
        progress.download_progress   = devide_or_default(info.get('downloaded_bytes', None), info.get('total_bytes_estimate', None), progress.download_progress)

    elif info['status'] == "finished":
        song = Song.objects.get(id=idObject)

        progress.status = progress.CODE_FINISHED

        progress.estimated_wait_time = float_or_default(info.get('eta', None), progress.estimated_wait_time)
        progress.download_time       = float_or_default(info.get('elapsed', None), progress.download_time)

        song.audio_file = f'{MEDIA_URL_AUDIO}{idObject}.mp3'

        song.save()

        # print(json.dumps(info))

    elif info['status'] == "error":
        progress.status = progress.CODE_ERROR


    progress.save()