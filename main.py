import argparse
import csv
import os
from file_manager import FileManager
from journal import Journal
from upload_manager import UploadManager
from datetime import datetime
from dotenv import load_dotenv

class Options:
    pass

options = Options()
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='File path to be uploaded', type=str)
args = parser.parse_args(namespace=options)

load_dotenv()

file_manager = FileManager()
upload_manager = UploadManager(bucket=os.getenv("S3_BUCKET", "my-s3-bucket"), prefix=os.getenv("S3_PREFIX", "my-folder"))
journal = Journal(os.getenv("DYNAMODB_TABLE", "Uploads"))

if options.file is None:
    print("[--file] is missing")
    exit(0)

# main_file_name = options.file.split("/")[-1]
# res = upload_manager.init_upload(main_file_name)
# upload_id = res["upload_id"]
# parts = []
# counter = 0
# with open(options.file, 'rb') as f:
#     while True:
#         piece = f.read(10000000) # roughly 10 mb parts
#         counter = counter + 1
#         response = upload_manager.upload_part(piece, main_file_name, counter, upload_id)
#         print(response, "\n")
#         parts.append({
#             "counter": counter,
#             "part_num": counter,
#             "etag": response["ETag"],
#             "name": main_file_name,
#         })
#         if piece == b'':
#             break

# # complete upload
# res = upload_manager.complete_upload(main_file_name, parts, upload_id)
# print(res)

# exit(0)   
# with open('movie.mp4', 'rb') as f:
#     while True:
#         piece = f.read(10000000) # roughly 10 mb parts
#         if piece == b'':
#             break

main_file_name = options.file.split("/")[-1]
res = file_manager.split_file(options.file)
uid = res["uid"]
my_date = datetime.now()
my_iso_date = my_date.isoformat()
journal.put_record("files", my_iso_date, {"uid": uid})
# Todo: save >>  file_path, file_name, chunks_path, uid
metadata = {
    "dest": res["dest"],
    "uid": uid,
    "chunks_count": len(res["chunks"])
}
chunks_path = res["dest"]

# merge_chunks(chunks_path)
# print("file_manager.merge_chunks", {"response": res})

files = []
with open(chunks_path + '/fs_manifest.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        file_name = row[0]
        if file_name != "filename":
            # print(file_name)
            files.append({
                "name": file_name,
                "path": f"{chunks_path}/{file_name}"
            })

# init upload
res = upload_manager.init_upload(main_file_name)
upload_id = res["upload_id"]
metadata["upload_id"] = upload_id
metadata["bucket"] = res["bucket"]
metadata["key"] = res["key"]
print(res, "\n")
journal.put_record(f"file:{uid}", "metadata", metadata)

print(files, "\n")

parts = []
# Upload each part
counter = 0
for fi in files:
    counter = counter + 1
    part_num = str(counter)
    with open(fi["path"], 'rb') as fc:
        file_body = fc.read()
        # print(file_body)
        response = upload_manager.upload_part(file_body, main_file_name, counter, upload_id)
        print(response, "\n")
        parts.append({
            "counter": counter,
            "part_num": counter,
            "etag": response["ETag"],
            "name": main_file_name,
        })
        

print(parts, "\n")   
# upload files
# res = upload_manager.upload_files(main_file_name, files, upload_id)
# parts = res["parts"]
# print(res)

# list uploaded files
# res = upload_manager.list_uploaded_files()
# print(res)

# list uploaded files by marker
# Todo: use generators to iterate through uploaded files
# res = upload_manager.list_uploaded_files_by_marker()
# print(res)

# complete upload
res = upload_manager.complete_upload(main_file_name, parts, upload_id)
print(res)

# cancel upload
# res = upload_manager.cancel_upload(main_file_name, upload_id)
# print(res, "\n")

# Cleanup
print(journal.get_record("files", my_iso_date), "\n")
print(journal.get_record(f"file:{uid}", "metadata"), "\n")
# journal.delete_record("files", my_iso_date)
# journal.delete_record(f"file:{uid}", "metadata")