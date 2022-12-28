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
        "token": "some_random_char36",
        "http_path": "ws_url:port/?/file",  # if needed <?> is replaced by <token>
        "download_path": "/tmp/",
        "dir_path": "book/",
        "filename": "cfdi_?.zip",  # if needed <?> is replaced by a random number
        "basename": "src/files",
        "pathname": "/source",
    },
    # This params are specified by the web service can be changed in https execution process
    "service_params": {  # Partialy implemented ** Obligatorios e implementados
        "representacion": "XML",  # ** XML,PDF,ACUSE
        "pageSize": "100",  # ** [0-100] default 50
        # same as params, default is ? that means:yesterday
        "fecha": '2022-12-06:2022-12-12',
        #        "fecha": '2022-12-06',
        "fechaInicial": '?',  # yyyy-mm-dd
        "fechaFinal": '?',  # yyyy-mm-dd
        "serie": '',
        "folioEspecifico": '',  # int
        "folioInicial": '',  # int
        "folioFinal": '',  # int
        "uuid": '',  # 2d340db1-9c08-4c97-9ca8-676dc648094e
    }
}
