#!venv/bin/python3

from options import load_options, OPTION
from file_upload import FileUpload
from services import journal


options = load_options()

if not options.has(OPTION.file_path):
    print(f"--{OPTION.file_path.value} arg is missing. add --help for more info")
    exit(0)

file_path = options.get(OPTION.file_path)
u_file = FileUpload(file_path=file_path)
# Split file into chunks
u_file.split()

print(f"Split file completed. File chunks dumped to {u_file.chunks_path}...")

u_file.load_chunks()

journal.save(u_file)
# init upload
u_file.init_upload()

print(u_file.file_name, u_file.upload_id)

journal.update_meta(u_file, "status", "INIT_UPLOAD")
journal.update_meta(u_file, "upload_id", u_file.upload_id)
journal.update_meta(u_file, "s3_bucket", u_file.s3_bucket)
journal.update_meta(u_file, "s3_key", u_file.s3_key)

u_file.upload_parts()

print(u_file.parts)
journal.update_meta(u_file, "status", "FINISHED_UPLOAD")
for part in u_file.parts:
    journal.update_part(u_file,  part["part_num"], "etag",  part["etag"])

u_file.get_upload_status()

# if upload completed 
# complete upload
u_file.complete_upload()

journal.update_meta(u_file, "status", "COMPLETED_UPLOAD")

# if upload filed or timedout
# cancel upload
# u_file.cancel_upload()
# journal.update_meta(u_file, "status", "CANCELLED_UPLOAD")