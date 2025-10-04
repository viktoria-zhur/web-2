from flask import Flask
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
if __name__ == "__main__":
    app.run(debug=True)