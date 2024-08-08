from app.config import *

@app.route('/')
def home():
    applications = application_list.to_json()
    return render_template('home.html', applications=applications)

@app.route('/refresh')
def refresh():
    applications = application_list.to_json()
    return jsonify(applications)

@app.route('/add', methods=['POST'])
def add():
    try:
        company = request.form['company']
        role = request.form['role']
        category = request.form['category']
        deadline = request.form['deadline']
        status = request.form['status']
        link = request.form['link']
        date_created = datetime.datetime.now()
        
        application = Application(company, role, category, deadline, status, link, date_created)
        application_list.add(application)
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"success": False}), 400
    

@app.route('/delete', methods=['POST'])
def delete():
    try:
        id = request.form['id']
        application_list.delete(id)
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"success": False}), 400

# 404 Error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500 Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500



