from typing import Self
import sqlite3
from util.util import Config, Date
from util.models import ThreadSummary, BoardSummary, Thread, Post

DEFAULT_DATABASE = 'liteboard.db'

class DB:
    ''' Singleton database interface.
    '''
    _instance: Self = None
    connection: sqlite3.Connection

    def __new__(cls) -> Self:
        ''' Create a new DB.
        '''
        if cls._instance is None:
            # create new DB connection if it doesn't exist
            cls._instance = super().__new__(cls)
            db_name: str = Config().get('db', DEFAULT_DATABASE)
            cls._instance.connection = sqlite3.connect(db_name)

            # create table if it doesn't exist
            cursor = cls._instance.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts(
                    board TEXT,
                    thread INTEGER,
                    postorder INTEGER,
                    date TEXT,
                    subject TEXT,
                    contents TEXT,
                    PRIMARY KEY(board, thread, postorder)
                )
            ''')
            cursor.close()

        return cls._instance

    def get_board(self, board_id: str) -> BoardSummary:
        ''' Get the contents of a board.

        Args:
            board_id (str): Board ID.
        
        Returns:
            BoardSummary: Board contents.
        '''
        # get data from DB
        cursor = self.connection.cursor()
        result = cursor.execute(f'''
            SELECT thread, date, subject 
            FROM posts 
            WHERE board = "{board_id}"
            AND postorder = 0
        ''')
        threads = result.fetchall()
        cursor.close()

        # parse into board summary
        board = BoardSummary()
        for thread in threads:
            thread_id = thread[0]
            date = thread[1]
            subject = thread[2]
            reply_count = self._count_replies(board_id, thread_id)
            board.add_thread(ThreadSummary(thread_id, date, subject, reply_count))

        return board
    
    def get_thread(self, board_id: str, thread_id: int) -> Thread:
        ''' Get a thread.

        Args:
            board_id (str): Board ID.
            thread_id (str): Thread ID.
        
        Returns:
            Thread: Thread.
        '''
        
        # get summary info from OP
        cursor = self.connection.cursor()
        result = cursor.execute(f'''
            SELECT date, subject
            FROM posts
            WHERE board = "{board_id}"
            AND thread = {thread_id}
            AND postorder = 0
                                            
        ''')
        thread_date, thread_subject = result.fetchone()
        reply_count = self._count_replies(board_id, thread_id)
        thread_summary = ThreadSummary(thread_id, thread_date, thread_subject, reply_count)
        this_thread = Thread(thread_summary)

        # get posts
        result = cursor.execute(f'''
            SELECT date, postorder, contents
            FROM posts
            WHERE board = "{board_id}"
            AND thread = {thread_id}    
        ''')
        post_rows = result.fetchall()

        # add posts to thread
        for row in post_rows:
            post_date, post_order, post_content = row
            this_post = Post(post_content, post_date, post_order)
            this_thread.add_post(this_post)

        cursor.close()
        return this_thread


    def new_thread(self, board_id: str, subject: str, content: str) -> int:
        ''' Create a new thread.

        Args:
            board_id (str): Board ID.
            subject (str): Subject line.
            content (str): Content

        Returns:
            int: Thread ID.
        '''
        
        cursor = self.connection.cursor()

        # get highest thread 
        result = cursor.execute(f'''
            SELECT MAX(thread)
            FROM posts
            WHERE board = "{board_id}"
            AND postorder = 0                 
        ''')
        last_thread = result.fetchone()[0]

        if last_thread is None:
            last_thread = 0

        thread_id = last_thread + 1

        result = cursor.execute(f'''
            INSERT INTO posts (
                board, thread, postorder, date, subject, contents
            )
            VALUES (
                "{board_id}",
                {thread_id},
                0,
                "{Date.timestamp()}",
                "{subject}",      
                "{content}"
            )
        ''')
        success = result.fetchall()

        cursor.close()
        self.connection.commit()

        print(success)
        return thread_id

    def reply_thread(self, board_id: str, thread_id: int, contents: str) -> bool:
        ''' Reply to a thread.

        Args:
            board_id (str): Board ID.
            thread_id (int): Thread ID.
            contents (str): Reply contents.

        Returns:
            bool: True if successful.
        '''
        
        cursor = self.connection.cursor()

        # get reply order
        result = cursor.execute(f'''
            SELECT MAX(postorder)
            FROM posts
            WHERE board = "{board_id}"
            AND thread = {thread_id}
        ''')
        post_order = result.fetchone()[0] + 1      
        
        cursor.execute(f'''
            INSERT INTO posts (
                board, thread, postorder, date, subject, contents
            )
            VALUES (   
                "{board_id}",
                {thread_id},
                {post_order},
                "{Date.timestamp()}",
                "",
                "{contents}"
            )      
        ''')

        self.connection.commit()
        cursor.close()

        return True

    def _count_replies(self, board_id: str, thread_id: int) -> int:
        ''' Get the number of replies in a thread.
        '''
        cursor = self.connection.cursor()
        response = cursor.execute(f'''
            SELECT COUNT(*)
            FROM posts
            WHERE board = "{board_id}"
            AND thread = {thread_id}
        ''')
        return response.fetchone()[0]