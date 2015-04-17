# System
import system as syt

if __name__ == "__main__": syt.setup_logger()

# Menu
from data.data_classes import SetInfo
from data import lego_urls


def quick_data_menu():
    eval_set = None

    def load_set():
        """ Prompts for a _set and loads it as the eval _set """
        nonlocal eval_set
        set_num = SetInfo.input_set_num()
        eval_set = SetInfo(set_num)

    def set_info():
        """ Prompts for a _set number and creates a dump of its basic data """
        nonlocal eval_set
        if eval_set is None: load_set()
        print(eval_set.debug_dump_all())

    def set_report():
        """ Prompts for a _set number and creates a csv dump of that _set """
        nonlocal eval_set
        if eval_set is None: load_set()
        eval_set.make_set_report()

    def set_links():
        """ Prompts for a _set number and returns a list of urls for easy access """
        nonlocal eval_set
        if eval_set is None: load_set()
        lego_urls.get_links(eval_set.set_num)

    def menu_title():
        nonlocal eval_set
        title = "- Quick Data -"
        if eval_set is not None:
            title += "\n> {} | {}".format(eval_set.set_num, eval_set.name)
        return title

    options = (
        ("Load Set", load_set),
        ("Get Set Info", set_info),
        ("Create Set Report", set_report),
        ("Get Set Links", set_links)
    )
    syt.Menu(name=menu_title, choices=options).run()


if __name__ == "__main__":
    quick_data_menu()