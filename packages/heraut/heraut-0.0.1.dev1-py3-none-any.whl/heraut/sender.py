import os
import pickle
import pathlib
import hashlib
import datetime
from .coreUtils import SigKill


class Sender(object):
    def __init__(self, path=None, name=''):
        self.name = name
        self.storage_dir = path
        self.hash = hashlib.blake2s
        if self.storage_dir is None:
            self.storage_dir = os.environ['HERAUT_DEFAULT']
        pass

    def send(self, message, label='', target=''):
        metadata = {'name': self.name}
        fname = self.get_filename_hash()
        with open(str(pathlib.Path.home()) + '/' + self.storage_dir + '/' + target + '-' + fname + '.pkl', 'wb') as f:
            pickle.dump(message, f)
            pickle.dump(label, f)
            pickle.dump(metadata, f)

        return True

    def stop_listener(self, target = ''):
        message = SigKill(sender=self.name, target=target)
        label = 'kill-' + target
        self.send(message=message, label=label, target=target)

    def get_filename_hash(self):
        key = bytes(str(os.getpid()) + str(datetime.datetime.now()), 'utf-8')
        return self.hash(key).hexdigest()
