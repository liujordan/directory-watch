import sys
import time
import logging
import os
from os import walk
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileModifiedEvent
from pathlib import Path

class MyEventHandler(LoggingEventHandler):
  def on_any_event(self, event):
    p = Path(event.src_path)
    print(list(p.parents))
    for path in list(p.parents)[1:]:
      print(path)
      for (dirpath, subdirList, filenames) in walk(path):
        print(dirpath, subdirList, filenames)
        if "docker-compose.yml" in filenames:
          print("RUNNING COMPOSE")
          os.system(f"docker-compose -f {str(dirpath) + '/docker-compose.yml'} up -d")
          break
      else:
        continue
      break
    return super(MyEventHandler, self).on_any_event(event) 

if __name__ == "__main__":
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

  path = sys.argv[1] if len(sys.argv) > 1 else '.'
  event_handler = MyEventHandler()

  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()