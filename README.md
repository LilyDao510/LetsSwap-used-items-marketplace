# start local postgres
```
#mac
pg_ctl -D /usr/local/var/postgres start
#linux
pg_ctl start
```
# bootstrap database
```
# Run once to initialize tables
psql -f sql_bootstrap.sql
```

# secret file
```
pass secret under /venv/.env
```


# item-exchange run
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
flask run
```

# known issues


