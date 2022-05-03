from read import read


def update(event, service):
    event_id = event.get('id')

    # 원하는 일정의 속성 값을 변경합니다.
    event['summary'] = "(수정된)" + event['summary']

    # 일정 수정 요청하기
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print(updated_event)


if __name__ == '__main__':
    events_result, service = read()
    for event in events_result:
        update(event, service)