import threading
import Queue
import time
import os

from downloadhttps import download_url


class DownloadPool:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.queue = Queue.Queue()
        self.bytes_downloaded = 0
        self.start_time = time.time()

    def add_file(self, url, path, filename=None):
        self.queue.put((url, path, filename))

    def start(self):
        semaphore_io = threading.Semaphore()

        for i in range(self.num_threads):
            t = DownloadThread(self, 'thread' + str(i), self.queue, semaphore_io)
            t.daemon = True
            t.start()

    def join(self):
        self.queue.join()

    def add_bytes_downloaded(self, amount):
        self.bytes_downloaded += amount

    def get_bytes_downloaded(self):
        return self.bytes_downloaded

    def get_start_time(self):
        return self.start_time


class DownloadThread(threading.Thread):
    def __init__(self, pool, name, queue, semaphore_io):
        threading.Thread.__init__(self)
        self.pool = pool
        self.name = name
        self.queue = queue
        self.semaphore_io = semaphore_io

    def safe_print(self, s):
        self.semaphore_io.acquire()
        print s
        self.semaphore_io.release()

    def run(self):
        while True:
            try:
                (url, directory, filename) = self.queue.get()

                if filename is None:
                    filename = url[url.rfind('/')+1:]

                if os.path.exists(directory + '/' + filename):
                    self.safe_print("Download skipped  {}".format(filename))
                    continue

                start_time = time.time()
                data = download_url(url, directory + '/' + filename)
                end_time = time.time()

                self.pool.add_bytes_downloaded(len(data))

                # This speed is alright.  But total speed isn't going to be a bit rough.  Better than nothing though
                this_speed_kbs = int((len(data) / (end_time-start_time)) / 1024)
                total_speed_kbs = int((self.pool.get_bytes_downloaded() / (end_time-self.pool.get_start_time())) / 1024)

                self.safe_print("Download complete  {}  {:,}KB/s  ({:,}KB/s)  ~{:,} images left".format(
                    filename, this_speed_kbs, total_speed_kbs, self.queue.qsize()))

            except Exception, e:
                # TODO: This cannot be right, but how do I make sure queue.task_done is called?
                print self.safe_print("Exception " + str(e))
            finally:
                self.queue.task_done()