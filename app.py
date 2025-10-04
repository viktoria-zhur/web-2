from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)
@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы",404
    
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
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
    <!doctype html>
    <html>
        <body>
            Сколько раз вы сюда заходили: ''' + str(count) + '''
            <hr>
            Дата и время: ''' + str(time) + '''<br>
            Запрошенный адрес: ''' + url + '''<br>
            Ваш IP адрес: ''' + client_ip + '''<br>
        </body>
    </html>
 '''

@app.route("/info")
def info():
    return redirect("/author")

@app.route("/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201    