# Internal
import system as syt
from database import health

if __name__ == "__main__": syt.setup_logger()


def system_menu():
    def backup_database():
        health.backup_database()

    def restore_database():
        health.restore_database()

    def get_func_counts():
        print(syt.get_counts())

    def database_stats():
        pass

    def database_health():
        pass

    options = (
        ("Backup Database", backup_database),
        #("Restore Database", restore_database),
        ("Get Function Counts", get_func_counts),
        ("Check Database Stats #", database_stats),
        ("Check Database Health #", database_health)
    )
    syt.Menu(name="- System -", choices=options).run()


if __name__ == "__main__":
    system_menu()
