from datetime import time

config = {
	"free_time_start": time(17, 0, 0),
	"free_time_end": time(23, 59, 59),
	"free_time_buffer": time(0, 5, 0),

	"download_folder": "/path/to/downloads",
	"db_folder": "/path/to/db",

	"proxy": {
		"host": "proxy.test.com",
		"port": 8080,
		"users": [
			{"name": "user", "passwd": "password", "quota": 4096}
		]
	},

	"origin": {
		"boxftp": {
			"protocol": "ftp",
			"host": "ftp.example.com",
			"port": 21,
			"user": "user",
			"passwd": "password"
		}
	}
}