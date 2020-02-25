from twitter_web_app import *

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=['GET', "POST"])

def calc():
    if request.method == 'POST':
        map_generator(locations_to_coords(find_friends_locations(get_account_api(list(request.form.items())[0][1]))))                                      #res = int(request.form['num1']) + int(request.form['num2'])
    return render_template('calc.html', res=6)     #request.form["Enter twitter account"])

if __name__ == "__main__":
    app.run(debug=True)