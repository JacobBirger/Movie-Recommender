from flask import Flask
from markupsafe import escape
import pandas as pd
#how to make a virtual environment
MovieRecomender = Flask(__name__)
@MovieRecomender.route('/')
def Movie_Recomender():
    return 
    
if __name__ == '__main__':
    MovieRecomender.run(debug=True,use_reloader=False)
# @MovieRecomender.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return f'User {escape(username)}'

# @MovieRecomender.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'

# @MovieRecomender.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'
    