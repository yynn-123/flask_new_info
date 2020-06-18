from flask import session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from info import creat_app, db

app = creat_app('develop')
manager = Manager(app)
# 数据库迁移flaks_script

Migrate(app, db)
manager.add_command('db', MigrateCommand)




if __name__ == '__main__':
    manager.run()
