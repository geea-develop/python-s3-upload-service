#!venv/bin/python3

from options import load_options, OPTION
from file_upload import FileUpload
from services import journal


options = load_options()

uploads = journal.list_records('files')
# uploads = [f.get('data') for f in uploads]
for u in uploads:
    print(u, "")
    uid = ""
    if u.get('data'):
        uid = u.get('data').get('uid')
    else:
        uid = u.get('uid')
    parts = journal.list_records('files:' + uid)
    for p in parts:
        print(p, "")

# parts = journal.list_records('files:3514a917-3d3c-4312-a8e4-ee5df68afcf1')
# # uploads = [f.get('data') for f in uploads]
# for u in uploads:
#     print(u, "")
#     uid = ""
#     if u.get('data'):
#         uid = u.get('data').get('uid')
#     else:
#         uid = u.get('uid')
#     fi = journal.get_record('files:' + uid, 'meta')
#     print(fi, "")