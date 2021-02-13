
import apiclient.discovery
spreadsheetId='https://docs.google.com/spreadsheets/d/1c4j7jDCPrPpqoXNJdL7qHBMMbC9xlRS3V7WR-yVtyic'

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'rustammazhatov@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()



