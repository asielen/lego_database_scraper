__author__ = 'andrew.sielen'

__version__ = 310
# Basic menu system v3.1

class Menu(object):
    """
        Basic menu in the format:
        1: Item
        2: Item
        3: Item
        Q: Back/Quit

        Need to pass a list of option strings with functions attached
        drop_down=True means the menu wont open itself again when closed

        Example:
        options = [("Create Email", self.menu_create_email),
                   ("Load Template", self.menu_load_email),
                   ("Edit Email", self.menu_edit_email),
                   ("Save Email", self.menu_save_template)]
        Menu("- Main Menu -", choices=options, quit=True)
    """

    STANDARD = 0
    LOAD = 1
    RETURN = 2
    MULTICHOICE = 3
    KILL = 0

    def __init__(self, name=None, choices=None, function=None, drop_down=False, type=STANDARD, quit_tag=None):
        """

        :param name: Menu intro text. Can also be a function call as long as it returns a string
        :param choices:
            Can be in two formats:
                1) Names with Functions
                    [("Choice1",Function1),("Choice2",Function2)]
                2) Names
                    ["Name1","Name2","Name3"]
        :param function: if type == LOAD, you need a function to call on the choice
        :param drop_down:
            False = Keep loading this menu until option back/quit_tag is chosen
            True = load the menu once and then quit_tag
        :param type:
            standard = choice format 1
            load = choice format 2
            return = choice format 2 - returns the choice instead of calling a function on that choice
        :param quit_tag:
            True = have the last option be 'quit_tag'
            False = have the last option be 'back'
        :return:
        """

        self.name = name
        self.type = type
        if function is None:
            self.function = self.return_string
        else:
            self.function = function

        # Make sure that the choices is in the right format for the type
        if type == self.STANDARD:
            # Should be in the format listed above, so each element should be a tuple of two elements
            assert len(choices[0]) == 2
        elif type == self.LOAD:
            # If the type isn't standard, we need a function to run
            assert function != None

        self.drop_down = drop_down

        self.choices = {}

        for idx, opt in enumerate(choices):
            if self.type != self.STANDARD:
                opt = (opt, self.function)  # convert the opt to a tuple if it isn't one
            self.choices[self.idx_to_sel(idx)] = opt

        # Create the choice list. - Could have just used a sorted dict.
        self.options_list = list(self.choices.keys())
        self.options_list.sort(key = lambda s: int(s))

        # For any menu type, this is just a text string that triggers a return instead of an action
        if quit_tag == True:
            self.choices["0"] = ("Quit", self.back)
        elif quit_tag is None:
            self.choices["0"] = ("Back", self.back)
        else:
            self.choices["0"] = (quit_tag, self.back)
        self.options_list.append("0")

        self.result = ""

    def return_string(self, str):
        """
        For the type: return. Returns the string instead of working it with the function
        :return:
        """
        return str

    def back(self):
        return

    def idx_to_sel(self, idx):
        """
            Convert the index number to a string that can be used in the selection process
                Adds one to the string so it starts with 0. 0 is reserved for quit/back
        """
        return str(idx + 1)

    def _options_menu(self):
        menu_intro = ""

        if callable(self.name):
            # If a function was entered for the header, call it
            menu_intro = self.name()
        else:
            # else use the text string
            menu_intro = self.name

        print("\n{}".format(menu_intro))

        for entry in self.options_list:
            print("  " + entry + ":", self.choices[entry][0])

        selection = input("Which selection? ")

        if selection in self.choices:
            if selection == "0":
                return self.KILL

            action = self.choices[selection][1]
            if self.type == self.STANDARD:
                return action()
            else:
                return action(self.choices[selection][0])

        else:
            print("Invalid Input. Please try again")


    def _choose_loop(self):
        result = None
        while True:
            result = self._options_menu()
            if result is self.KILL:
                break
            if self.drop_down is True:
                break
        return result

    def run(self):
        self.result = self._choose_loop()
        return self.result


class Load_Menu(Menu):
    """
    Alias for Load Menus
    """

    def __init__(self, name=None, choices=None, function=None):
        super(Load_Menu, self).__init__(name=name, choices=choices, function=function, drop_down=True, type=Menu.LOAD).run()


def MultiChoiceMenu(choice_list=None):
    """
    Class for making multi-select menus
    """

    selected_choices = []
    current_choice = None
    while current_choice != Menu.KILL:
        options = ["Add", ] + selected_choices
        current_choice = Menu("- Current List - (select add to add, others to remove)", choices=options,
                              type=Menu.RETURN, drop_down=True, quit_tag="Done").run()
        print(current_choice)
        if current_choice == 'Add':
            options = list(set(choice_list) - set(selected_choices))
            current_selection = Menu("- Add which selection? -", choices=options, type=Menu.RETURN, drop_down=True,
                                     quit_tag="Done").run()
            print(current_selection)
            selected_choices.append(current_selection)
        elif current_choice in options:
            selected_choices.remove(current_choice)
    return selected_choices

