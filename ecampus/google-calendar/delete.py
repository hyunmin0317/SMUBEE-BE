from read import read


def delete(event, service):
    # eventId : 일정을 조회한 후 얻은 id 값을 말합니다.
    eventId = event.get('id')
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    print(f'{eventId} 삭제 완료')


if __name__ == '__main__':
    events_result, service = read()
    for event in events_result:
        delete(event, service)