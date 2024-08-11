from flask import Flask, render_template, request, flash, redirect, url_for
from forms import LoginForm
from config import Config

from requests.auth import HTTPBasicAuth

from get_data import get_metra_data

from datetime import datetime  #this is correct

from markupsafe import escape, Markup
from flask import Blueprint

from get_data.get_metra_data import get_position_json, get_stops_times, get_json_single_trip, get_stops_detail

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config.from_object(Config)
#app = Blueprint('home', __name__)

"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
"""

@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html', message='Hello, Flask with Blueprints!')


@app.route('/user/<name>')
def user(name):
    return render_template('home.html', message='Hello, %s!' % name)


@app.route('/about')
def about():
    user_agent = request.headers.get('User-Agent')
    about_url = url_for('about')
    return render_template('home.html',  about_url=about_url, message="Welcome to my Flask site's 'about' page.  &copy;2024")


@app.route('/privateList/<start_number>')
def show_list2(start_number):
    start_number = int(start_number)
    endNumber = start_number + 101
    myList = range(start_number, endNumber)
    return render_template('list.html',
                           the_title="Bigger List Sample",
                           myList=myList,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )



@app.route('/fruit/list')
def show_list():
    theList = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'strawberry',
               'raspberry', 'cherry']
    return render_template('list.html',
                           the_title='List Sample',
                           myList=theList,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )


@app.route('/fruit/set')
def show_set():
    theSet = {'orange', 'apple', 'pear', 'banana', 'kiwi', 'strawberry',
              'raspberry', 'cherry'}
    return render_template('list.html',
                           the_title='Set Sample',
                           myList=theSet,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )


@app.route('/fruit/set/ordered')
def show_set_ordered():
    theSet = {'orange', 'apple', 'pear', 'banana', 'kiwi', 'strawberry',
              'raspberry', 'cherry'}
    theOrderedSet = sorted(theSet)
    return render_template('list.html',
                           the_title='Set Sample Ordered',
                           myList=theOrderedSet,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           current_time = datetime.now()
                           )



###@app.route('/api/data/stops_times')
@app.route('/api/data/stops_times/')
def get_stops_times_data():
    html_table = get_stops_times()
    return render_template('stops_times.html',
                           the_title='Stops Times',
                           #the_title='https://metrarail.com/tickets',
                           tables=html_table,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )
@app.route('/api/data/stops_times/<TripId>')
def get_stops_times_data_tripNumber(TripId=None):
    if TripId:
        print("True")
        html_table = get_stops_times(TripId)
    else:
        html_table = get_stops_times()
    return render_template('stops_times.html',
                           the_title='Stops Times',
                           tables=html_table,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )



def get_stops_times_data():
    html_table = get_stops_times()
    return render_template('stops_times.html',
                           the_title='Stops Times',
                           #the_title='https://metrarail.com/tickets',
                           tables=html_table,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )

@app.route('/api/data/stops_detail/<stop_id>')
def get_stops_detail_jeff(stop_id=None):
    html_table = get_stops_detail(stop_id=None)
    return render_template('stops_times.html',
                           the_title='Stops Times',
                           # the_title='https://metrarail.com/tickets',
                           tables=html_table,
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )




@app.route('/api/data/<report_type>')
def get_data(report_type=None):
    html_table = get_position_json(report_type)
    Markup(html_table)
    return render_template('MetraAPI.html',
                           the_title=report_type.upper(),
                           ##the_title=Markup('<a href="/api/data/stops">Stops</a>'),
                           table = Markup(html_table),
                           run_date=datetime.now().strftime("%A, %B %d %Y %I:%M%p"),
                           )





@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user{}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)








if __name__ == '__main__':
    app.debug = True
    app.run(port=5002, use_reloader=True)