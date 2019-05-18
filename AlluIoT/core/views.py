from flask import render_template, request,Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html')

@core.route('/info')
def info():
    return render_template('info.html')

@core.route('/instView_dash')
def instView_dash():
    return render_template('instView_dash.html')

@core.route('/compareView_dash')
def compareView_dash():
    return render_template('compareView_dash.html')

@core.route('/pumpView_dash')
def pumpView_dash():
    return render_template('pumpView_dash.html')

@core.route('/tableView_dash')
def tableView_dash():
    return render_template('tableView_dash.html')