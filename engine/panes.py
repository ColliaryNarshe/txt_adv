import pygame
from engine.action_menu import ActionMenu
from engine.map import Map

PANE_WIDTH = 200
CONSOLE_HEIGHT = 350
ACTION_MENU_HEIGHT = 350
PANE_SPACING = 10 # Spacing around panes

BORDER_COLOR = 'Grey50' #'cadetblue3' # 'dodgerblue4'
PANE_COLOR = 'burlywood3'

WIN_BORDER_WIDTH = 0 # Should be half of what is defined in main.py, other half off screen
PANE_BORDER_WIDTH = 10



class ItemMenu:
    # Could make a separate function to "update fonts" and render only when you
    # call it rather than every frame
    def __init__(self, WIN, engine):
        self.WIN = WIN
        self.engine = engine
        self.items = self.engine.item_inventory
        self.MENU_HEIGHT = self.WIN.get_height() - ACTION_MENU_HEIGHT - WIN_BORDER_WIDTH - (PANE_BORDER_WIDTH * 2) - (PANE_SPACING * 3)
        self.RIGHTSIDE = self.WIN.get_width() - WIN_BORDER_WIDTH - (PANE_BORDER_WIDTH//2) - PANE_SPACING
        self.TOPSIDE = WIN_BORDER_WIDTH + (PANE_BORDER_WIDTH//2) + PANE_SPACING
        self.MENU_INDENT = 15
        self.MENU_SPACING = 32
        self.FONT_COLOR = 'Black'

        # Text surface/rect:
        self.txt_sur = pygame.Surface((PANE_WIDTH - PANE_SPACING, self.MENU_HEIGHT))
        self.menu_rect = self.txt_sur.get_rect(topright=(self.RIGHTSIDE, self.TOPSIDE))

        # Text for menu items
        self.menu_font = pygame.font.SysFont('georgia', 21, 0)
        self.menu_font_bold = pygame.font.SysFont('georgia', 26, 1)


    def display_txt(self):
        # Items title:
        self.title_font = self.menu_font_bold.render("Items:", 1, self.FONT_COLOR)
        self.title_rect = self.title_font.get_rect(topleft = (self.MENU_INDENT, self.MENU_INDENT - 8))
        self.txt_sur.blit(self.title_font, self.title_rect)
        count = 0
        for num in range(len(self.items)):
            if self.items[num][1] > 0:
                rendered_font = self.menu_font.render(self.items[num][0] +f": {self.items[num][1]}" , 1, self.FONT_COLOR)
                font_rect = rendered_font.get_rect(topleft=(self.MENU_INDENT, 44 + (self.MENU_SPACING * count)))
                self.txt_sur.blit(rendered_font, font_rect)
                count += 1


    def display_menu(self):
        self.WIN.blit(self.txt_sur, self.menu_rect)
        self.txt_sur.fill(PANE_COLOR)
        pygame.draw.rect(self.WIN, BORDER_COLOR, self.menu_rect, PANE_BORDER_WIDTH)

        self.display_txt()


class CharacterPane:
    def __init__(self, WIN, engine):
        self.WIN = WIN
        self.engine = engine
        # self.BACKGROUND_COLOR = 'grey'
        self.PANE_WIDTH = PANE_WIDTH - PANE_SPACING
        self.PANE_HEIGHT = self.WIN.get_height() - (WIN_BORDER_WIDTH * 2) - (PANE_BORDER_WIDTH) - (PANE_SPACING * 2)
        self.LEFTSIDE = WIN_BORDER_WIDTH + (PANE_BORDER_WIDTH//2) + PANE_SPACING
        self.TOPSIDE = WIN_BORDER_WIDTH + (PANE_BORDER_WIDTH//2) + PANE_SPACING
        self.NAME_FONT_SIZE = 23
        self.HP_FONT_SIZE = 21
        self.FONT_COLOR = (30,30,30)
        self.FONT_COLOR_HP = 'Brown'
        self.NAMES_SPACING = 150
        self.UNDER_NAME_SPACE = 44 # Between name and HP
        self.HP_BAR_LENGTH = 150
        self.HP_BAR_HEIGHT = 20
        # Font lists:
        self.name_font_list = []
        self.name_font_rect_list = []
        self.hp_font_list = []
        self.hp_font_rect_list = []

        # Surface/Rect
        self.character_sur = pygame.Surface((self.PANE_WIDTH, self.PANE_HEIGHT))
        self.character_rect = self.character_sur.get_rect(topleft=(self.LEFTSIDE, self.TOPSIDE))

        # Fonts:
        self.char_name_font = pygame.font.SysFont('bahnschrift', self.NAME_FONT_SIZE, 1)
        self.HP_font = pygame.font.SysFont("ebrima", self.HP_FONT_SIZE, 0) # 'ebrima'

        # Use list of names from characters.py to render fonts/rects and append to lists
        for idx, char in enumerate(self.engine.character_list):
            # CHARACTER FONTS:
            font_txt = self.char_name_font.render(char.name, 1, self.FONT_COLOR)
            font_txt_rect = font_txt.get_rect(topleft = (20, 15 + (self.NAMES_SPACING * idx)))
            self.name_font_list.append(font_txt)
            self.name_font_rect_list.append(font_txt_rect)



    def display_menu(self):
        self.WIN.blit(self.character_sur, self.character_rect)
        self.character_sur.fill(PANE_COLOR)
        pygame.draw.rect(self.WIN, BORDER_COLOR, self.character_rect, PANE_BORDER_WIDTH)

        # blit character names
        for idx in range(len(self.name_font_list)):
            self.character_sur.blit(self.name_font_list[idx], self.name_font_rect_list[idx])

        # Slash through name if dead:
        for idx,char in enumerate(self.engine.character_list):
            if char.dead:
                pygame.draw.line(self.WIN, 'Brown', (self.name_font_rect_list[idx].left + 16, self.name_font_rect_list[idx].centery + 17), (self.name_font_rect_list[idx].right + 16, self.name_font_rect_list[idx].centery + 17), 6)


        # Render & blit HP/MP:
        for idx, char in enumerate(self.engine.character_list):
            font_txt = self.HP_font.render(f"HP: {int(char.health)} / {int(char.health_max)}", 1, self.FONT_COLOR_HP)
            font_txt_rect = font_txt.get_rect(topleft = (20, (self.NAMES_SPACING * idx) + self.UNDER_NAME_SPACE + 5))
            self.character_sur.blit(font_txt, font_txt_rect)

            if char.mp_max:
                font_txt = self.HP_font.render(f"MP: {int(char.mp)} / {int(char.mp_max)}", 1, self.FONT_COLOR_HP)
                font_txt_rect = font_txt.get_rect(topleft = (20, 15 + (self.NAMES_SPACING * idx) + (self.UNDER_NAME_SPACE * 2)))
                self.character_sur.blit(font_txt, font_txt_rect)

        # Render & blit HP bars:
        for idx, char in enumerate(self.engine.character_list):
            if char.health:
                char_hp_length = self.HP_BAR_LENGTH // (char.health_max / char.health)
            else:
                char_hp_length = 0
            bg_hp_bar = pygame.Rect(20, 10 + (self.NAMES_SPACING * idx) + self.UNDER_NAME_SPACE + 25, self.HP_BAR_LENGTH, self.HP_BAR_HEIGHT)
            hp_bar = pygame.Rect(20, 10 + (self.NAMES_SPACING * idx) + self.UNDER_NAME_SPACE + 25, char_hp_length, self.HP_BAR_HEIGHT)
            pygame.draw.rect(self.character_sur, 'OrangeRed', hp_bar)
            pygame.draw.rect(self.character_sur, 'Black', bg_hp_bar, 3)
            pygame.draw.rect(self.character_sur, 'Black', hp_bar, 3)

        # MP bars
        for idx, char in enumerate(self.engine.character_list):
            if char.mp:
                char_mp_length = self.HP_BAR_LENGTH // (char.mp_max / char.mp)
            else:
                char_mp_length = 0
            if char.mp_max:
                bg_hp_bar = pygame.Rect(20, 10 + (self.NAMES_SPACING * idx) + (self.UNDER_NAME_SPACE * 2) + 34, self.HP_BAR_LENGTH, self.HP_BAR_HEIGHT)
                hp_bar = pygame.Rect(20, 10 + (self.NAMES_SPACING * idx) + (self.UNDER_NAME_SPACE * 2) + 34, char_mp_length, self.HP_BAR_HEIGHT)
                pygame.draw.rect(self.character_sur, 'Light Blue', hp_bar)
                pygame.draw.rect(self.character_sur, 'Black', bg_hp_bar, 3)
                pygame.draw.rect(self.character_sur, 'Black', hp_bar, 3)


class ConsolePane:
    def __init__(self, WIN, engine):
        self.WIN = WIN
        self.engine = engine
        self.FONT_SIZE = 23
        self.CONSOLE_COLOR = 'Black'
        self.TEXT_COLOR = 'White'
        self.CONSOLE_WIDTH = self.WIN.get_width() - (PANE_WIDTH * 2) - (WIN_BORDER_WIDTH * 2) - (PANE_BORDER_WIDTH * 3)  - (PANE_SPACING * 2)
        self.LEFTSIDE = PANE_WIDTH + WIN_BORDER_WIDTH + int(PANE_BORDER_WIDTH * 1.5) + PANE_SPACING
        self.TOPSIDE = self.WIN.get_height() - CONSOLE_HEIGHT - WIN_BORDER_WIDTH - (PANE_BORDER_WIDTH//2) - PANE_SPACING

        # Console border and background
        self.border_rect = pygame.Rect(self.LEFTSIDE, self.TOPSIDE, self.CONSOLE_WIDTH, CONSOLE_HEIGHT)
        # Console text surface:
        self.surface_txt = pygame.Surface((self.CONSOLE_WIDTH - 30, CONSOLE_HEIGHT - 42))
        # Font:
        self.console_font = pygame.font.SysFont('bahnschrift', self.FONT_SIZE, 0)

    def display_menu(self):
        # Draw background + border:
        pygame.draw.rect(self.WIN, self.CONSOLE_COLOR, self.border_rect)
        pygame.draw.rect(self.WIN, BORDER_COLOR, self.border_rect, PANE_BORDER_WIDTH)

        # Draw text surface with same color as background:
        self.WIN.blit(self.surface_txt, (self.border_rect.x + 25, self.border_rect.y + 18))
        self.surface_txt.fill(self.CONSOLE_COLOR)

        # Write Text:
        for num, line in enumerate(self.engine.complete_text):
            # Indent using keyword because of necessary strip (in engine)
            if line.startswith('=Indent='):
                line = line.replace('=Indent=', '                ')
            if line.startswith('RED:'):
                self.surface_txt.blit(self.console_font.render(line[4:], 1, 'Red'), (0, 0 + (self.FONT_SIZE * num)))
            else:
                self.surface_txt.blit(self.console_font.render(line, 1, self.TEXT_COLOR), (0, 0 + (self.FONT_SIZE * num)))


class MapPane:
    def __init__(self, WIN, engine):
        self.WIN = WIN
        self.engine = engine
        self.MAP_WIDTH = self.WIN.get_width() - (PANE_WIDTH * 2) - (WIN_BORDER_WIDTH * 2) - (PANE_BORDER_WIDTH * 3) - (PANE_SPACING * 2)
        self.MAP_HEIGHT = self.WIN.get_height() - CONSOLE_HEIGHT - (WIN_BORDER_WIDTH * 2) - int(PANE_BORDER_WIDTH * 2) - (PANE_SPACING * 3)
        self.LEFTSIDE = PANE_WIDTH + WIN_BORDER_WIDTH + int(PANE_BORDER_WIDTH * 1.5) + PANE_SPACING
        self.TOPSIDE = WIN_BORDER_WIDTH + (PANE_BORDER_WIDTH // 2) + PANE_SPACING
        self.show_dot = True
        # Surface + rect:
        self.map_sur = pygame.Surface((self.MAP_WIDTH, self.MAP_HEIGHT))
        self.map_rect = self.map_sur.get_rect(topleft=(self.LEFTSIDE, self.TOPSIDE))

        self.map_sur_zoomed = pygame.Surface((self.MAP_WIDTH * 2, self.MAP_HEIGHT * 2))
        self.map_rect_zoomed = self.map_sur_zoomed.get_rect(topleft=(self.LEFTSIDE, self.map_rect.bottom))
        # Get map:
        self.map = Map(self.MAP_WIDTH, self.MAP_HEIGHT) # self.map.map or self.map.map_zoomed for the image
        self.map_zoomed = Map(self.MAP_WIDTH * 2, self.MAP_HEIGHT * 2, zoom=True)


    def display_map(self, surf, map_rect, map):
        # Lock icons:
        if self.engine.door_locked:
            surf.blit(map.lock, (map.lock_x, map.lock_y))
        else:
            surf.blit(map.unlocked, (map.unlocked_x, map.unlocked_y))

        # Key icons, if key or map in inventory:
        for item in self.engine.item_inventory:
            if item[0] == 'Key' or item[0] == 'Map':
                if item[1]:
                    surf.blit(map.key, (map.key_x, map.key_y))
                    break

        # Fog of war check for map:
        no_map = True
        for item in self.engine.item_inventory:
            if item[0] == 'Map':
                if item[1]:
                    no_map = False
        # Draw fog of war:
        count = 0
        for idx, room in enumerate(self.engine.room_list[2:]):  # Omit 0-1 0=None 1=starting room
            if room.fog_on and no_map:
                rect_test = pygame.Rect(map.fog_dict[idx+2][0], map.fog_dict[idx+2][1], map.fog_dict[idx+2][2], map.fog_dict[idx+2][3])
                pygame.draw.rect(surf, 'Black', rect_test)
                # This added because of one wall shared by two room. Draw only if both rooms have fog.
                if room.location == 9 or room.location == 12:
                    count += 1
                    if count == 2:
                        rect_test = pygame.Rect(map.fog_dict[9.12][0], map.fog_dict[9.12][1], map.fog_dict[9.12][2], map.fog_dict[9.12][3])
                        pygame.draw.rect(surf, 'Black', rect_test)

        # Draw location marker:
        if self.show_dot:
            pygame.draw.circle(surf, 'Brown', map.rooms_dict[self.engine.current_room.location], 12)

        # Map surface
        if self.engine.zoom:
            x_loc = map_rect.x - map.rooms_dict[self.engine.current_room.location][0] + (self.MAP_WIDTH // 2)
            y_loc = map_rect.y - map.rooms_dict[self.engine.current_room.location][1] - (self.MAP_HEIGHT // 2)
            self.WIN.blit(surf, (x_loc, y_loc))
        else:
            self.WIN.blit(surf, map_rect)

        # Map image:
        surf.blit(map.map, (0,0))


    def display_menu(self):
        # Zooming map (Think I did this the hard way, not sure why I needed a separate black surface for zoomed. Just put image on pane surface, and use negative coordinates)
        if self.engine.zoom:
            # Adjust lock location, slightly changes with zoom
            self.map.lock_x = int(self.MAP_WIDTH * .61)
            self.display_map(self.map_sur_zoomed, self.map_rect_zoomed, self.map_zoomed)
        else:
            self.map.lock_x = int(self.MAP_WIDTH * .60)
            self.display_map(self.map_sur, self.map_rect, self.map)


        # Black surface with hole for map to hide behind while zoomed (enlarged):
        black_surf = pygame.Surface((self.WIN.get_width(), self.WIN.get_height())).convert_alpha()
        black_surf.fill((0,0,0))
        see_through = pygame.Rect(self.map_rect.x, self.map_rect.y, self.map_rect.width, self.map_rect.height)
        pygame.draw.rect(black_surf, (250,250,250,0), see_through)
        self.WIN.blit(black_surf, (0,0))

        # Border:
        pygame.draw.rect(self.WIN, BORDER_COLOR, self.map_rect, PANE_BORDER_WIDTH)


class Panes:
    def __init__(self, WIN, engine):
        # Create panes:
        self.action_menu = ActionMenu(WIN, engine, PANE_WIDTH, PANE_SPACING, ACTION_MENU_HEIGHT, WIN_BORDER_WIDTH, PANE_BORDER_WIDTH, PANE_COLOR, BORDER_COLOR)
        self.item_menu = ItemMenu(WIN, engine)
        self.character_pane = CharacterPane(WIN, engine)
        self.console_pane = ConsolePane(WIN, engine)
        self.map_pane = MapPane(WIN, engine)
        self.WIN = WIN

    def display_screen(self):
        # Draw Panes:
        self.WIN.fill('black')
        self.map_pane.display_menu()
        self.action_menu.display_menu()
        self.item_menu.display_menu()
        self.character_pane.display_menu()
        self.console_pane.display_menu()
