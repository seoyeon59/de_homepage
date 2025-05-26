from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # flash 메시지를 위해 비밀키 설정

# 홈페이지 라우트
@app.route('/')
def index():
    return render_template('index.html')

# 게시판 라우트 (기능 구현 예정)
@app.route('/board')
def board():
    return render_template('board.html')

# 글쓰기 라우트 (기능 구현 예정)
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # 실제 저장 없이 알림만 표시
        flash('글이 작성되었습니다.')
        return redirect(url_for('board'))
    return render_template('write.html')

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
