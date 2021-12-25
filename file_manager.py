from helpers import gen_uid
from fsplit.filesplit import Filesplit
import pathlib
import os
from dotenv import load_dotenv

load_dotenv()

fs = Filesplit()

output_dir="/tmp/python-s3-upload-chunks"

# 1MB = 
mb_size_in_bytes = 1024*1000
mb_amount = 10

class FileManager:
    def __init__(self):
        # create temporary files directory
        pathlib.Path(output_dir).mkdir(exist_ok=True)
    
    def split_file(self, file_path):
        chunks = []
        uid = gen_uid()
        dest = f"{output_dir}/{uid}"
        # create temporary files directory
        pathlib.Path(dest).mkdir(exist_ok=True)

        def split_cb(f, s):
            chunks.append({"path": f, "size": s})
            # print("chunk: {0}, size: {1}".format(f, s))
        
        fs.split(file=file_path, split_size=mb_size_in_bytes*mb_amount, output_dir=dest, callback=split_cb)
        return { "succeeded": True, "dest": dest, "chunks": chunks, "uid": uid }

    def merge_chunks(self, dir_path):
        chunks = []
        def merge_cb(f, s):
            chunks.append({"path": f, "size": s})
            # print("file: {0}, size: {1}".format(f, s))
        fs.merge(input_dir=dir_path, callback=merge_cb, cleanup=True)
        return { "chunks": chunks, "succeeded": True }


