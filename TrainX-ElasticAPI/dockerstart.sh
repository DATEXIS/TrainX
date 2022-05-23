if [ -f iHaveSuccessfullyFinished${INDEX,,}.txt ]; then
  echo "Already loaded data successfully into index ${INDEX,,} to elasticsearch"
else
  cd api/elastictrainer/src
  if [ -f ${IMPORT_FILE} ]; then
    echo "${IMPORT_FILE} already unzipped"
  else
    IMPORT=$IMPORT_FILE
    FILE=${IMPORT/json/zip}
    unzip $FILE
    echo "Unpacking was successful."
    # Some kind of folder that gets created by unziping on macOS
    rm -rf __MACOSX
  fi
fi



echo "Waiting for database"
while ! nc -z elasticsearch 9200 2>/dev/null
do
  sleep 5;
  echo "."
done
echo "Database is up."

python3 /app/api/app.py
