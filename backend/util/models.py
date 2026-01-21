from typing import List, Dict
from pydantic import BaseModel

class ThreadSummary:
    ''' Summary of a thread.
    '''
    thread_id: int
    date: str
    subject: str
    replies: int
    attachment: str

    def __init__(self, thread_id: int, date: str, subject: str, replies: int, attachment: str) -> None:
        ''' Create a new ThreadSummary.

        Args:
            thread_id (int): Thread ID.
            date (str): UNIX timestamp.
            subject (str): Subject line.
        '''
        self.thread_id = thread_id
        self.date = date
        self.subject = subject
        self.replies = replies
        self.attachment = attachment


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
        dictionary: Dict[int, Dict[str, str]] = {}

        for thread in self.threads:
            dictionary[thread.thread_id] = {
                'subject': thread.subject,
                'date': thread.date,
                'replies': thread.replies,
                'attachment': thread.attachment
            }

        return dictionary


class Post:
    ''' A post in a thread.
    '''
    content: str
    date: str
    order: int
    attachment: str

    def __init__(self, content: str, date: str, order: int, attachment: str) -> None:
        ''' Create a new Post object.

        Args:
            content (str): Post contents.
            date (str): Post date.
            order (int): Post order.
        '''
        self.content = content
        self.date = date
        self.order = order
        self.attachment = attachment


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
        dictionary['replies'] = self.summary.replies
        dictionary['posts'] = {}
        for post in self.posts:
            dictionary['posts'][post.order] = {
                'date': post.date,
                'content': post.content,
                'attachment': post.attachment
            }

        return dictionary
    

class NewThreadRequest(BaseModel):
    ''' Request to create a new thread.
    '''
    subject: str
    content: str


class ReplyRequest(BaseModel):
    ''' Request to reply to a thread.
    '''
    content: str