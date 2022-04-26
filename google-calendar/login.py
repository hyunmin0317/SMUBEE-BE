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


if __name__ == '__main__':
    login()