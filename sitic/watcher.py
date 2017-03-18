# -*- condig: utf-8 -*-
import os
import time
from functools import reduce

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from sitic.config import config
from sitic.generator import Generator


class EventHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super(FileSystemEventHandler, self).__init__(*args, **kwargs)
        self.modified = False

    def _handle_event(self, event):
        filename = os.path.basename(event.src_path)
        if not event.is_directory:
            any_match = reduce(lambda x,y: x or y,
                    [re.match(filename) for re in config.ignore_files_regex])
            if not any_match:
                self.modified = True

    def on_modified(self, event):
        self._handle_event(event);

    def on_created(self, event):
        self._handle_event(event);


class Watcher:

    def start(self):
        generator = Generator()
        event_handler = EventHandler()
        observer = Observer()
        observer.schedule(event_handler, config.content_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
                if event_handler.modified:
                    event_handler.modified = False
                    generator.gen()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
