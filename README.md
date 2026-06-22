# ☕ Coffee Kiosk

Python과 tkinter 라이브러리를 활용하여 개발한 **커피 카페 키오스크** 프로토타입입니다.

기본적인 메뉴 선택·장바구니·결제 흐름뿐만 아니라 메뉴별 옵션, 매장/포장 재확인, 한/영 언어 전환, 무활동 타임아웃, 영수증 선택 등을 구현하여 실제 키오스크에 가까운 주문 경험을 제공합니다.

## 🎯 프로젝트 소개

Coffee Kiosk는 Python과 tkinter 라이브러리를 활용하여 개발한 카페 주문 키오스크 애플리케이션입니다.

커피·논커피·주스·티/차·디저트 등 **36종 메뉴**와 메뉴별 옵션(HOT/ICE, 얼음·물·당도, 샷 추가 등), JSON 기반 데이터 관리, 화면 전환, 장바구니 시스템 등 키오스크의 핵심 기능들을 구현하였으며, 학습·포트폴리오용으로 제작되었습니다.

## ✨ 주요 기능

### 🌐 한/영 언어 전환

시작 화면에서 **Korean ↔ English** 전환

- UI 문구, 메뉴명, 옵션명, 장바구니 요약 모두 언어에 맞게 표시
- `data/menu.json`, `data/options.json`에 영문명(`name_en`) 분리 저장

### 📋 카테고리별 메뉴

5개 카테고리, 총 36종 메뉴

- **커피** — 아메리카노, 카페라떼, 콜드브루 등
- **논커피** — 초코라떼, 딸기라떼, 자몽에이드 등
- **주스** — 오렌지, 사과, 망고, 포도 등
- **티/차** — 티백, 아이스티, 밀크티, 허브티 등
- **디저트** — 케이크, 쿠키, 크로아상 등

### ⚙️ 메뉴별 옵션

메뉴마다 다른 옵션 그룹 적용

- **온도** — HOT / ICE
- **물·얼음·당도** — 많이 / 보통 / 적게
- **샷 추가** — +500원
- 옵션 영역 스크롤 + 하단 **담기** 버튼 고정

### 🛒 장바구니

선택한 메뉴와 옵션을 장바구니에서 관리

- 옵션 조합별 개별 항목 관리
- 수량 증감 (+ / −)
- **초기화** / **결제하기** 버튼

### 🍽 매장 / 포장 재확인

결제 직전 주문 방식을 다시 선택·확인

- **매장에서 먹고 가기** / **포장해 가기** 선택
- 결제하기 클릭 시 선택 내용 확인 팝업

### 💳 결제 · 영수증 · 완료

결제 수단 선택 후 주문 완료까지 이어지는 흐름

- 결제 수단: 카드 / 현금 / 모바일
- 결제 전 최종 확인 팝업
- **결제 중** 화면 (5초) → **결제 완료** → 영수증 선택
- 영수증 출력 여부 선택 (받기 / 괜찮아요)
- 주문 완료 후 **커피** 카테고리로 초기화

### ⏱ 무활동 타임아웃

메뉴 화면에서 **30초** 동안 아무 동작이 없으면 자동으로 시작 화면으로 복귀

- **10초 남았을 때** 화면 하단에 알림 표시
- **「선택하지 않으면 N초 후 처음 화면으로 돌아갑니다」** — 남은 시간 카운트다운
- 터치·클릭·스크롤 시 알림 사라지고 **30초 타이머 리셋**

## 🔄 주문 흐름

```
시작 → 메뉴 선택 → (옵션) → 장바구니
  → 주문 방식 확인 → 결제 → 결제 중 → 결제 완료 → 영수증 → 시작
```

## 🖥️ 키오스크 화면

### 시작 화면

![시작 화면](docs/screenshots/ko-01-welcome.png)

- **주문 시작하기** 버튼으로 메뉴 화면 이동
- 우상단 **English** 버튼으로 영어 전환

### 메뉴 선택

![메뉴 선택](docs/screenshots/ko-02-menu.png)

- 카테고리 탭 (커피 / 논커피 / 주스 / 티·차 / 디저트)
- 메뉴별 이름, 설명, 시작 가격 표시
- **옵션 선택** 버튼으로 커스터마이징
- **← 처음으로** 버튼, 장바구니 요약 표시

### 무활동 알림

![무활동 알림](docs/screenshots/ko-12-idle-warning.png)

- 30초 무활동 시 **10초 전**부터 하단 알림 표시
- **선택하지 않으면 N초 후 처음 화면으로 돌아갑니다**
- 메뉴 선택·스크롤 등 조작 시 타이머 초기화

### 옵션 선택

![옵션 선택](docs/screenshots/ko-03-options.png)

- HOT / ICE, 물·샷 등 메뉴별 옵션
- 옵션에 따른 가격 실시간 반영
- **취소** / **담기** 버튼

### 장바구니

![장바구니](docs/screenshots/ko-04-menu-cart.png)

- 담은 메뉴, 선택 옵션, 수량·가격 표시
- 수량 조절 (+ / −)
- **합계** 금액, **초기화** / **결제하기**

### 주문 방식 확인

![주문 방식 확인](docs/screenshots/ko-05-order-type.png)

- **매장에서 먹고 가기** / **포장해 가기** 선택
- 선택 후 **결제하기** 버튼 활성화

### 주문 방식 확인 팝업

![주문 방식 확인 팝업](docs/screenshots/ko-06-order-type-confirm.png)

- 선택한 주문 방식 재확인
- **Yes** / **No** 로 최종 확인

### 결제

![결제](docs/screenshots/ko-07-payment.png)

