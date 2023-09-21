# start local postgres

pg_ctl -D /usr/local/var/postgres start
# bootstrap database
psql -f sql_bootstrap.sql

# secret file
pass secret under /venv/.env


# item-exchange run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run

