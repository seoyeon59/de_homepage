from flask import Flask, render_template, request

app = Flask(__name__)

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 글쓰기 페이지
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        # 글 저장 처리 (지금은 생략)
        title = request.form['title']
        content = request.form['content']
        # 실제 구현 시 DB에 저장 필요
        return f"제목: {title}, 내용: {content}"
    return render_template('write.html')

# 글 조회 페이지 (더미 예시)
@app.route('/view')
def view():
    return render_template('view.html', title='샘플 제목', content='샘플 내용입니다.')

# 게시판 페이지
@app.route('/board')
def board():
    return render_template('board.html')

# 공지사항 페이지
@app.route('/notice')
def notice():
    return render_template('notice.html')

if __name__ == '__main__':
    app.run(debug=True)
