from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase 초기화 (한 번만 실행)
cred = credentials.Certificate('de-homepage-firebase-adminsdk-fbsvc-f5575c8f23.json')  # 키 파일 경로 맞게
firebase_admin.initialize_app(cred)
firebase_db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        try:
            # Firestore에 저장
            firebase_db.collection('posts').add({
                'title': title,
                'content': content,
                'views': 0,
                'comments': []
            })
            return redirect(url_for('board'))
        except Exception as e:
            return f"DB 저장 중 오류 발생: {e}"

    return render_template('write.html')

@app.route('/board')  # 게시판 목록 페이지
def board():
    try:
        posts = []
        docs = firebase_db.collection('posts').order_by('title').stream()
        for doc in docs:
            post = doc.to_dict()
            post['id'] = doc.id
            posts.append(post)
    except Exception as e:
        posts = []
        print(f"게시글 목록 로딩 오류: {e}")

    return render_template('board.html', posts=posts)

@app.route('/post/<post_id>')  # 게시글 상세 페이지
def post_detail(post_id):
    try:
        doc_ref = firebase_db.collection('posts').document(post_id)
        doc = doc_ref.get()
        if doc.exists:
            post = doc.to_dict()
            post['id'] = doc.id
            # 조회수 증가
            new_views = post.get('views', 0) + 1
            doc_ref.update({'views': new_views})
            post['views'] = new_views
            return render_template('view.html', post=post)
        else:
            return "게시글을 찾을 수 없습니다.", 404
    except Exception as e:
        return f"DB 오류 발생: {e}"

@app.route('/notice')
def notice():
    return render_template('notice.html')

@app.route('/read')
def read_redirect():
    db = firestore.client()
    posts_ref = db.collection('posts')
    docs = posts_ref.stream()

    posts = []
    for doc in docs:
        post = doc.to_dict()
        post['id'] = doc.id
        posts.append(post)

    print(f"불러온 게시글 수: {len(posts)}")  # 디버깅용 로그
    return render_template('read.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
