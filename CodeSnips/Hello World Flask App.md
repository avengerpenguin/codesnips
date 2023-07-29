Create `hello.py`:

```python
from flask import Flask, render_template, request

# Create a Flask app instance
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return 'Hello, World!'

# Route for a simple form
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        return f'Hello, {name}!'
    return render_template('form.html')

# Route with dynamic content
@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
```

Create `templates/form.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Simple Form</title>
</head>
<body>
    <h1>Enter your name:</h1>
    <form method="POST" action="/form">
        <input type="text" name="name" required>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
```

Run:

```bash
flask --app=hello run
```