- 주문 내역 (메뉴, 옵션, 주문 방식)
- 결제 수단 선택 (카드 / 현금 / 모바일)
- **결제하기** 버튼

### 결제 확인 팝업

![결제 확인 팝업](docs/screenshots/ko-08-payment-confirm.png)

- 주문 방식 + 결제 수단 + 금액 최종 확인
- **Yes** / **No**

### 결제 중

![결제 중](docs/screenshots/ko-11-processing.png)

- **결제 중입니다** — 5초간 결제 진행 연출
- **잠시만 기다려 주세요**

### 결제 완료

![결제 완료](docs/screenshots/ko-10-complete.png)

- **결제가 완료되었습니다** + 주문번호
- 주문 방식 · 결제 수단 · 금액 요약
- 잠시 후 영수증 화면으로 자동 이동

### 영수증

![영수증](docs/screenshots/ko-09-receipt.png)

- **영수증을 받으시겠습니까?**
- **괜찮아요** / **받기**
- 선택 후 **처음 화면**으로 복귀 (다음 주문 시 **커피** 카테고리)

### 🌐 English Version

시작 화면에서 **English**를 선택하면 아래와 같이 영어 UI로 이용할 수 있습니다.

![Welcome](docs/screenshots/en-01-welcome.png)

![Menu](docs/screenshots/en-02-menu.png)

![Order Type](docs/screenshots/en-03-order-type.png)

![Payment](docs/screenshots/en-04-payment.png)

![Receipt](docs/screenshots/en-05-receipt.png)

![Complete](docs/screenshots/en-06-complete.png)

## 🧠 객체지향 구조

### KioskApp

키오스크 애플리케이션의 핵심 로직 담당

- 화면 전환 (welcome / menu / order_confirm / payment / receipt / complete)
- 장바구니·주문 방식·언어 상태 관리
- 주문 완료 처리 및 초기화

### BaseScreen

모든 화면의 기본 클래스

- `on_show()` / `on_hide()` 화면 전환 훅
- 공통 스타일 및 앱 참조

### MenuScreen / PaymentScreen 등

각 화면별 UI 및 이벤트 처리

- WelcomeScreen — 시작 화면, 언어 전환
- MenuScreen — 메뉴·장바구니, 무활동 타임아웃(10초 전 알림)
- OrderConfirmScreen — 매장/포장 선택 및 확인
- PaymentScreen — 결제 수단 선택
- ProcessingScreen — 결제 진행 중 (5초)
- CompleteScreen — 결제 완료, 영수증 화면으로 이동
- ReceiptScreen — 영수증 출력 여부

### Cart / CartItem

장바구니 데이터 관리

- 옵션 조합별 항목 추가·수량 변경·삭제
- 합계 금액 계산
- 언어별 옵션 요약 표시

### MenuItem / OptionGroup

메뉴·옵션 데이터 관리

- JSON 파일 로드
- 메뉴별 옵션 그룹 연결
- 추가 금액 계산, 다국어 이름 반환

### OptionDialog

메뉴 옵션 선택 팝업

- 라디오 버튼 옵션 UI
- 실시간 가격 반영
- 스크롤 영역 + 하단 담기 버튼 고정

## 📁 프로젝트 구조

```
Kiosk/
│
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── menu.json
│   └── options.json
│
├── docs/
│   └── screenshots/
│
├── models/
│   ├── menu.py
│   ├── options.py
│   └── cart.py
│
└── ui/
    ├── app.py
    ├── i18n.py
    ├── order_types.py
    ├── styles.py
    ├── widgets.py
    ├── dialogs/
    │   └── option_dialog.py
    └── screens/
        ├── welcome.py
        ├── menu.py
        ├── order_confirm.py
        ├── payment.py
        ├── processing.py
        ├── complete.py
        └── receipt.py
```

## ▶ 실행 방법

### 1. 프로젝트 다운로드

```bash
git clone https://github.com/jwoochoi2001/Coffee-Kiosk.git
```

### 2. 프로젝트 폴더 이동

```bash
cd Coffee-Kiosk
```

### 3. 실행

```bash
python3 main.py
```

> tkinter는 Python 기본 내장이라 별도 패키지 설치가 필요 없습니다.

## 💻 개발 환경

Language : Python 3  
GUI : tkinter (내장)  
Data : JSON  
IDE : PyCharm  
OS : macOS

## 📌 구현 기능

- 한/영 언어 전환
- 카테고리별 메뉴 (36종)
- 메뉴별 옵션 (HOT/ICE, 얼음·물·당도, 샷 등)
- 장바구니 (옵션별 관리, 수량 조절)
- 매장 / 포장 재확인 + 확인 팝업
- 결제 수단 선택 (카드 / 현금 / 모바일)
- 결제 최종 확인 팝업
- 결제 중 화면 (5초)
- 결제 완료 화면
- 영수증 출력 여부 선택
- 주문 후 커피 카테고리 초기화
- 메뉴 화면 30초 무활동 타임아웃 (10초 전 하단 알림)
- JSON 기반 메뉴·옵션 데이터

## 👨‍💻 개발자

**최정우**

GitHub: https://github.com/jwoochoi2001

**36종 메뉴를 모두 주문해 보세요!**

## 🚀 소식

**[2026년]**

- **6월 18일** — 프로젝트 개발 시작, 기본 화면 흐름 및 메뉴·장바구니 구현
- **6월 19일** — 메뉴별 옵션 시스템, 매장/포장 재확인, 영수증 화면 추가
- **6월 20일** — 한/영 언어 전환, 무활동 타임아웃(30초), UI 개선 및 README 작성
