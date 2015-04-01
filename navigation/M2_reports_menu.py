# Internal
import system as syt

if __name__ == "__main__": syt.setup_logger()


def make_report_menu():
    def set_report():
        set_report_menu()

    def multi_report():
        multi_set_report_menu()

    options = (
        ("Build Historic Set Report", set_report),
        ("Build Multi-Set Report", multi_report)
    )
    syt.Menu(name="- Make Reports -", choices=options).run()


def set_report_menu():
    def new_report():
        pass

    def edit_report():
        pass

    def run_report():
        pass

    def save_report():
        pass

    def load_report():
        pass

    options = (
        ("Build New Report", new_report),
        ("Edit Report Parameters", edit_report),
        ("Run Report", run_report),
        ("Save Report", save_report),
        ("Load Report", load_report)
    )
    syt.Menu(name="- Make Set Report -", choices=options).run()


def multi_set_report_menu():
    def new_report():
        pass

    def edit_report():
        pass

    def run_report():
        pass

    def save_report():
        pass

    def load_report():
        pass

    options = (
        ("Build New Report", new_report),
        ("Edit Report Parameters", edit_report),
        ("Run Report", run_report),
        ("Save Report", save_report),
        ("Load Report", load_report)
    )
    syt.Menu(name="- Make Multi Set Report -", choices=options).run()


if __name__ == "__main__":
    make_report_menu()