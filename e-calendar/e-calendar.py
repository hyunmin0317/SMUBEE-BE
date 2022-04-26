from crawling import course_data
from google_api import login, create, read, delete


def delete_all(service):
    events_result = read(service)
    for event in events_result:
        delete(service, event)

if __name__ == '__main__':
    service = login()
    # delete_all(service)

    data_list = course_data('201911019', '1q2w3e4r!!')
    for data in data_list:
        print(data)
        date = data['close'][:10]
        create(
            service,
            data['name'],
            '상명대학교',
            data['ratio'],
            date + 'T23:59:59',
            date + 'T23:59:59'
        )