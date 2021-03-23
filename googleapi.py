import io
import os
from googleapiclient.http import MediaIoBaseDownload

from oauth2client.transport import request
from Google import Create_Service

# API_NAME = 'drive'
# API_VERSION = 'v3'
# CLIENT_SECRET_FILE = 'credentials.json'
# SCOPES = ['https://www.googleapis.com/auth/drive']

# service = Create_Service(CLIENT_SECRET_FILE,API_NAME, API_VERSION, SCOPES) 
# print(dir(service))

# myAblums = service.albums().list().execute()
# print(myAblums)
def file_listing(user_input,service,length):
    file_ids =[]
    file_names =[]
    results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            if item['name']==user_input:
                id =item['id']
    print('id===',id)
    query = f'parents = "{id}"'
    res = service.files().list(q=query).execute()
    print("response",res)
    files = res.get('files')
    print("files",files)
    for i in files:
        file_ids.append(i['id'])
        file_names.append(i['name'])
    print('file ids',file_ids)
  
    if length != len(file_ids):
        file_download(service,file_ids,file_names)
def file_download(service,file_ids,file_names):
    # listdr = os.listdir('/home/actoinfi/presonal datas/telegram bot/down')
    # print('list dir ',listdr)
    
    print("file_names*********",file_names)
    
    for file_id,file_name in zip(file_ids,file_names):
        i=+1
        request = service.files().get_media(fileId = file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh,request=request)
        done = False
        while not done:
            status,done=downloader.next_chunk()
            print('download process{0}'.format(status.progress()*100))
        fh.seek(0)
        with open(os.path.join('down',file_name),'wb') as f:
            f.write(fh.read())
            f.close()
# file_listing(service)