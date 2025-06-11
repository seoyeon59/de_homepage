from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# MariaDB 연결 설정

user = 'root'
password = "bear0205%21%40%21%40"
host = '127.0.0.1'      # 또는 IP
port = 3306           # 보통 3306
db_name = 'de_homepage' # HeidiSQL에서 미리 만든 DB 이름

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 모델 정의
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# DB 초기화 (초기 실행 시 필요)
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        try:
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('board'))
        except Exception as e:
            return f"DB 저장 중 오류 발생: {e}"

    return render_template('write.html')

@app.route('/board')
def board():
    try:
        posts = Post.query.order_by(Post.title).all()
    except Exception as e:
        posts = []
        print(f"게시글 목록 로딩 오류: {e}")
    return render_template('board.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404

    post.views += 1
    db.session.commit()
    return render_template('view.html', post=post)

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    content = request.form.get('comment')
    if not content:
        return "댓글 내용을 입력하세요.", 400
    try:
        comment = Comment(post_id=post_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post_id))
    except Exception as e:
        return f"댓글 추가 중 오류 발생: {e}"

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete(post_id):
    try:
        post = Post.query.get(post_id)
        if not post:
            return "삭제할 게시글이 존재하지 않습니다.", 404
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('board'))
    except Exception as e:
        return f"삭제 중 오류 발생: {e}"

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = Post.query.get(post_id)
    if not post:
        return "해당 게시글이 존재하지 않습니다.", 404

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            post.title = title
            post.content = content
            db.session.commit()
            return redirect(url_for('post_detail', post_id=post_id))
        except Exception as e:
            return f"수정 중 오류 발생: {e}"

    return render_template('edit.html', post=post, post_id=post_id)

@app.route('/notice')
def notice():
    return render_template('notice.html')

@app.route('/read')
def read():
    posts = Post.query.all()
    return render_template('read.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
