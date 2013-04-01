import threading
import Queue


class ThreadPool:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.queue = Queue.Queue()

    def add_image(self, image):
        self.queue.put(image)

    def download(self, directory):
        semaphore_io = threading.Semaphore()

        for i in range(self.num_threads):
            t = DownloadThread('thread' + str(i), self.queue, semaphore_io, directory)
            t.daemon = True
            t.start()

        self.queue.join()


class DownloadThread(threading.Thread):
    def __init__(self, name, queue, semaphore_io, directory):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.semaphore_io = semaphore_io
        self.directory = directory

    def safe_print(self, s):
        self.semaphore_io.acquire()
        print s
        self.semaphore_io.release()

    def run(self):
        while True:
            try:
                image = self.queue.get()

                if image.download_to(self.directory):
                    speed_kbs = int((image.download_size / image.download_time) / 1024)
                    self.safe_print("Download complete  {}  {:,}KB/s".format(image.page, speed_kbs))
                else:
                    self.safe_print("Download skipped  {}".format(image.page))
            except Exception, e:
                # TODO: This cannot be right, but how do I make sure queue.task_done is called?
                print self.safe_print("Exception " + str(e))
            finally:
                self.queue.task_done()
