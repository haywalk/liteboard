''' API for a simple text board.
'''

from flask import Flask, request, jsonify, Response
from flask_pydantic import ValidationError
from util.db import DB
from util.util import Config
from util.models import NewThreadRequest

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
    # make sure board exists
    if board_id not in Config().get('boards', []):
        return jsonify({
            'error': f'No such board {board_id}.'
        }), 404
    
    # make sure thread exists
    if thread_id not in [i.thread_id for i in DB().get_board(board_id).threads]:
        return jsonify({
            'error': f'No such thread {thread_id} on {board_id}.'
        }), 404

    return jsonify(DB().get_thread(board_id, thread_id).as_dict())

@app.post('/<board_id>')
def new_thread(board_id: str) -> Response:
    ''' Given a board ID, make a new thread on that board.

    Args:
        board_id (str): Board ID.

    Returns:
        Response: JSON response with thread ID.
    '''
    try:
        payload = NewThreadRequest.model_validate(request.get_json())
        thread_id = DB().new_thread(board_id, payload.subject, payload.content)

        return jsonify({
            'thread_id': thread_id
        }), 200

    except ValidationError as e:
        return jsonify({
            "error": "Malformed payload.",
            "details": e.errors()
        }), 400

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