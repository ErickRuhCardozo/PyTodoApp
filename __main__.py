from database.db import Db
from views.mainwindow import MainWindow


def main():
    if not Db.exists():
        Db.create()
    
    MainWindow()


if __name__ == '__main__':
    main()
