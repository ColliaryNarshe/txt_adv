import pygame
from sys import exit

# Dot event
dot_event = pygame.USEREVENT + 1
pygame.time.set_timer(dot_event, 900)

# Event for holding down arrow keys in menu
arrow_event = pygame.USEREVENT + 2
pygame.time.set_timer(arrow_event, 150)

going_north = False
# Used for arrows holding down
down = 2
up = 2

def keyboard_input(panes, engine):
    global going_north
    global down
    global up

    # Keys_pressed checked below with timed event
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_DOWN]:
        down += 1
        if down >= 2:
            engine.menu_sound.play()
            engine.menu_sound.set_volume(.3)
            panes.action_menu.move_down()
            down = 0
    else:
        down = 2

    if keys_pressed[pygame.K_UP]:
        up += 1
        if up >= 2:
            engine.menu_sound.play()
            engine.menu_sound.set_volume(.3)
            panes.action_menu.move_up()
            up = 0
    else:
        up = 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Blinking dot on map:
        if event.type == dot_event:
            panes.map_pane.show_dot = not panes.map_pane.show_dot

        # Arrow keys for menu select (one at a time no holding):
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_DOWN:
                # engine.menu_sound.play()
                # engine.menu_sound.set_volume(.3)
                # panes.action_menu.move_down()
            #
            # if event.key == pygame.K_UP:
            #     engine.menu_sound.play()
            #     engine.menu_sound.set_volume(.3)
            #     panes.action_menu.move_up()

            # WASD shortcut movements:
            if engine.menu_state != 'choice' and engine.menu_state != 'characters' and engine.menu_state != 'items':
                if event.key == pygame.K_w:
                    going_north = True
                    new_room(0, panes, engine)
                if event.key == pygame.K_s:
                    new_room(1, panes, engine)
                if event.key == pygame.K_a:
                    new_room(2, panes, engine)
                if event.key == pygame.K_d:
                    new_room(3, panes, engine)
                # if event.key == pygame.K_i:  # Removed because no point, just press enter
                #     engine.inspect_room()
                if event.key == pygame.K_m:
                    engine.zoom = not engine.zoom
                # if event.key == pygame.K_f:
                #     # will need to make fog of war rects adjustable sizes rather than set, otherwise works.
                #     panes.item_menu.WIN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                #     return True


            # menu item select:
            if event.key == pygame.K_RETURN:
                # Quit menu:
                if engine.game_over:
                    if panes.action_menu.cursor_location == 0:  # Restart
                        engine.restart = True
                    if panes.action_menu.cursor_location == 1:  # Quit
                        pygame.quit()
                        exit()

                # Option menu
                elif panes.action_menu.option_menu_on:
                    if panes.action_menu.cursor_location == 0:  # Return
                        panes.action_menu.option_menu_on = False
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        return
                    if panes.action_menu.cursor_location == 1:  # Restart
                        engine.restart = True
                    if panes.action_menu.cursor_location == 2:  # Save
                        pass
                    if panes.action_menu.cursor_location == 3:  # Seed
                        pass
                    if panes.action_menu.cursor_location == 4:  # Screen
                        pass
                    if panes.action_menu.cursor_location == 5:  # Zoom
                        engine.zoom = not engine.zoom
                        return
                    if panes.action_menu.cursor_location == 6:  # Shortcuts
                        pass
                    if panes.action_menu.cursor_location == 7:  # Credits
                        pass
                    if panes.action_menu.cursor_location == 8:  # Quit
                        pygame.quit()
                        exit()

                # Room 25 split left right choice:
                elif engine.menu_state == 'left_right':
                    if panes.action_menu.cursor_location == 0:  # Left
                        engine.left_choice = True
                        engine.split_room()
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        return

                    if panes.action_menu.cursor_location == 1:  # Right
                        engine.left_choice = False
                        engine.split_room()
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        panes.action_menu.cursor_location = 0
                        return

                # Main menu items:
                if engine.menu_state == 'main':
                    if panes.action_menu.cursor_location == 0:  # Inspect
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        engine.inspect_room()

                    if panes.action_menu.cursor_location == 1:  # North
                        going_north = True
                        new_room(0, panes, engine)

                    if panes.action_menu.cursor_location == 2:  # South
                        new_room(1, panes, engine)

                    if panes.action_menu.cursor_location == 3:  # West
                        new_room(2, panes, engine)

                    if panes.action_menu.cursor_location == 4:  # East
                        new_room(3, panes, engine)

                    if panes.action_menu.cursor_location == 5:  # Use item
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        engine.menu_state = 'items'
                        panes.action_menu.update_item_menu()
                        panes.action_menu.cursor_location = 0

                    if panes.action_menu.cursor_location == 6:  # Use magic heal
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        engine.menu_state = 'characters_return'
                        panes.action_menu.cursor_location = 0

                    if panes.action_menu.cursor_location == 7: # Option menu
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        panes.action_menu.cursor_location = 0
                        panes.action_menu.option_menu_on = True
                        return



                elif engine.menu_state == 'choice':
                    if engine.room_enter_states['battle'] and not engine.room_enter_states['special_choice']:
                        # Choose to fight battle:
                        if panes.action_menu.cursor_location == 0: # Yes battle
                            engine.menu_state = 'main'
                            engine.enter_room()

                        # Choose not to fight, return to prev room
                        if panes.action_menu.cursor_location == 1:  # No battle
                            engine.running_sound.play()
                            engine.running_sound.set_volume(.3)
                            engine.menu_state = 'main'
                            engine.current_room = engine.previous_room
                            engine.update_console(["----------", f"You have backtracked to the previous room."])
                            engine.room_enter_states['battle'] = False
                            engine.room_enter_states['enter'] = True
                            panes.action_menu.cursor_location = 0


                    if engine.room_enter_states['special_choice'] or engine.room_enter_states['inspect_treasure']:
                        if panes.action_menu.cursor_location == 0: # Yes special
                            engine.option = 'yes'
                            # panes.action_menu.set_character_states_dead_or_full(set_all=True)
                            engine.inspect_room()

                        if panes.action_menu.cursor_location == 1: # No special
                            engine.option = 'no'
                            panes.action_menu.cursor_location = 0
                            engine.inspect_room()

                elif engine.menu_state == 'characters_return':
                    if panes.action_menu.cursor_location == 5:
                        panes.action_menu.cursor_location = 0
                        engine.menu_state = 'main'
                        engine.menu_sound.play()
                        engine.menu_sound.set_volume(.3)
                        panes.action_menu.inventory_active = False
                        return

                    # For inventory character selection:
                    engine.character_selection = engine.character_list[panes.action_menu.cursor_location]

                    if panes.action_menu.inventory_active:
                        panes.action_menu.use_inventory()
                        # panes.action_menu.update_item_menu()
                    else:
                        # Healing magic
                        engine.heal_magic()

                elif engine.menu_state == 'characters':
                    # Get character choice
                    engine.character_selection = engine.character_list[panes.action_menu.cursor_location]

                    # For equipping (finding certain items)
                    panes.action_menu.cursor_location = 0
                    engine.chosen_char = True
                    # To add item to inventory (with choice to equip)
                    engine.item_character_choice()
                    engine.inspect_room()

                # Inventory
                elif engine.menu_state == 'items':
                    engine.menu_sound.play()
                    engine.menu_sound.set_volume(.3)
                    # Get the item index:
                    panes.action_menu.character_index = panes.action_menu.cursor_location
                    idx = panes.action_menu.character_index  # Redundant just to read easier
                    # panes.action_menu.set_character_states_dead_or_full()
                    panes.action_menu.no_items_usable = False # delete this if calling above

                    if not panes.action_menu.no_items_usable:
                        # Return to main menu
                        if panes.action_menu.accessible_items[idx] == 'Return':
                            engine.menu_state = 'main'
                            panes.action_menu.cursor_location = 0
                        # Go to Character selection menu:
                        else:
                            engine.menu_state = 'characters_return'
                            panes.action_menu.cursor_location = 0
                            panes.action_menu.inventory_active = True
                            panes.action_menu.check_if_disabled(1, panes.action_menu.character_menu)
                            # panes.action_menu.cursor_location -= 1 # Does check_if_disabled move the cursor down?

                    else:
                        if panes.action_menu.accessible_items[idx] == 'Return':
                            engine.menu_sound.play()
                            engine.menu_sound.set_volume(.3)
                            engine.menu_state = 'main'
                            panes.action_menu.cursor_location = 0




