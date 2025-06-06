from flask import Blueprint, render_template, request, redirect, url_for
from firebase import firebase_db
from firebase_admin import firestore  # ArrayUnion 등 사용 위해
from flask import Flask

app = Flask(__name__)
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


@app.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    comment = request.form.get('comment')
    if not comment:
        return "댓글 내용을 입력하세요.", 400
    try:
        doc_ref = firebase_db.collection('posts').document(post_id)
        doc = doc_ref.get()
        if not doc.exists:
            return "게시글이 존재하지 않습니다.", 404

        # 기존 댓글 리스트 가져오기
        post = doc.to_dict()
        comments = post.get('comments', [])

        # 새 댓글 추가
        comments.append(comment)

        # 댓글 업데이트
        doc_ref.update({'comments': comments})
        return redirect(url_for('post_detail', post_id=post_id))
    except Exception as e:
        return f"댓글 추가 중 오류 발생: {e}"


@app.route('/post/<post_id>/delete', methods=['POST'])
def delete(post_id):
    try:
        firebase_db.collection('posts').document(post_id).delete()
        return redirect(url_for('board'))
    except Exception as e:
        return f"삭제 중 오류 발생: {e}"

@app.route('/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    doc_ref = firebase_db.collection('posts').document(post_id)
    doc = doc_ref.get()

    if not doc.exists:
        return "해당 게시글이 존재하지 않습니다.", 404

    post = doc.to_dict()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            doc_ref.update({
                'title': title,
                'content': content
            })
            return redirect(url_for('post_detail', post_id=post_id))
        except Exception as e:
            return f"수정 중 오류 발생: {e}"

    return render_template('edit.html', post=post, post_id=post_id)

@app.route('/notice')
def notice():
    return render_template('notice.html')

@app.route('/read')
def read():
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