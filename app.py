import os
import re
import json

from datetime import datetime

from flask import Flask
from flask import request
from flask import render_template, abort, url_for

app = Flask(__name__)
app.debug = True  # Or set this via config or environment

# Constants
DB_FILE = 'logs/db.jsonXX'

# Initilise DB
db = {}
if app.debug and os.path.exists(DB_FILE):
    with open(DB_FILE, 'r') as f:
        db = json.load(f)


def save_db(filename=DB_FILE):
    with open(filename, 'w') as f:
        json.dump(db, f, default=str, indent=4)


def validate_room_code(room_code):
    """Ensures the room code is alphanumeric and converts it to uppercase."""
    if not re.match(r'^[A-Za-z0-9]+$', room_code):  
        abort(404, description="Room can only consist of letters and numbers: "+room_code)

    if len(room_code) < 2 or len(room_code) > 10:  
        abort(404, description="Room length must be < 10 ~ "+str(len(room_code)))

    return room_code.upper()  # Return the uppercase version


def get_room(room_code):
    created_date = datetime.now()
    if room_code not in db:
        db[room_code] = {
            'description': room_code,
            'learners': {},
            'created_date': created_date
        }
    return db[room_code]


def save_learner(room_code, learner_id, first_name, status, answer):
    room = get_room(room_code)
    room['learners'][learner_id] = {
        'first_name': first_name,
        'status': status,
        'answer': answer,
        'last_updated': datetime.now()
    }


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        status = request.form.get('status')
        return f"Received: {name} - {status}"
    
    return render_template('home.html')

@app.route('/<room_code>', methods=['GET', 'POST'])
def learner_view(room_code):
    template_name = 'learner.html'
    
    # Make sure that the room code is valid
    room_code = validate_room_code(room_code)
    if request.method == 'POST':
        learner_id = request.form.get('learner_id')
        first_name = request.form.get('first_name')
        status = request.form.get('status')
        answer = request.form.get('answer')

        # if clear pressed keep name only
        if status == 'clear':
            answer = ''

        # for testing change learner_id so that can have multiple users in one browser
        if app.debug:
            learner_id = first_name+":"+learner_id

        # Save the record
        save_learner(room_code, learner_id, first_name, status, answer)

        # save the db to a file
        if app.debug: save_db()

        # Show the page
        context = {
            'room_code' : room_code,
            'first_name' : first_name,
            'status' : status,
            'answer' : answer,
        }
        return render_template(template_name, **context)
    
    return render_template(template_name, room_code=room_code)


@app.route('/<room_code>/tutor', methods=['GET', 'POST'])
def tutor_view(room_code):
    template_name = 'tutor.html'
    
    # Make sure that the room code is valid
    room_code = validate_room_code(room_code)

    # Get url for learners
    url = request.host_url.rstrip('/')+url_for('home')+room_code.lower()
    
    # Get learner records from the database for this room
    learners = db.get(room_code, {'learners':{}})['learners']

    # Show the page
    context = {
        'room_code': room_code,
        'learners': learners,
        'url': url,
    }
    return render_template(template_name, **context)


@app.route('/<room_code>/poll', methods=['GET'])
def poll_view(room_code):
    template_name = 'poll.html'
    room_code = validate_room_code(room_code)

    # Get learner records from the database for this room
    learners = db.get(room_code, {'learners':{}})['learners']

    # Get learner records from the database for this room
    learner_count = len(learners)

    # Group by status
    status_counts = {}
    
    for _,learner in learners.items():
        if learner['status'] == 'clear': continue  # ignore status of clear
        if learner['status'] not in status_counts:
            status_counts[learner['status']] = []
        status_counts[learner['status']].append(learner['first_name'])

    # Get the maximum count of learners in any status
    max_count = max((len(learners) for learners in status_counts.values()), default=0)

    # Show the page
    context = {
        'room_code': room_code,
        'learner_count': learner_count,
        'status_counts': status_counts,
        'max_count': max_count,
    }
    return render_template(template_name, **context)


# Static Views
@app.route('/about', methods=['GET'])
def about_page():
    template_name = 'about.html'
    context = {
    }
    return render_template(template_name, **context)

@app.route('/browser-check', methods=['GET'])
def browser_check():
    template_name = 'browser-check.html'
    context = {
        'message': 'Browser Check!'
    }
    return render_template(template_name, **context)





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
