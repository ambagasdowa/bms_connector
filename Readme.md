---
title: "Status of the base Project for an api creation"
author: "baizabal.jesus@gmail.com"
extensions:
  - image_ueberzug
  - qrcode
  - render
styles:
  style: solarized-dark
  table:
    column_spacing: 15
  margin:
    top: 3
    bottom: 0
  padding:
    top: 3
    bottom: 3
---

# First Step

> base on the project <https://inmagik.com/en/blog/fastapi-basic-crud>
> and in the manuals for fastapi <https://fastapi.tiangolo.com/tutorial/sql-databases/>

- Install the dependencies
-

```bash
  python3 -m pip install uvicorn fastapi sqlalchemy pandas pymysql jinja2 python-multipart
```

- build the skelton app

- check the db

- publish

## Requests

```bash
https --verbose --verify=no baizabal.xyz:8000/srcpositions/4/6 \
            [0]["bms_books_id"]=4 \
            [0]["bms_bookpages_id"]=6 \
            [0]["color"]="cyan" \
            [0]["lineWidth"]=2 \
            [0]["source_width"]="1440" \
            [0]["source_height"]="890" \
            [0]["inputType"]="radio" \
            [0]["page"]=3 \
            [0]["x1"]="120" \
            [0]["y1"]="80" \
            [0]["x2"]="230" \
            [0]["y2"]="40" \
            [1]["bms_books_id"]=4 \
            [1]["bms_bookpages_id"]=6 \
            [1]["color"]="cyan" \
            [1]["lineWidth"]=2 \
            [1]["source_width"]="1440" \
            [1]["source_height"]="890" \
            [1]["inputType"]="text" \
            [1]["page"]=3 \
            [1]["x1"]="120" \
            [1]["y1"]="80" \
            [1]["x2"]="230" \
            [1]["y2"]="40"
```

- query to

```bash
https --verify=no baizabal.xyz:8000/srcpos/4/6 | jq | cat -l json
```

- other

```bash
https --verify=no baizabal.xyz:8000/items/4/1702 | jq | cat -l json
```

- test

```bash
https --verify=no baizabal.xyz:8000/srcpositions/1 | jq | cat -l json
```

- files

```bash
https --verify=no -f POST baizabal.xyz:8000/upload \
      book_name="Matematicas Bachillerato de 2nd grado 002,Guia de estudio para ingreso a la unam 002,Guia de Estudio para la UV 002, Libro Fisica 2nd semestre de Bachillerato 002" \
      files@~/Development/book_matematicas_002_bachillerato.zip \
      files@~/Development/guia_unam_215_universidad.zip \
      files@~/Development/guia_uv_002_demo.zip \
      files@~/Development/book_fisica_002_bachillerato.zip \
      token:'ioafsyudfoansdfnjnkajsnd017341782yhodklasdhjnallaisdfu=='
```

# TODO

- Api [Server](https://github.com/ambagasdowa/bms_connector.git) Development

  - [~] Reorder Items method for release mysql work
  - [~] Add singleton to [items module] logic for serve [one] OR [many-to-many] responses
  - [ ] Add server or local parameter to img-paths[bookpages:{}] responses

> - [x] : done
> - [~] : Working on
> - [ ] : TODO

# Database source

> [database](https://gitlab.com/ambagasdowa/sql/-/raw/master/mariadb/panamericano/bms.sql)
