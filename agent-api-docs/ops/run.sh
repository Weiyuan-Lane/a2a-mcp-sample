#!/bin/sh

NGINX_DIR="/usr/share/nginx/html"
BASE_DOCS_DIR_URL="/docs"

render_docs()
{
  apis_str="var apis=["

  for d in $BASE_DOCS_DIR_URL/* ; do
    file=`basename "$d"`
    filename="${file%.*}"
    apis_str="$apis_str{url:\"$BASE_DOCS_DIR_URL/$file\", name:\"$filename\"},"
    cp "$d" "$NGINX_DIR$BASE_DOCS_DIR_URL"
  done

  apis_str="$apis_str];"

  sed -e "s|APIS_STRING_TEMP|$apis_str|g" /assets/index.html > $NGINX_DIR/index.html
  find $NGINX_DIR -type f -regex ".*\.\(html\|js\|css\)" -exec sh -c "gzip < {} > {}.gz" \;
}

mkdir -p "$NGINX_DIR$BASE_DOCS_DIR_URL"
render_docs

nginx

while true; do
  inotifywait -e modify,create,delete -r $BASE_DOCS_DIR_URL |
    render_docs
done
