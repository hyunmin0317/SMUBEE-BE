from crawling import course_data
from google_api import login, create, delete_all


if __name__ == '__main__':
    service = login()
    # delete_all(service)

    data_list = course_data('201911019', '1q2w3e4r!!')
    for data in data_list:
        print(data)
        date = data['close'][:10]
        description = '수업명: '+data['course']+'\n진도율: '+data['ratio']

        create(
            service,
            data['name'],
            '상명대학교',
            description,
            date + 'T23:59:59',
            date + 'T23:59:59'
        )