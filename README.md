# Kitchen_Story_Lab 

<img src="logo.jpg" alt="logo" width="200px">

## Django로 만든 요리 팁&레시피 공유 블로그

Django를 활용한 레시피 공유 블로그 플랫폼으로, 사용자별 레시피 포스트와 좋아요 기능을 통해 요리 경험을 작성하고 공유할 수 있는 서비스입니다.

## 📅개발 기간
2024.02.05 ~ 2024.02.11

## 🛠 기술 스택
* Backend: Python3.13, Django 5.1, SQLite3

* Frontend: Django Template + Bootstrap, HTML/CSS, Javascript

* Library: TinyMCE(에디터), django-widget-tweaks(폼 렌더링), pillow(이미지처리)

## 💡주요기능
1. 사용자 관리   
* 회원가입/로그인/로그아웃
* 프로필 관리 (이미지, 닉네임, 소개)
* 비밀번호 변경

2. 게시글 관리   
* 게시글 CRUD
* 임시저장 기능
* TinyMCE 에디터 지원
* 이미지 업로드
* 좋아요 기능
* 인기글 표시(조회수 + 좋아요 기반)

3. 레시피 특화 기능   
* 레시피 정보 구조화(조리시간, 난이도, 분량)
* 실시간 타이머 기능
* 타이머 알림 시스템

4. 검색 및 필터링   
* 카테고리별 필터링
* 검색기능(제목, 내용)
* 최신순/인기순 정렬

5. 댓글 시스템 
* 댓글 CRUD
* 작성자 표시
* 시간 표시

## 📁프로젝트 구조
```
📁 kitchen_story_lab
├─📁accounts                   # 사용자 관리 앱
│  ├─migrations
│  │  └─__pycache__
│  └─__pycache__
├─📁blog                       # 블로그 앱
│  ├─migrations
│  │  └─__pycache__
│  └─__pycache__
├─📁config                     # 프로젝트 설정
│  ├─settings.py               # 설정 파일
│  ├─urls.py                   # URL 패턴
│  └─__pycache__
├─📁media                     # 미디어 파일
│  └─📁profiles               # 프로필 이미지
├─📁static                    # 프로젝트 정적 파일
│  ├─📁audio                  # 타이머 알림음
│  ├─📁css                    # 스타일시트
│  ├─📁js                     # 타이머, 좋아요 스크립트
│  └─📁images                 # 이미지 파일
├─📁templates                 # 템플릿 파일
│  ├─base.html                # 기본 레이아웃 템플릿
│  ├─📁accounts               # 사용자 관련 템플릿
│  └─📁blog                   # 블로그 관련 템플릿
├─📄manage.py                  # Django 관리 스크립트
├─📄README.md                  # 프로젝트 문서
└─📄requirements.txt           # 패키지 의존성 목록
```

## ⚙️설치 및 실행방법
1. 저장소 클론
```
git clone [repository URL]
```
2. 가상환경 생성 및 활성화
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. 패키지 설치
```
pip install -r requirements.txt
```
4. 데이터베이스 마이그레이션
```
python manage.py makemigrations
python manage.py migrate
```
5. 서버실행
```
python manage.py runserver
```
## 🔍 API 명세
### 사용자 관리 API
| 메서드 | URL패턴 | 기능 | 인증 필요 |
|--------|-----|-------------|-------------|
| POST | /accounts/signup/ | 회원가입 | X |
| POST | /accounts/login/ | 로그인 | X |
| POST | /accounts/logout/ | 로그아웃 | O |
| GET/POST | /accounts/profile/ | 프로필 조회/수정 | O |
| POST | /accounts/change_password/ | 비밀번호 변경 | O |

### 게시글 API
| 메서드 | URL패턴 | 기능 | 인증 필요 |
|--------|-----|-------------|-------------|
| GET | / | 게시글 목록 | X |
| GET | /<int:pk>/ | 게시글 상세 | X |
| GET | /write/ | 게시글 작성 폼 | O |
| POST | /write/ | 게시글 작성 | O |
| GET | /edit/<int:pk>/ | 게시글 수정 폼 | O |
| POST | /edit/<int:pk>/ | 게시글 수정 | O |
| DELETE | /delete/<int:pk>/ | 게시글 삭제 | O |
| POST | /post/<int:post_pk>/like/ | 좋아요 토글 | O |

