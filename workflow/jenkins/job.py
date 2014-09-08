import os


class Job(object):
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['name']

    @property
    def url(self):
        return self._data['url']

    @property
    def status(self):
        return self._data['color']

    @property
    def image(self):
        return "{}/images/{}.png".format(os.getcwdu(), self.status)

    @property
    def description(self):
        return self._data.get('description', "")
