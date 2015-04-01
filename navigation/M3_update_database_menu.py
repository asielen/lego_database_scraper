# Internal
import system as syt

if __name__ == "__main__": syt.setup_logger()


def database_update_menu():
    def daily_update():
        pass

    def data_update():
        pass

    def inventory_update():
        pass

    def base_update():
        pass

    options = (
        ("Daily Update", daily_update),
        ("Set Data Update", data_update),
        ("Inventory Update", inventory_update),
        ("Base Update", base_update)
    )
    syt.Menu(name="- Update Database -", choices=options).run()


if __name__ == "__main__":
    database_update_menu()