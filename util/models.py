from typing import List
from pydantic import BaseModel

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


class Post:
    ''' A post in a thread.
    '''
    content: str
    date: str
    order: int

    def __init__(self, content: str, date: str, order: int) -> None:
        ''' Create a new Post object.

        Args:
            content (str): Post contents.
            date (str): Post date.
            order (int): Post order.
        '''
        self.content = content
        self.date = date
        self.order = order


class Thread:
    ''' A thread.
    '''
    summary: ThreadSummary
    posts: List[Post]

    def __init__(self, summary: ThreadSummary) -> None:
        ''' Create a new Thread object.

        Args:
            summary (ThreadSummary): Thread summary.
        '''
        self.summary = summary
        self.posts = []
    
    def add_post(self, post: Post) -> None:
        ''' Add a post to the thread.
        '''
        self.posts.append(post)

    def as_dict(self) -> dict:
        ''' Return the thread as a dictionary.
        '''
        dictionary: dict = {}

        dictionary['subject'] = self.summary.subject
        dictionary['date'] = self.summary.date
        dictionary['thread_id'] = self.summary.thread_id
        dictionary['posts'] = {}
        for post in self.posts:
            dictionary['posts'][post.order] = {
                'date': post.date,
                'content': post.content
            }

        return dictionary
    
class NewThreadRequest(BaseModel):
    ''' Request to create a new thread.
    '''
    subject: str
    content: str