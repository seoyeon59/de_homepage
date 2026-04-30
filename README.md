# 🚀 소학회 홈페이지 개발 및 로그 기반 보안 위협 분석 프로젝트

서울여자대학교 데이터사이언스학과 소학회 **'데이터 엔지니어스(Data Engenius)'** 활동의 일환으로 진행된 프로젝트입니다. Flask 기반의 웹 서비스를 구축하고, 리눅스 환경에 배포한 후 축적된 로그 데이터를 분석하여 보안 위협을 탐지하는 전 과정을 수행했습니다.

---

## 1. 프로젝트 개요
- **홈페이지 제작**: 소학회 소개 및 스터디 자료 공유를 위한 게시판 기반 웹 사이트 구축
- **배포 및 운영**: Apache 서버를 통한 리눅스 환경 배포 및 실서비스 운영
- **로그 분석**: 약 6주간 수집된 접속 로그(`access_log`, `error_log`)를 활용한 공격 유형 분석

---

## 2. 주요 기능 및 기술 스택

### 🛠 Tech Stack
| 구분 | 기술 |
| :--- | :--- |
| **Backend** | Python (Flask), Flask-SQLAlchemy |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | MariaDB, SQL |
| **Server/Infra** | Linux, Apache, Bash |
| **Data Analysis** | Python (Pandas), SQL, API Crawling |


### 🖥 주요 기능
- **메인 페이지**: 학회 활동 목적, 목표 및 기수별 활동 상황 소개
- **게시판 시스템**: 
  - 공지사항 관리 및 글 목록 조회 (DB 연동)
  - 게시글 작성, 수정, 조회수 카운트 기능
  - 댓글 시스템 및 MariaDB 데이터 연동

---

## 3. 로그 기반 공격 유형 분석 (Main Analysis)
홈페이지 배포 후 발생한 실제 트래픽 데이터를 바탕으로 데이터 엔지니어링 관점의 분석을 진행했습니다.

### 🔍 데이터 전처리 및 분석 방법
1. **ETL 프로세스**: Raw 로그 파일을 텍스트 파일(.txt)로 변환 후 Python을 사용하여 파싱한 후, 구분자 처리를 통해 구조화된 CSV 데이터로 변환
2. **IP 위치 추적**: 오픈 API(KISA)를 연동하여 접속 IP별 국가 위치 크롤링 및 통계 산출
3. **접속 패턴 분석**: IP별 접속 횟수, 요일/시간대별 트래픽 집중 현상 파악

### 🛡 보안 위협 탐지 결과
- **에러 로그 매핑**: `access_log`의 특정 IP와 시간을 Key로 설정하여 `error_log`와 매핑, 특정 시점의 에러 발생 원인 추적
- **악성 코드 탐지**: GET/POST 요청 메시지 분석을 통해 SQL Injection 및 악성 스크립트 삽입 시도 패턴 발견
- **프로토콜 분석**: HTTP/1.0과 HTTP/1.1의 연결 관리 방식 차이를 이해하고, HTTP/2.0에서 나타나는 특이 메소드(PRI, HELP)를 통한 공격 시도 확인

---

## 4. DB 스키마 및 분석 쿼리
프로젝트에 사용된 핵심 SQL 구조입니다.

```sql
-- 400번대 에러(클라이언트 오류)를 발생시킨 IP를 시간순으로 정렬하여 분석
SELECT ip, status, time 
FROM homepage_data 
WHERE status LIKE '4%' 
GROUP BY ip 
ORDER BY time;
