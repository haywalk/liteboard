from typing import List

class ThreadSummary:
    ''' Summary of a thread.
    '''
    thread_id: str
    date: str
    subject: str

    def __init__(self, thread_id: str, date: str, subject: str) -> None:
        ''' Create a new ThreadSummary.

        Args:
            thread_id (str): Thread ID.
            date (str): UNIX timestamp.
            subject (str): Subject line.
        '''
        self.thread_id = thread_id
        self.date = date
        self.subject = subject

class BoardSummary:
    ''' List of threads in a board..
    '''
    threads: List[ThreadSummary]

    def __init__(self) -> None:
        ''' Create a new BoardSummary.
        '''
        self.threads = []

    def add_thread(self, thread: ThreadSummary) -> None:
        ''' Add a thread to the BoardSummary.

        Args:
            thread (ThreadSummary): Thread summary.
        '''
        self.threads.append(thread)
    
    def as_dict(self):
        ''' Return the board summary as a dictionary.
        '''
        dictionary: dict = {}

        for thread in self.threads:
            dictionary[thread.thread_id] = {
                'subject': thread.subject,
                'date': thread.date
            }

        return dictionary
