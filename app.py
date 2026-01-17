''' API for a simple text board.
'''

from flask import Flask, request, jsonify, Response
from flask_pydantic import validate
from util.db import DB
from util.config import Config

app: Flask = Flask(__name__)

@app.get('/<board_id>')
def get_board(board_id: str) -> Response:
    ''' Given a board ID, return a list of threads.

    Args:
        board_id (str): Board ID.

    Returns:
        Response: JSON response with board contents.
    '''
    # make sure board exists
    if board_id not in Config().get('boards', []):
        return jsonify({
            'error': f'No such board {board_id}'
        }), 404
    
    return jsonify(DB().get_board(board_id).as_dict()), 200

@app.get('/<board_id>/<thread_id>')
def get_thread(board_id: str, thread_id: str) -> Response:
    ''' Given a board ID and a thread ID, return a thread.

    Args:
        board_id (str): Board ID.
        thread_id (str): Thread ID.
    
    Returns:
        Response: JSON response with thread contents.
    '''
    pass

@app.post('/<board_id>')
def new_thread(board_id: str) -> Response:
    ''' Given a board ID, make a new thread on that board.

    Args:
        board_id (str): Board ID.

    Returns:
        Response: JSON response with thread ID.
    '''
    pass

@app.post('/<board>/<thread_id>')
def reply_thread(board_id: str, thread_id: str) -> Response:
    ''' Given a board ID and a thread ID, reply to the thread.

    Args:
        board_id (str): Board ID.
        thread_id (str): Thread ID.

    Returns:
        Response: JSON response with post number.
    '''
    pass

# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)