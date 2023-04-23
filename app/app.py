from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_data = request.json['input']
    print(f"Received input: {input_data}")

    # Process the input as needed

    return jsonify({'message': 'success'})

if __name__ == '__main__':
    app.run(debug=True)