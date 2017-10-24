from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    blogs = Blog.query.all()
    title = "My Blog"
    return render_template('blog.html',title=title, blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['post_title']
        body = request.form['new_post']
        body_error=''
        title_error=''
        if title=="" or body=="":
            if not require_input(title):
                title_error = "A title is required"
            if not require_input(body):
                body_error = "A body is required"
            return render_template('newpost.html',title_error=title_error,body_error=body_error)
        else:
                new_entry = Blog(title, body)
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/blog?id='+str(new_entry.id))
    else:
        return redirect('/blog')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('singlepost.html', blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs, title="Build A Blog")

def require_input(string):
    if string == '':
        return False
    else:
        return True

if __name__ == '__main__':
    app.run()
