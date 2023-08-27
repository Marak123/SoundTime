import re

class ValidURL:
    def __init__(self, url: str) -> None:
        self.url = url

        self.valid_url_reg = r'(((http|https):\/\/)|(\/)|(..\/))(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?'
        self.valid_url_dict = {
            'youtube': (
                r'(https?://)?(www\.|music\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
            ),

            'soundcloud': r'(http|https):\/\/(?:www\.)?soundcloud.com\/((?:[^\W_]|-)){3,255}\/(sets|((?:[^\W_]|-){3,255}))(\/((?:[^\W_]|-){3,255})|(\?in=((?:[^\W_]|-){3,255})\/((?:[^\W_]|-){3,255})\/((?:[^\W_]{3,255}|-))|))',
            'vimeo': r'https:\/\/(?:www.)?vimeo.com\/([0-9]{9})(?:\#t=(\d+)s)?',
            'spotify': r'^(?:spotify:|https:\/\/[a-z]+\.spotify\.com\/(track\/|user\/(.*)\/playlist\/))(.*)$',
        }

    def __validator_url(self) -> str:
        if not re.match(self.valid_url_reg, self.url):
            return None

        for service, validator in self.valid_url_dict.items():
            if re.match(validator, self.url):
                return service

        return None

    @property
    def is_valid(self) -> bool:
        return self.__validator_url() is not None

    @property
    def platform(self) -> str:
        return self.__validator_url()