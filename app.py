from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        status = request.form.get('status')
        return f"Received: {name} - {status}"
    
    return render_template('form.html')

@app.route('/<room_code>', methods=['GET', 'POST'])
def learner(room_code):
    if request.method == 'POST':
        name = request.form.get('name')
        status = request.form.get('status')
        return f"Room {room_code}: {name} - {status}"
    
    return render_template('learner.html', room_code=room_code)

@app.route('/<room_code>/tutor', methods=['GET', 'POST'])
def tutor(room_code):
    if request.method == 'POST':
        name = request.form.get('name')
        status = request.form.get('status')
        return f"Room {room_code}: {name} - {status}"
    
    return render_template('tutor.html', room_code=room_code)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
