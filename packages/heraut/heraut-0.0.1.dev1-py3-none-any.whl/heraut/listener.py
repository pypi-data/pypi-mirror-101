import queue as qu
import os
import pickle
import pathlib

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .coreUtils import SigKill


class Listener(object):
    def __init__(self, path=None, name=''):
        self.active = True
        self.name = name
        self.queue = qu.Queue()
        self.handler = Handler(queue=self.queue)
        self.observer = Observer()
        self.path = path
        if self.path is None:
            self.path = str(pathlib.Path.home()) + '/' + os.environ['HERAUT_DEFAULT']
        self.observer.schedule(event_handler=self.handler, path=self.path)
        self.observer.start()

    def listening(self):
        return self.active

    def get_message(self):
        flag = True
        while flag:
            if not self.queue.empty():
                # Get a message
                filename = self.queue.get(True)
                with open(filename, 'rb') as f:
                    message = pickle.load(f)
                    label = pickle.load(f)
                    metadata = pickle.load(f)

                if type(message) is not SigKill:
                    return True, message, label, metadata
                else:
                    print('caught a sigkill for', message.target)
                    self.active = False
                    self.end()
                    return False, None, None, None

    def end(self):
        # Clean up the observer thread
        self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, queue):
        super().__init__()
        assert type(queue) is qu.Queue
        self.queue = queue

    def on_closed(self, event):
        print('closed', event.src_path)
        self.queue.put(event.src_path)