### 댓글 API
| 메서드 | URL패턴 | 기능 | 인증 필요 |
|--------|-----|-------------|-------------|
| POST | /<int:post_pk>/comment/create/ | 댓글 작성 | O |
| GET | /comment/<int:pk>/update/ | 댓글 수정 폼 | O |
| POST | /comment/<int:pk>/update/ | 댓글 수정 | O |
| DELETE | /comment/<int:pk>/delete/ | 댓글 삭제 | O |

### 검색/필터 API
| 메서드 | URL패턴 | 기능 | 인증 필요 |
|--------|-----|-------------|-------------|
| GET | /?q=검색어 | 검색 | X |
| GET | /?category=카테고리ID | 카테고리 필터 | X |
| GET | /?sort=latest | 최신순 정렬 | X |
| GET | /?sort=popular | 인기순 정렬 | X |

* O: 인증 필요
* X: 인증 불필요

## WBS
### 2월 5일 (수)
* 프로젝트 환경 설정
* Django 프로젝트 셋업
* requirements.txt 생성 및 패키지 설치
* 데이터베이스(sqlite3) 연결

[User 모델 설계 및 구현]
* AbstractUser 상속
* nickname, profile_image, bio 필드 추가

[로그인/회원가입/로그아웃 시스템 구현]
* CustomUserCreationForm 구현
* 로그인/회원가입 페이지 구현

### 2월 6일 (목)
[Post/Category/Recipe 모델 구현]

[포스트 CRUD 시스템 구현]
* TinyMCE 에디터 연동
* 이미지 업로드 처리
* 임시저장 기능

[메인 화면 구현]
* 네비게이션 바
* 검색 기능
* 인기 게시글 표시
* 카테고리별 필터링

### 2월 7일 (금)

[좋아요 시스템 구현]
* PostLike 모델 구현
* AJAX 처리

[조회수 시스템 구현] 

[댓글 시스템 구현(CRUD)]
* Comment 모델 구현
* 댓글 작성/수정/삭제 기능

### 2월 8일 (토)

[상세 페이지 기능 구현]
* 레시피 정보 표시
* 타이머 기능
* 이전/다음 글 이동

[프로필 시스템 구현]
* 프로필 수정
* 비밀번호 변경

### 2월 9일 (일)
[UI/UX 개선]
* Bootstrap 스타일링
* 반응형 디자인
* 메시지 알림 시스템

### 2월 10일 (월)
[게시글 관리 시스템 보완]
* 인기도 기반 정렬 구현
* 카테고리 관리 개선

[레시피 기능 보완]
* 레시피 타이머 개선
* 난이도 표시 시스템

### 2월 11일 (화)

* 전체 시스템 테스트
* 버그 수정
* README 작성
* 최종 점검

## ERD
![alt text](ERD.png)

## 구현(gif)
#### 회원가입   
![alt text](<회원가입 (2).gif>)
#### 로그인
![alt text](로그인.gif)
#### 비밀번호 & 프로필 변경
![alt text](비밀번호-변경_-프로필-변경.gif)
#### 로그아웃
![alt text](로그아웃.gif)
#### 카테고리 선택
![alt text](카테고리-별-항목.gif)
#### 검색기능
![alt text](검색.gif)
#### 게시물 목록 정렬
![alt text](글-목록-페이지_-정렬.gif)
#### 글 생성 및 글 수정(임시저장 & 수정)
![alt text](임시저장-및-수정.gif)
*(임시저장은 작성자만 볼 수 있음)
![alt text](image.png)
(+ 화면 우측의 관련레시피는 같은 카테고리의 글)
#### 글 삭제
![alt text](<글 삭제.gif>)
#### 댓글 CRUD
![alt text](<댓글 CRUD.gif>)
#### 레시피 정보 & 타이머 
![alt text](<레시피-정보-표시_-타이머 (1).gif>)
#### 좋아요 기능
![alt text](좋아요-증가.gif)

#### ( 글, 목록, 댓글에 이름대신 닉네임이 뜨도록 수정(갱신 안됨))
![alt text](image-1.png)
![alt text](image-3.png)
![alt text](image-2.png)


## 💥 어려웠던 점&문제 해결 내용(추가예정)

