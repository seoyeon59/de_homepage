from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# 실제 DB 연결은 추후 적용
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        db='your_database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 글쓰기 페이지
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
            cursor.execute(sql, (title, content))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('board'))
        except Exception as e:
            return f"DB 저장 중 오류 발생: {e}"

    return render_template('write.html')

# 글 목록
@app.route('/board')
def board():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT id, title FROM posts ORDER BY id DESC"
        cursor.execute(sql)
        posts = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        posts = []
    return render_template('board.html', posts=posts)

# 글 상세 보기
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(sql, (post_id,))
        post = cursor.fetchone()
        cursor.close()
        conn.close()

        if post:
            return render_template('view.html', post=post)
        else:
            return "게시글을 찾을 수 없습니다.", 404
    except Exception as e:
        return f"DB 오류 발생: {e}"

# 공지사항 페이지
@app.route('/notice')
def notice():
    return render_template('notice.html')

if __name__ == '__main__':
    app.run(debug=True)