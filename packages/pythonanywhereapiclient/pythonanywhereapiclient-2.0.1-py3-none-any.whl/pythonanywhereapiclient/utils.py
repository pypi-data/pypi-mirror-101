import os
from dataclasses import dataclass


def construct_request_payload(dictionary, exclude=[]):
    for key, value in dictionary.copy().items():
        if key in exclude or value is None:
            del dictionary[key]

    return dictionary


def getenv(key, default=None):
    return os.getenv(f'PYTHONANYWHERE_API_CLIENT_{key}', default)


@dataclass(frozen=True)
class Python:
    version: str

    @property
    def executable(self):
        return f'python{self.version}'

    @property
    def longcode(self):
        return f'python{self.version_stripped}'

    @property
    def shortcode(self):
        return f'py{self.version_stripped}'

    @property
    def version_stripped(self):
        return self.version.replace('.', '')
