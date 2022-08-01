from flask import Flask, render_template
from app import app
from one_dimension import script, div


@app.route("/")
@app.route('/index')
def index():
    return render_template('home.html')


@app.route("/1D")
def one():
    return render_template('one_dimension.html', bokeh_script=script, bokeh_div=div)


@app.route("/2D")
def two():
    return render_template('two_dimension.html', bokeh_script=script, bokeh_div=div)

@app.route("/Borden")
def borden():
    return render_template('borden_site.html') #bokeh_script=script, bokeh_div=div)

@app.route("/ADE")
def ade():
    return render_template('ADE_example.html') #bokeh_script=script, bokeh_div=div)