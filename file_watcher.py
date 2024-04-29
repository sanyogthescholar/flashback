import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import image_caption
import time

class MyEvent(LoggingEventHandler):
    new_file_path = "" #temp variable to store the path of the new file
    def dispatch(self, event):
        if not event.is_directory:
            print(f"{event = }")
            if event.event_type == 'created': #if the event is a file creation event
                new_file = event._src_path
                if new_file == self.new_file_path: #if the file is the same as the last file
                    print("!!File already processed!!")
                    return
                self.new_file_path = new_file #set the new file as the last file
                #print(new_file)
                #print(f"{event.event_type = }")
                #start = time.time()
                result = image_caption.caption_image(new_file) #caption the image and store in ChromaDB
                #end = time.time() - start
                #print(f"{result = }\n{end = }")

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