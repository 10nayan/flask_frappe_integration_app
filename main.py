from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import random

app = Flask(__name__)
BASE_URL = "http://0.0.0.0:8000"

@app.route("/")
def index():
    car_url = f"{BASE_URL}/api/resource/Car?fields=[%22english_name%22,%20%22arabic_name%22,%20%22car_id%22,%20%22launch_date%22,%20%22company%22,%22colour_id%22,%20%22model%22]"
    auth_header = {"Authorization": "token 361fa6d3fa4e7da:c6d6330341528b1"}
    response = requests.get(car_url, headers = auth_header)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        all_cars = response_data.get('data')[:5]
    else:
        all_cars = []
    print(all_cars)
    return render_template("index.html", cars = all_cars)

@app.route("/<car_id>")
def detail(car_id):
    car_url = f"{BASE_URL}/api/resource/Car/{car_id}"
    auth_header = {"Authorization": "token 361fa6d3fa4e7da:c6d6330341528b1"}
    response = requests.get(car_url, headers = auth_header)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        car = response_data.get('data')
    else:
        car = []
    return render_template("detail.html", car = car)

@app.route("/delete/<car_id>", methods = ["GET"])
def delete(car_id):
    car_url = f"{BASE_URL}/api/resource/Car/{car_id}"
    auth_header = {"Authorization": "token 361fa6d3fa4e7da:c6d6330341528b1"}
    response = requests.delete(car_url, headers = auth_header)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        car = []
    return render_template("index.html", car = car)

@app.route("/create", methods = ["POST"])
def create():
    car_id = random.randint(100,999)
    ename = request.form.get('ename')
    aname = request.form.get('aname')
    model = request.form.get('model')
    company = request.form.get('company')
    launch_date = request.form.get('launch_date')
    year = request.form.get('year')
    colour_id = request.form.get('colour_id')
    car_url = f"{BASE_URL}/api/resource/Car"
    body = json.dumps({
        'car_id': car_id,
        'english_name': ename,
        'arabic_name': aname,
        'launch_date': launch_date, 
        'company': company, 
        'colour_id': colour_id, 
        'model': model,
        'year': year
    })
    auth_header = {"Authorization": "token 361fa6d3fa4e7da:c6d6330341528b1"}
    response = requests.post(car_url, headers = auth_header, data = body)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route("/update/<car_id>", methods = ["POST"])
def update(car_id):
    updated_body = {}
    ename = request.form.get('ename')
    aname = request.form.get('aname')
    model = request.form.get('model')
    company = request.form.get('company')
    launch_date = request.form.get('launch_date')
    year = request.form.get('year')
    colour_id = request.form.get('colour_id')
    if ename:
        updated_body['english_name'] = ename
    if aname:
        updated_body['arabic_name'] = aname
    if model:
        updated_body['model'] = model
    if company:
        updated_body['company'] = company
    if launch_date:
        updated_body['launch_date'] = launch_date
    if year:
        updated_body['year'] = year
    if colour_id:
        updated_body['colour_id'] = colour_id

    car_url = f"{BASE_URL}/api/resource/Car/{car_id}"
    auth_header = {"Authorization": "token 361fa6d3fa4e7da:c6d6330341528b1"}
    response = requests.patch(car_url, headers = auth_header, data = json.dumps(updated_body))
    print(response.status_code, updated_body, response.text)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True, port = 8080)