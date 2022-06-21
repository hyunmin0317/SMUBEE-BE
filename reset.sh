sudo rm db.sqlite3

for APP in announcements courses notifications planners professors users
do
    sudo rm -rf $APP/migrations/
    mkdir $APP/migrations/
    touch ./$APP/migrations/__init__.py
done
