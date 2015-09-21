import logging
import multiprocessing
import sys

class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filename="threading.log",
    filemode='a'
)

class JobProcess(multiprocessing.Process):
    def __init__(self, name, job):
        super(JobProcess, self).__init__()
        self.name = name
        self.job = job

    def run(self):
        thread_logger = logging.getLogger(self.name)
        sys.stdout = StreamToLogger(thread_logger, logging.INFO)
        sys.stderr = StreamToLogger(thread_logger, logging.ERROR)
        thread_logger.info("Starting " + self.name + "...")
        self.job.main()

print("Awesome test program!")
testing_module = __import__("test_thread")
test_job = JobProcess("Thread 1", testing_module)
test_job.start()
print("DONE!!")
