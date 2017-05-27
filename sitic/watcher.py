# -*- condig: utf-8 -*-
import os
import time
from functools import reduce

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from sitic.config import config
from sitic.generator import Generator
from sitic.logging import logger


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

    def __init__(self):
        self.generator = Generator()

    def start(self, generate_on_start = True):

        if generate_on_start:
            self.generator.gen()

        paths_to_watch = [config.content_path, config.static_path, config.templates_path]

        event_handler = EventHandler()
        observer = Observer()
        for path in paths_to_watch:
            if os.path.exists(path):
                logger.info('Watching {}'.format(path))
                observer.schedule(event_handler, path, recursive=True)
        observer.start()

        stop = False
        while not stop:
            try:
                time.sleep(1)
                if event_handler.modified:
                    event_handler.modified = False
                    self.generator.gen()
            except KeyboardInterrupt:
                stop = True
                logger.info('Stopping watcher...')

        observer.stop()
        observer.join()
