# === === === === === === === ===  Config Section  === === === === === === === === #

configuration = {
    "db_connection": {
        "server": "127.0.0.1",
        "driver": "pymsql+mysql",
        "database": "db_ediq2021",
        "user": "ambagasdowa",
        "password": "pekas",
        "proc_exec": "call",  # call[mariadb]|exec[mssql]...
        "proc_0": "bms_proc_build_cache_inp_usr",
    },
    "download_config": {
        # Optional as global or by user authorization (Recomended)
        "token": "some_random_char36",
        "download_path": "/tmp/",
        "dir_path": "book/",
        "ext_basename": "https://baizabal.xyz/assets/Panamericano/files/",
        "basename": "/home/ambagasdowa/files",
        "pathname": "/source",
    },
}
