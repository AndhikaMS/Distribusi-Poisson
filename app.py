from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Poisson formula function
def poisson_probability(lmbda, x):
    return (math.exp(-lmbda) * (lmbda ** x)) / math.factorial(x)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get the input values from the frontend
        lmbda = float(request.form['lambda'])
        x = int(request.form['x'])

        # Calculate the Poisson probability
        probability = poisson_probability(lmbda, x)

        # Return the result as JSON
        return jsonify({'probability': round(probability, 6)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
