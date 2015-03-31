# Update a single set using the set num
# todo
#
#
#



from data.data_classes import SetInfo
from data import update_secondary as secondary
import system as syt


def main():
    options = (
        ("Update Basestats", update_baseStats), # Todo: Check to see if this works
        ("Update Prices", update_prices),
        ("Manual Update", manual_Update)
    )

    syt.Menu("– Update Set –",choices=options, drop_down=True).run()


def update_baseStats():
    print("Update Base Stats")
    set_id = SetInfo.input_set_num()
    secondary.add_set_to_database(set_id)


def update_prices():
    print("Update Prices")


def manual_Update():
    print("Manual Update")


if __name__ == "__main__":
    main()