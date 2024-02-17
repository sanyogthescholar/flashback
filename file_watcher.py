import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import image_caption
import time

class MyEvent(LoggingEventHandler):
    def dispatch(self, event):
        #TODO Debug events running more than once
        #print(event)
        if not event.is_directory:
            if event.event_type == 'created':
                new_file = event._src_path
                print(new_file)
                print(f"{event.event_type = }")
                start = time.time()
                result = image_caption.caption_image(new_file)
                end = time.time() - start
                print(f"{result = }\n{end = }")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else './uploaded_files'
    event_handler = MyEvent()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("File Watcher Started")
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()