from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    scholar_no = db.Column(db.Integer, nullable=False)
    branch = db.Column(db.String(200))
    year = db.Column(db.Integer)

    def __repr__(self):
        return '<Information %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name_input = request.form['name']
        scholar_no_input = request.form['scholar_no']
        branch_input = request.form['branch']
        year_input = request.form['year']

        new_task = Information(
            name=name_input,
            scholar_no=scholar_no_input,
            branch=branch_input,
            year=year_input
        )

        try:
            db.session.add(new_task)
            db.session.commit()
            print('New task added successfully:', new_task)
            return redirect('/')
        except Exception as e:
            print('Error occurred while adding the task:', e)
            return 'An error occurred while adding the task to the database.'
    else:
        tasks = Information.query.all()
        return render_template('base.html', tasks=tasks)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
