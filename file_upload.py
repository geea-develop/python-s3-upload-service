from services import file_manager, upload_manager
import csv

class FileUpload:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = file_path.split("/")[-1]

    def split(self):
        res = file_manager.split_file(file_path=self.file_path)
        if not res["succeeded"]:
            print("split file ran into an error")
            exit(0)
        if not res["dest"]:
            print("missing split files destination")
            exit(0)
        self.chunks_path = res["dest"]
        self.uid = res["dest"].split("/")[-1]

    def load_chunks(self):
        fs_manifest_path = "fs_manifest.csv"
        if hasattr(self, 'chunks') and self.chunks:
            return self.chunks

        self.chunks = []
        with open(f"{self.chunks_path}/{fs_manifest_path}", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                file_name = row[0]
                # skip first row
                if file_name != "filename":
                    self.chunks.append({
                        "name": file_name,
                        "path": f"{self.chunks_path}/{file_name}"
                    })
    
    def init_upload(self):
        res = upload_manager.init_upload(self.file_name)
        if not res["succeeded"]:
            print("init upload ran into an error")
            exit(0)
        if not res["upload_id"]:
            print("missing upload id")
            exit(0)
        if not res["bucket"]:
            print("missing upload destination bucket")
            exit(0)
        if not res["key"]:
            print("missing upload destination key")
            exit(0)

        self.upload_id = res["upload_id"]
        self.s3_bucket = res["bucket"]
        self.s3_key = res["key"]

    def upload_parts(self):
        self.parts = []
        self.counter = 0
        for fi in self.chunks:
            self.counter = self.counter + 1
            # part_num = str(self.counter)
            with open(fi["path"], 'rb') as fc:
                file_body = fc.read()
                part = {
                    "counter": self.counter,
                    "part_num": self.counter,
                    "name": self.file_name,
                    "path": fi["path"]
                }
                print(f"Uploading part {self.counter} ...")
                try:
                    response = upload_manager.upload_part(file_body, self.file_name, self.counter, self.upload_id)
                    # print(response, "\n")
                    part["etag"] = response["ETag"]
                finally:
                    print(f"Part {self.counter} completed.")
                    self.parts.append(part)

    def get_upload_status(self):
        res = upload_manager.list_uploaded_files()
        print(res)
        return { "succeeded": True }    
    
    def complete_upload(self):
        res = upload_manager.complete_upload(self.file_name, self.parts, self.upload_id)
        print(res)

    def cancel_upload(self):
        res = upload_manager.cancel_upload(self.file_name, self.parts, self.upload_id)
        print(res)