import datetime
from login import login


def read():
    service = login()
    calendar_id = 'primary'
    today = datetime.date.today().isoformat()
    tomorrow = (datetime.date.today()+datetime.timedelta(days=1)).isoformat()
    time_min = today + 'T00:00:00+09:00'
    time_max = tomorrow + 'T23:59:59+09:00'
    max_results = 5
    is_single_events = True
    orderby = 'startTime'

    events_result = service.events().list(calendarId = calendar_id,
                                          timeMin = time_min,
                                          timeMax = time_max,
                                          maxResults = max_results,
                                          singleEvents = is_single_events,
                                          orderBy = orderby
                                         ).execute().get('items')
    return events_result, service

if __name__ == '__main__':
    events_result = read()
    print(events_result)