# 운동기록 사이트 만들기

---

### <개요>

운동 습관을 체계적으로 관리하고자 하는 개인적 니즈에서 출발하여, 
단순 반복되는 종목명 타이핑 동작을 최소화하고 운동 및 식단 기록을 간편하게 분석할 수 있는 웹 애플리케이션을 개발하였습니다.

---

### <준비사항>

먼저 사용하게 될 스택들과 요구 사항들을 개략적으로 나열 후 개발하면서 세부 사항을 다듬어가며 개발하고자하였습니다.

- 필요 스택
    - 서버 : Flask, mySQL, matplotlib
    - 서버↔클라이언트 : html, javascript, jinja, jquery, xhr
- 요구 사항
    - 프론트엔드
        - 운동 종목 기입 및 선택 인터페이스
        - 운동 세트수, 반복 횟수, 무게 등 기입 인터페이스
        - 식단 메뉴 기입 및 선택 인터페이스
        - 섭취 음식 중량 기입 인터페이스
        - 분석 결과 및 지침(일별,월별,분기별)
    - 백엔드
        - 클라이언트로부터 받은 데이터를 DB에 저장
        - DB로부터 가져온 데이터로 운동에 필요한 칼로리 계산(소모 칼로리)
        - DB로부터 가져온 데이터로 식단으로 얻게 되는 칼로리 계산(사용 가능 칼로리)
        - 영양 성분 계산
        - 사용자의 체중과 운동량, 영양 섭취 및 성분 균형 등을 고려한 계산 로직
    - ERD (개발 전)  
  
      <img src="https://github.com/giteraction/workout/assets/95407727/c87407e7-5e69-44dd-8b8d-599e61d43839" style="width:500px;">  
        
    - ERD (개발 후)  
        - USER 테이블 > 사용자의 체중, 운동 방향 및 빈도 컬럼으로 변경
        - FOOD 테이블 > 음식의 영양 성분을 담아둘 NUTRIENT 테이블 추가 (칼로리 및 단백질 계산을 위해)
        - EXERCISE 테이블 > 운동 종목 리스트 BODYBUILD 테이블 추가 (서버에서 전달하게끔 변경)
    
    <img src="https://github.com/giteraction/workout/assets/95407727/f48236e0-978a-4979-a12b-00cbb15d2396" style="width:500px;">  

---

### **<개발물 구성>**

1. 전체 구조 및 동작 시나리오 구상

<img src="https://github.com/giteraction/workout/assets/95407727/975900cf-0852-4b90-8b65-ec9fa2c3b9bb" style="width:500px;">
---

1. 인터페이스 디자인
<img src="https://github.com/giteraction/workout/assets/95407727/bbb66228-e0bd-4f74-a3d3-fa038222ce9b" style="width:500px;">

---

1. 서버 연동 및 테스트 
<img src="https://github.com/giteraction/workout/assets/95407727/ba4d5687-dfb6-4c11-8b04-f96f16628a82" style="width:500px;">
---

### <개발 과정 중 마일스톤 리스트>
<img src="https://github.com/giteraction/workout/assets/95407727/d09fa097-45b4-4e8e-85b6-2a39d6a38f78" style="width:500px;">


---

### <최종 완성>

- 사용자 설정
<img src="https://github.com/giteraction/workout/assets/95407727/0d401804-49ab-4b3b-a55f-4b518f6cec92" alt="사용자 설정" style="width:500px;">

- 운동 기록 저장
<img src="https://github.com/giteraction/workout/assets/95407727/47bdf292-ee82-464a-8a62-5282cd4e2707" alt="운동 기록 저장" style="width:500px;">

- 운동 기록보기
<img src="https://github.com/giteraction/workout/assets/95407727/730f000b-0799-4532-bffd-c7353de649a2" alt="운동 기록 보기" style="width:500px;">

- 새로운 운동 추가
<img src="https://github.com/giteraction/workout/assets/95407727/8b3b0263-67d4-48b5-877d-dac9fd25cc39" alt="새로운 운동 추가" style="width:500px;">

- 음식 기록 저장
<img src="https://github.com/giteraction/workout/assets/95407727/29f792c6-19f4-48f4-85f9-17b87b5b9041" alt="음식 기록 저장" style="width:500px;">

- 새로운 음식 추가
<img src="https://github.com/giteraction/workout/assets/95407727/ebc32e61-a7b7-4d20-bd9e-bf84fbe2bbfc" alt="새로운 음식 추가" style="width:500px;">

- 식단 기록 보기
<img src="https://github.com/giteraction/workout/assets/95407727/10dccb55-1a18-4360-b9b6-cd920a26145f" alt="식단 기록 보기" style="width:500px;">


---

### <후기>

본 프로젝트는 개발이 진행되면서 사용자의 행동 데이터를 기반으로 피드백을 제공하는 시스템으로 발전시켰습니다. 
개발 과정에서 기능 요구사항을 세분화하고, 테스트 중 도출된 아이디어를 반영하여 기능을 확장하였습니다. 
이를 통해 클라이언트의 니즈를 구조화하고 실질적인 기능으로 구현하는 경험을 하였습니다.

# project-workout_management
# project-workout_management
