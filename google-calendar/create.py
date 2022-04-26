import datetime
from googleapiclient.discovery import build
from login import login


# 구글 캘린더 API 서비스 객체 생성
creds = login()
today = datetime.date.today().isoformat()
service = build('calendar', 'v3', credentials=creds)

event = {
        'summary': 'itsplay의 OpenAPI 수업', # 일정 제목
        'location': '서울특별시 성북구 정릉동 정릉로 77', # 일정 장소
        'description': 'itsplay와 OpenAPI 수업에 대한 설명입니다.', # 일정 설명
        'start': { # 시작 날짜
            'dateTime': today + 'T09:00:00',
            'timeZone': 'Asia/Seoul',
        },
        'end': { # 종료 날짜
            'dateTime': today + 'T10:00:00',
            'timeZone': 'Asia/Seoul',
        },
        'recurrence': [ # 반복 지정
            'RRULE:FREQ=DAILY;COUNT=2' # 일단위; 총 2번 반복
        ],
        'attendees': [ # 참석자
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': { # 알림 설정
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60}, # 24 * 60분 = 하루 전 알림
                {'method': 'popup', 'minutes': 10}, # 10분 전 알림
            ],
        },
    }

# calendarId : 캘린더 ID. primary이 기본 값입니다.
event = service.events().insert(calendarId='primary', body=event).execute()
print('Event created: %s' % (event.get('htmlLink')))