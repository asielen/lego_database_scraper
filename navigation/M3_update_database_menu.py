# Internal
import system as syt

if __name__ == "__main__": syt.setup_logger()

# Price capture
from data.update_ternary import daily_data
from data import update_secondary as secondary


def database_update_menu():
    def daily_update():
        daily_data.price_capture_menu()

    def data_update():
        secondary.updates_sets_database_from_api()

    def inventory_update():
        secondary.updates_inv_database_from_api()

    def base_update():
        pass

    options = (
        ("Daily Update", daily_update),
        ("Set Data Update", data_update),
        ("Inventory Update", inventory_update),
        ("Base Update #", base_update)
    )
    syt.Menu(name="- Update Database -", choices=options).run()


if __name__ == "__main__":
    database_update_menu()