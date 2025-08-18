from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    # Placeholder: integrate with retriever/generator
    return jsonify({'answer': 'This is a placeholder answer.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
