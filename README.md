# Kitchen_Story_Lab

## 📝프로젝트 소개   
Django로 만든 요리 팁&레시피 공유 블로그

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


