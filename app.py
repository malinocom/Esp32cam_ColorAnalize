from flask import Flask, render_template
app = Flask(name)

@app.route('/show') def show_page(): return render_template('page.html') # نام فایل HTML شما

if name == 'main': app.run(debug=True)

Run
