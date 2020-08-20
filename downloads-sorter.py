import os
import time

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""
    Listens for changes in the downloads folder.
    Files will be sorted into their respective folders.

"""

documents = {'.pdf', '.docx', '.doc', '.txt'}
media = {'.jpeg', '.jpg', '.svg', '.png', '.PNG', '.mp4', '.mp3'}
setup_files = {'.exe', '.msi'}
compressed_files = {'.zip'}
files = {'.apk'}


class MyHandler(FileSystemEventHandler):

    def on_modified(self, event):
        """
            event (Event)

            Listens for modifications to the directory.
            Sorts files types by folders.
        """

        # Move the file to the correct sub folder..

        # Iterate through all files.

        for file_name in os.listdir(str(FOLDER_TO_TRACK)):

            ext = os.path.splitext(file_name)[1]

            # if os.path.isfile(FOLDER_TO_TRACK/file_name) and not file_name.endswith("ini") and not file_name.endswith("part") and not file_name.endswith("crdownload") and not file_name.startswith(".") and not os.stat(FOLDER_TO_TRACK/file_name).st_size == 0:
            if (ext in documents or ext in media or ext in setup_files or ext in compressed_files or ext in files):
                # Check each file by type

                # Place file in correct folder
                # If folder type doesn't exist, make a new folder for that file type.
                if not os.path.exists(FOLDER_TO_TRACK / ext[1:]):
                    os.mkdir(FOLDER_TO_TRACK / ext[1:])

                # Check if the file's name exist in the folder
                # If the file's name exist change the name.
                source_path = FOLDER_TO_TRACK / file_name
                destination_path = get_nonexistant_path(
                    FOLDER_TO_TRACK / ext[1:] / file_name)

                # Move the file to the correct sub folder..
                os.rename(source_path, destination_path)

        # Delete empty files.
        for dirpath, dirnames, file_names in os.walk(FOLDER_TO_TRACK, topdown=False):
            path = Path(dirpath)
            for file_name in file_names:

                if os.stat(path / file_name).st_size == 0:
                    os.remove(path / file_name)


def get_nonexistant_path(path):
    """
        path (Path)
        returns nonexistanting path.
    """
    if not os.path.exists(path):
        return path
    root, ext = os.path.splitext(path)

    i = 1
    new_path = "{}-{}{}".format(root, i, ext)
    while os.path.exists(new_path):
        i += 1
        new_path = "{}-{}{}".format(root, i, ext)

    return new_path


FOLDER_TO_TRACK = Path.home() / "Downloads"

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, FOLDER_TO_TRACK, recursive=True)
observer.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
