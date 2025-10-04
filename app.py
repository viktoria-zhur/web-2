from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def start():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-cepsep на flask</h1>
            </body>
        </html>"""

@app.route("/author")
def author():
    name = "Журавлева Виктория Александровна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
            </body>
        </html>"""

@app.route('/image')
def image():
    path = url_for("static", filename="a.png")
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>Supra</h1>
            <img src="''' + path + '''">
        </body>
    </html>            
'''
count = 0

@app.route('/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
 </html>
 '''       