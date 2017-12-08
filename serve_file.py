import sys 
import os
from http.server import SimpleHTTPRequestHandler
import socketserver

PORT = 80
BUFFER_SIZE = 100 * 1024


if len(sys.argv) != 2:
	print("Please pass a filename to serve.")
	sys.exit()

filename = sys.argv[1]

def strip_path(file_name_path):
	idx = file_name_path.rfind("\\")
	if idx != -1:
		return file_name_path[idx + 1:]
	else:
		return file_name_path

class FileServerRequestHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		global filename	
		global BUFFER_SIZE

		if self.client_address[0] != "127.0.0.1":
			print("Bad request from non localhost")
			self.send_response(404)
			return

		print("Request received. Now serving file " + filename)

		self.send_response(200)
		file_size = os.path.getsize(filename)
		self.send_header("Content-disposition", " attachment; filename=" + strip_path(filename))
		self.send_header("Content-type", "application/force-download")
		self.send_header("Content-Length", file_size)
		self.end_headers()

		print("file size is ", file_size)
		buf_size = BUFFER_SIZE
		remaining_length = file_size

		if file_size < buf_size:
			buf_size = file_size

		total_written = 0

		with open(filename, "rb") as f:
			bytes = f.read(buf_size)
			remaining_length = remaining_length - buf_size
			# print("Remaining size {}".format(remaining_length))
			# # sys.stdout.write("\033[F")
			if remaining_length == 0:
				self.wfile.write(bytes)
				return

			while bytes != "":
				self.wfile.write(bytes)
				total_written = total_written + len(bytes)
				print(total_written, " of bytes written.")

				if remaining_length == 0:
					break
				if remaining_length < buf_size:
					buf_size = remaining_length
				bytes = f.read(buf_size)
				remaining_length = remaining_length - buf_size
				

httpd = socketserver.TCPServer(("", PORT), FileServerRequestHandler)

print("serving at port", PORT)
httpd.serve_forever()