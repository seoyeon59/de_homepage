# firebase.py
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 앱이 이미 초기화되었는지 확인
if not firebase_admin._apps:
    cred = credentials.Certificate('dataengenius-c0d6c-firebase-adminsdk-fbsvc-cb7de035ea.json')
    firebase_admin.initialize_app(cred)

# 클라이언트 객체를 모듈 전체에서 재사용
firebase_db = firestore.client()
