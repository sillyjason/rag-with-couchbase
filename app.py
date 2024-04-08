from flask import Flask, render_template
from app1 import run_function_blueprint
from app2 import blueprint2
from app3 import blueprint3
from app4 import blueprint4
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, static_folder='static')
app.register_blueprint(run_function_blueprint)
app.register_blueprint(blueprint2)
app.register_blueprint(blueprint3)
app.register_blueprint(blueprint4)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app1')
def app1():
    return render_template('app1.html')

@app.route('/app2')
def app2():
    return render_template('app2.html')

@app.route('/app3')
def app3():
    return render_template('app3.html')

@app.route('/app4')
def app4():
    return render_template('app4.html')

if __name__ == '__main__':
    app.run(port=8080)
