from app.config import *


@app.before_request
def load_logged_in_user():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.route('/')
def index():
    """
    Render the index page with a welcome message.
    """
    return render_template('welcome.html')


@app.route('/home')
@login_required
def home():
    """
    Render the home page with a list of applications for the logged-in user.
    """
    applications = (
        Application.query
        .join(Company)
        .filter(Application.user_id == session['user_id'])
        .all()
    )

    return render_template('home.html', applications=applications)

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']

    total = Application.query.filter_by(user_id=user_id).count()

    by_status = (
        db.session.query(Application.status, func.count())
        .filter(Application.user_id == user_id)
        .group_by(Application.status)
        .all()
    )

    by_category = (
        db.session.query(Application.category, func.count())
        .filter(Application.user_id == user_id)
        .group_by(Application.category)
        .all()
    )

    over_time_raw = (
        db.session.query(
            func.date_format(Application.date_created, "%Y-%m").label("month"),
            func.count()
        )
        .filter(Application.user_id == user_id)
        .group_by("month")
        .order_by("month")
        .all()
    )

    # Convert result into two lists: labels and counts
    labels = [row[0] for row in over_time_raw]
    counts = [row[1] for row in over_time_raw]

    return render_template(
        'dashboard.html',
        total=total,
        by_status=by_status,
        by_category=by_category,
        over_time_labels=labels,
        over_time_counts=counts
    )


@app.route('/company/search')
def search_companies():
    query = request.args.get('q', '')
    results = Company.query.filter(Company.name.ilike(f"%{query}%")).limit(10).all()
    return jsonify([{"id": c.id, "name": c.name} for c in results])


@app.route('/add', methods=['POST'])
def add():
    try:
        company_name = request.form['company'].strip()
        role = request.form['role']
        category = request.form['category']
        deadline = request.form['deadline']
        status = request.form['status']
        link = request.form['link']

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
            db.session.commit()

        application = Application(
            role=role,
            category=category,
            deadline=deadline,
            status=status,
            link=link,
            user_id=user_id,
            company_id=company.id
        )

        db.session.add(application)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/edit", methods=["POST"])
def edit_application():
    try:
        data = request.form
        app_id = data["id"]

        application = Application.query.get(app_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        company_name = data["company"].strip()
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
            db.session.flush()

        # Detect and log status change
        old_status = application.status
        new_status = data["status"]
        if old_status != new_status:
            status_log = StatusChange(
                application_id=application.id,
                old_status=old_status,
                new_status=new_status
            )
            db.session.add(status_log)

        # Update the application
        application.company_id = company.id
        application.role = data["role"]
        application.category = data["category"]
        application.deadline = data["deadline"]
        application.status = new_status
        application.link = data["link"]

        db.session.commit()
        return jsonify({"success": True}), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error editing application: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/change-status', methods=['POST'])
def change_status():
    try:
        app_id = request.form['id']
        new_status = request.form['status']

        application = Application.query.get(app_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        old_status = application.status
        if old_status != new_status:
            # Log the change
            status_change = StatusChange(
                application_id=application.id,
                old_status=old_status,
                new_status=new_status
            )
            db.session.add(status_change)

            # Apply the new status
            application.status = new_status

        db.session.commit()
        return jsonify({"success": True}), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in change_status: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/delete', methods=['POST'])
def delete():
    try:
        id = request.form['id']
        application_list.delete(id)
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"success": False}), 400


## User Handling

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for('register'))

        user = User(email=email, name=name, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful')
            return redirect(url_for('home')) 
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('login'))


## Jinja2 custom functions
@app.context_processor
def utility_functions():
    def get_badge_class(status):
        return {
            "Not Started": "bg-secondary text-white",
            "Applied": "bg-primary text-white",
            "Interview": "bg-warning text-dark",
            "Offer": "bg-success text-white",
            "Rejected": "bg-danger text-white"
        }.get(status, "bg-light")
    return dict(get_badge_class=get_badge_class)

@app.template_filter('strftime')
def _jinja2_filter_datetime(value, format='%Y-%m'):
    return value.strftime(format)


# 404 Error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500 Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500



