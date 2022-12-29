# === === === === === === === ===  Config Section  === === === === === === === === #

configuration = {
    "db_connection": {
        "server": "127.0.0.1",
        "driver": "pymsql+mysql",
        "database": "db_ediq2021",
        "user": "ambagasdowa",
        "password": "pekas",
    },
    "download_config": {
        # Optional as global or by user authorization (Recomended)
        "token": "some_random_char36",
        #        "http_path": "ws_url:port/?/file",  # if needed <?> is replaced by <token>
        "download_path": "/tmp/",
        "dir_path": "book/",
        #        "filename": "cfdi_?.zip",  # if needed <?> is replaced by a random number
        #        "basename": "/src/tmp/files",
        "basename": "/home/ambagasdowa/files",
        "pathname": "/source",
    },
}
