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
    def __init__(self, job):
        super(JobProcess, self).__init__()
        self.job = job

    def run(self):
        # sys.stdout = open('file', 'w')
        # sys.stderr = open('file', 'a')
        thread_stdout = logging.getLogger("ThreadSTDOUT")
        thread_stderr = logging.getLogger("ThreadSTDERR")
        sys.stdout = StreamToLogger(thread_stdout, logging.INFO)
        sys.stderr = StreamToLogger(thread_stderr, logging.ERROR)
        self.job.main()

print("Awesome test program!")
testing_module = __import__("test_thread")
test_job = JobProcess(testing_module)
test_job.start()
print("DONE!!")
