import pygame


class ActionMenu:
    # import all the constants here so they can be edited in one place (panes.py)
    def __init__(self, WIN, engine, PANE_WIDTH, PANE_SPACING, ACTION_MENU_HEIGHT, WIN_BORDER_WIDTH, PANE_BORDER_WIDTH, PANE_COLOR, BORDER_COLOR):
        self.cursor_location = 0
        self.WIN = WIN
        self.engine = engine
        self.MENU_WIDTH = PANE_WIDTH - PANE_SPACING
        self.MENU_HEIGHT = ACTION_MENU_HEIGHT  - (WIN_BORDER_WIDTH//2) - (PANE_BORDER_WIDTH // 2) #- (PANE_SPACING * 2)
        self.RIGHTSIDE = self.WIN.get_width() - WIN_BORDER_WIDTH - (PANE_BORDER_WIDTH//2) - PANE_SPACING
        self.BOTTOMSIDE = self.WIN.get_height() - WIN_BORDER_WIDTH - (PANE_BORDER_WIDTH//2) - PANE_SPACING
        self.MENU_CENTER = self.MENU_WIDTH // 2
        self.MENU_SPACING = 10
        self.FONT_SIZE = 27
        self.FONT_COLOR = (30,30,30)
        self.PANE_COLOR = PANE_COLOR
        self.BORDER_COLOR = BORDER_COLOR
        self.PANE_BORDER_WIDTH = PANE_BORDER_WIDTH
        self.FONT_HIGHLIGHT_COLOR = 'Brown'
        self.FONT_DISABLED_COLOR = (150,150,150)

        self.option_menu_on = False
        self.font_dict = {}
        self.font_rect_dict = {}
        self.accessible_items = []  # To grab from inventory
        self.inventory_active = False  # This and next line for inventory use
        self.character_index = None
        self.all_characters_out = True  # Check if call characters are dead or full health
        self.no_items_usable = True  # If all characters are dead or full health

        self.main_menu =    {
            0:['Inspect', True],
            1:['Move North', True],
            2:['Move South', True],
            3:['Move West', True],
            4:['Move East', True],
            5:['Use Item', True],
            6:['Heal Magic', True],
            7:['Options', True]
        }
        self.choice_menu = {
            0:['Yes', True],
            1:['No', True]
        }

        self.character_menu = {
            0:['Knight', True],
            1:['Archer', True],
            2:['Thief', True],
            3:['White Mage', True],
            4:['Black Mage', True]
        }
        self.character_menu_return = {
            0:['Knight', True],
            1:['Archer', True],
            2:['Thief', True],
            3:['White Mage', True],
            4:['Black Mage', True],
            5:['Return', True]
        }

        self.item_menu = {
            0:['Potion', True],
            1:['Ether', True],
            2:['Elixir', True],
            3:['Return', True]
        }

        self.game_over_menu = {
           0:['Restart', True],
           1:['Quit', True]
        }

        self.option_menu = {
            0:['Return', True],
            1:['Restart', True],
            2:['Save', False],
            3:['Difficulty', False],
            4:['Screen', False],  # To make fullscreen and back
            5:['Zoom', True],
            6:['Shortcuts', False],
            7:['Credits', False],
            8:['Quit', True]
        }

        self.left_right = {
            0:['Left', True],
            1:['Right', True]
        }

        self.menus_dict = {
            'main': self.main_menu,
            'choice': self.choice_menu,
            'characters': self.character_menu,
            'items': self.item_menu,
            'left_right': self.left_right
        }


        self.current_menu = self.main_menu

        # Menu and rect
        self.menu_sur = pygame.Surface((self.MENU_WIDTH, self.MENU_HEIGHT))
        self.menu_rect = self.menu_sur.get_rect(bottomright=(self.RIGHTSIDE, self.BOTTOMSIDE))

        # Text for menu items
        self.menu_font = pygame.font.SysFont('bahnschrift', self.FONT_SIZE, 0)
        self.bold_font = pygame.font.SysFont('bahnschrift', self.FONT_SIZE - 1, 1)

        # This is just to get the height of the font to use in render_fonts()
        self.test_font_height = self.menu_font.render("Move", 1, self.FONT_COLOR)
        self.test_font_height_rect = self.test_font_height.get_rect(midtop=(self.MENU_CENTER, self.MENU_SPACING))

        # Cursor dot rect:
        self.cursor_dot_rect = pygame.Rect(self.menu_rect.x, self.menu_rect.y + self.MENU_SPACING, 50, 50)

        # LATER: Try for IndexError on "if self.engine.current_room.room_choices[0]"
    def render_fonts(self, menu):

        # Couldn't figure out where to change this, so just put it here. Will constantly change it while in characters, but doesn't work in keyboard input under 'characters'
        # if self.engine.menu_state == 'characters':
        #     for idx in range(len(self.character_menu)):
        #         self.character_menu[idx][1] = True



        for num in range(len(menu)):
            # Renders the font and puts them in dictionary:
            if menu[num][1]: # if enabled
                if self.cursor_location == num: # if it's current selection, highlight
                    self.font_dict[menu[num][0]] = self.bold_font.render(menu[num][0], 1, self.FONT_HIGHLIGHT_COLOR)
                else:
                    self.font_dict[menu[num][0]] = self.menu_font.render(menu[num][0], 1, self.FONT_COLOR)
            else: # if disabled
                self.font_dict[menu[num][0]] = self.menu_font.render(menu[num][0], 1, self.FONT_DISABLED_COLOR)

            # Rects for the fonts, puts them in dictionary
            self.font_rect_dict[menu[num][0]] = self.font_dict[menu[num][0]].get_rect(midtop=(self.MENU_CENTER, self.MENU_SPACING + ((self.MENU_SPACING + self.test_font_height_rect.height) * num)))
            # blits fonts from dictionary:
            self.menu_sur.blit(self.font_dict[menu[num][0]], self.font_rect_dict[menu[num][0]])


            # Reset dictionaries for other menus, probably don't need:
            # self.font_dict = {}
            # self.font_rect_dict = {}


    def set_character_states_dead_or_full(self, set_all=False):
        # Unused
        # For character menu, grey out full/empty health
        self.no_items_usable = True
        for idx in range(len(self.character_menu)):
            name = self.character_menu[idx][0]
            for char in self.engine.character_list:
                if name == char.name:
                    if not char.dead and char.health != char.health_max:
                        self.character_menu[idx][1] = True
                        self.no_items_usable = False
                    else:
                        self.character_menu[idx][1] = False
                        if set_all:
                            self.character_menu[idx][1] = True


    def move_up(self):
        # current_menu = self.menus_dict[self.engine.menu_state]
        self.cursor_location -= 1
        if self.cursor_location < 0:
            self.cursor_location = len(self.current_menu) - 1
        self.check_if_disabled(-1, self.current_menu)


    def move_down(self):
        # current_menu = self.menus_dict[self.engine.menu_state]
        self.cursor_location += 1
        if self.cursor_location >= len(self.current_menu):
            self.cursor_location = 0
        self.check_if_disabled(1, self.current_menu)


    def subtract_current_item(self):
        for item in self.engine.item_inventory:
            if item[0] == self.engine.current_item:
                item[1] -= 1


    def use_inventory(self):
        for item in self.engine.item_inventory:
            if item[0] == self.accessible_items[self.character_index]:
                if not item[1]:
                    self.engine.menu_state = 'main'
                    self.inventory_active = False
                    self.engine.error_sound.play()
                    self.engine.error_sound.set_volume(.3)
                    self.cursor_location = 0
                    return
        # Should probably move this and subtract_current_item into engine...
        if self.engine.character_selection.dead and self.accessible_items[self.character_index] != 'Elixir':
            self.engine.error_sound.play()
            self.engine.error_sound.set_volume(.3)
            self.engine.update_console([f"You can't do that."])

        else:
            if self.accessible_items[self.character_index] == 'Potion':
                if self.engine.character_selection.health != self.engine.character_selection.health_max:
                    # Sound effect:
                    self.engine.healing_sound.play()
                    self.engine.healing_sound.set_volume(.3)

                    self.engine.current_item = 'Potion'
                    self.subtract_current_item()
                    self.engine.character_selection.health += 100
                    if self.engine.character_selection.health > self.engine.character_selection.health_max:
                        self.engine.character_selection.health = self.engine.character_selection.health_max
                    self.engine.update_console([f"{self.engine.character_selection.name} gained 100HP."])
                else:
                    self.engine.error_sound.play()
                    self.engine.error_sound.set_volume(.3)
                    self.engine.update_console([f"You can't do that."])

            if self.accessible_items[self.character_index] == 'Ether':
                if self.engine.character_selection.mp != self.engine.character_selection.mp_max:
                    # Sound effect:
                    self.engine.healing_sound.play()
                    self.engine.healing_sound.set_volume(.3)

                    self.engine.current_item = 'Ether'
                    self.subtract_current_item()
                    self.engine.character_selection.mp += 100
                    if self.engine.character_selection.mp > self.engine.character_selection.mp_max:
                        self.engine.character_selection.mp = self.engine.character_selection.mp_max
                    self.engine.update_console([f"{self.engine.character_selection.name} gained 100MP."])

                else:
                    self.engine.error_sound.play()
                    self.engine.error_sound.set_volume(.3)
                    self.engine.update_console([f"You can't do that."])

            if self.accessible_items[self.character_index] == 'Elixir':
                if self.engine.character_selection.health == self.engine.character_selection.health_max and self.engine.character_selection.mp == self.engine.character_selection.mp_max:
                    self.engine.error_sound.play()
                    self.engine.error_sound.set_volume(.3)
                    self.engine.update_console([f"You can't do that."])
                else:
                    # Sound effect:
                    self.engine.healing_sound.play()
                    self.engine.healing_sound.set_volume(.3)

                    self.engine.current_item = 'Elixir'
                    self.subtract_current_item()
                    self.engine.character_selection.mp = self.engine.character_selection.mp_max
                    self.engine.character_selection.health = self.engine.character_selection.health_max
                    self.engine.character_selection.dead = False
                    self.engine.update_console([f"{self.engine.character_selection.name} gained full HP/MP"])


    def check_if_disabled(self, direction: '-1 or 1 (up or down)', current_menu) -> 'Moves past disabled choices':
        # Loops number of times equal to menu length in case everything is disabled
        for num in range(len(current_menu)):
            # If not active:
            if not current_menu[self.cursor_location][1]:
                self.cursor_location += direction
                # To circle around from top or bottom
                if self.cursor_location >= len(current_menu):
                    self.cursor_location = 0
                elif self.cursor_location < 0:
                    self.cursor_location = len(current_menu) - 1


    def update_item_menu(self):
        # Update the item count for inventory game use
        temp_item_menu = {}
        x = 0
        if self.engine.menu_state == 'items':
            idx = 0
            self.accessible_items = []
            for item in self.engine.item_inventory:
                if item[0] == 'Potion':
                    x += 1
                    if item[1]: # If there is one or more of item
                        temp_item_menu[idx] = [f'Potion: {item[1]}', True]
                        self.accessible_items.append('Potion')
                        idx += 1
                if item[0] == 'Ether':
                    if item[1]:
                        temp_item_menu[idx] = [f'Ether: {item[1]}', True]
                        self.accessible_items.append('Ether')
                        idx += 1
                if item[0] == 'Elixir':
                    if item[1]:
                        temp_item_menu[idx] = [f'Elixir: {item[1]}', True]
                        self.accessible_items.append('Elixir')
                        idx += 1

            temp_item_menu[idx] = ["Return", True]
            self.accessible_items.append('Return')
            self.item_menu = temp_item_menu


    def display_menu(self):
        # Check if Healing menu neads to be disabled:
        if self.engine.character_list[3].dead or self.engine.character_list[3].mp < 20: # Disable Healing
            self.main_menu[6][1] = False
        else:
            self.main_menu[6][1] = True

        # Display menu:
        self.WIN.blit(self.menu_sur, self.menu_rect)
        self.menu_sur.fill(self.PANE_COLOR)
        pygame.draw.rect(self.WIN, self.BORDER_COLOR, self.menu_rect, self.PANE_BORDER_WIDTH)

        # Choose menu state (from engine.py)
        if self.engine.menu_state == 'main':
            self.current_menu = self.main_menu
        elif self.engine.menu_state == 'choice':
            self.current_menu = self.choice_menu
        elif self.engine.menu_state == 'characters':
            self.current_menu = self.character_menu
        elif self.engine.menu_state == 'characters_return':
            self.current_menu = self.character_menu_return
        elif self.engine.menu_state == 'items':
            # self.update_item_menu() # Better in keyboard_input to call only once----??
            self.current_menu = self.item_menu
        elif self.engine.menu_state == 'left_right':
            self.current_menu = self.left_right

        if self.engine.game_over:
            self.current_menu = self.game_over_menu
        elif self.option_menu_on:
            self.current_menu = self.option_menu

        self.render_fonts(self.current_menu)

        # Cursor dot
        self.cursor_dot_rect.centery = self.menu_rect.y + self.test_font_height_rect.center[1] + ((self.MENU_SPACING + self.test_font_height_rect.height) * self.cursor_location)
        pygame.draw.circle(self.WIN, 'Brown', self.cursor_dot_rect.center, 10)


    def disable_menus(self):
        if self.engine.current_room.room_choices[0]: # North
            self.main_menu[1][1] = True
        else:
            self.main_menu[1][1] = False

        if self.engine.current_room.room_choices[1]: # South
            self.main_menu[2][1] = True
        else:
            self.main_menu[2][1] = False

        if self.engine.current_room.room_choices[2]: # West
            self.main_menu[3][1] = True
        else:
            self.main_menu[3][1] = False

        if self.engine.current_room.room_choices[3]: # East
            self.main_menu[4][1] = True
        else:
            self.main_menu[4][1] = False
