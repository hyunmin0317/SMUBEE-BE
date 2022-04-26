import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def login():
    # 구글 클라우드 콘솔에서 다운받은 OAuth 2.0 클라이언트 파일경로
    creds_filename = 'credentials.json'

    # 사용 권한 지정
    # https://www.googleapis.com/auth/calendar	               캘린더 읽기/쓰기 권한
    # https://www.googleapis.com/auth/calendar.readonly	       캘린더 읽기 권한
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # 파일에 담긴 인증 정보로 구글 서버에 인증하기
    # 새 창이 열리면서 구글 로그인 및 정보 제공 동의 후 최종 인증이 완료됩니다.
    flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
    creds = flow.run_local_server(port=8000)
    service = build('calendar', 'v3', credentials=creds)
    return service


def read(service):
    calendar_id = 'primary'
    today = datetime.date.today().isoformat()
    time_min = '2022-03-01T00:00:00+09:00'
    time_max = '2022-05-01T23:59:59+09:00'
    is_single_events = True
    orderby = 'startTime'

    events_result = service.events().list(calendarId = calendar_id,
                                          timeMin = time_min,
                                          timeMax = time_max,
                                          singleEvents = is_single_events,
                                          orderBy = orderby
                                         ).execute().get('items')
    return events_result

def create(service, summary, location, description, start, end):
    # 구글 캘린더 API 서비스 객체 생성

    event = {
            'summary': summary, # 일정 제목
            'location': location, # 일정 장소
            'description': description, # 일정 설명
            'start': { # 시작 날짜
                'dateTime': start,
                'timeZone': 'Asia/Seoul',
            },
            'end': { # 종료 날짜
                'dateTime': end,
                'timeZone': 'Asia/Seoul',
            },
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

def update(service, event):
    event_id = event.get('id')

    # 원하는 일정의 속성 값을 변경합니다.
    event['summary'] = "(수정된)" + event['summary']

    # 일정 수정 요청하기
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print(updated_event)

def delete(service, event):
    # eventId : 일정을 조회한 후 얻은 id 값을 말합니다.
    eventId = event.get('id')
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    print(f'{eventId} 삭제 완료')