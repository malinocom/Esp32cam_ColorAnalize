from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Amiram</h1><a href="/show">Go to Show Page</a>'

@app.route('/show')
def show_page():
    return render_template('page.html')

if __name__ == '__main__':
    app.run(debug=True)
