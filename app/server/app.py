from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # This could be any data that the user can't directly access
    # For this example, we'll just use a simple string
    data = "Hello, this is your secret data!"
    return jsonify(data=data)

if __name__ == "__main__":
    app.run(debug=True)
