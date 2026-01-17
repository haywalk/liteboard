from typing import Self
import sqlite3
from util.config import Config
from util.models import ThreadSummary, BoardSummary

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
                    board,
                    thread,
                    postorder,
                    date,
                    subject,
                    contents,
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
            AND postorder = "0"
        ''')
        threads = result.fetchall()
        cursor.close()

        # parse into board summary
        board = BoardSummary()
        for thread in threads:
            thread_id = thread[0]
            date = thread[1]
            subject = thread[2]
            board.add_thread(ThreadSummary(thread_id, date, subject))

        return board
        