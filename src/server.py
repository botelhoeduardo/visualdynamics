from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    if request.method == 'POST':
        pass
    return render_template('index.html')

if __name__ == '__main__':
    app.run()