# Note: Add try in case of IndexError later
def new_room(num, panes, engine):
    # going_north used for locked door
    global going_north

    # engine.room_enter_states['enter'] = True  # This line maybe not necessary
    engine.room_enter_states['text'] = False # Not sure if this is necessary
    engine.room_enter_states['inspect_treasure'] = False  # This one yes
    # Get room from list then change to current_room
    room_num = engine.current_room.room_choices[num]

    # Get a message from locked room.
    if engine.current_room.location == 20:
        if engine.current_room.lock and going_north:
            engine.update_console(["The door is locked!"])
            going_north = False
            return
    going_north = False

    # Prevent movement with WASD shortcuts:
    if room_num == 0 or engine.game_over:
        return

    engine.complete_text = []  # Empty console txt from prev room

    # Save previous room in case run from fight
    engine.previous_room = engine.current_room
    engine.current_room = engine.room_list[room_num]
    engine.current_room.fog_on = False  # Fog of war off
    # Put cursor to top of menu:
    panes.action_menu.cursor_location = 0

    # Sound effect:
    # if not pygame.mixer.get_busy():
    if not engine.channel.get_busy():
        engine.channel.play(engine.walking_sound)
        # engine.walking_sound.play()

    # Reset timer so that new dot location won't start invisible:
    pygame.time.set_timer(dot_event, 0)
    pygame.time.set_timer(dot_event, 900)
    panes.map_pane.show_dot = True

    if engine.current_room.location == 26:
        if engine.current_room.enemies:
            engine.display_room_txt()

    if engine.current_room.location == 27:
        engine.last_room()

    engine.enter_room()
    # Disables unusable menu choices
    panes.action_menu.disable_menus()
