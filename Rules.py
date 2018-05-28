import collections
import logging


def set_rules(world):
    global_rules(world)

    if world.bridge == 'medallions':
        # require all medallions to form the bridge
        set_rule(world.get_entrance('Rainbow Bridge'), lambda state: state.has('Forest Medallion') and state.has('Fire Medallion') and state.has('Water Medallion') and state.has('Shadow Medallion') and state.has('Spirit Medallion') and state.has('Light Medallion'))
    elif world.bridge == 'vanilla':
        # require only what vanilla did to form the bridge
        set_rule(world.get_entrance('Rainbow Bridge'), lambda state: state.has('Light Arrows') and state.has('Shadow Medallion') and state.has('Spirit Medallion'))
    elif world.bridge == 'dungeons':
        # require all medallions and stones to form the bridge
        set_rule(world.get_entrance('Rainbow Bridge'), lambda state: state.has('Forest Medallion') and state.has('Fire Medallion') and state.has('Water Medallion') and state.has('Shadow Medallion') and state.has('Spirit Medallion') and state.has('Light Medallion') and state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire'))


def set_rule(spot, rule):
    spot.access_rule = rule

def set_always_allow(spot, rule):
    spot.always_allow = rule


def add_rule(spot, rule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def forbid_item(location, item):
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name != item and old_rule(i)


def item_in_locations(state, item, locations):
    for location in locations:
        if item_name(state, location) == item:
            return True
    return False

def item_name(state, location):
    location = state.world.get_location(location)
    if location.item is None:
        return None
    return location.item.name


def global_rules(world):
    # ganon can only carry triforce
    world.get_location('Ganon').item_rule = lambda item: item.name == 'Triforce'

    # these are default save&quit points and always accessible
    world.get_region('Links House').can_reach = lambda state: True

    # overworld requirements
    set_rule(world.get_entrance('Deku Tree'), lambda state: state.has('Kokiri Sword') or world.open_forest)
    set_rule(world.get_entrance('Lost Woods Bridge'), lambda state: world.open_forest or (state.has('Slingshot') and state.has('Kokiri Sword')))
    set_rule(world.get_entrance('Deku Tree Basement Path'), lambda state: state.has('Slingshot'))
    set_rule(world.get_location('Skull Kid'), lambda state: state.has('Sarias Song'))
    set_rule(world.get_location('Ocarina Memory Game'), lambda state: state.has('Fairy Ocarina') or state.has('Ocarina of Time'))
    set_rule(world.get_location('Target in Woods'), lambda state: state.has('Slingshot'))
    set_rule(world.get_location('Deku Theater Skull Mask'), lambda state: state.has('Zeldas Letter'))
    set_rule(world.get_location('Deku Theater Mask of Truth'), lambda state: state.has('Zeldas Letter') and state.has('Sarias Song') and state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire') and state.guarantee_hint()) #Must befriend Skull Kid to sell Skull Mask, all stones to spawn running man.
    set_rule(world.get_location('Anju as Adult'), lambda state: state.is_adult())
    set_rule(world.get_location('Man on Roof'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('10 Gold Skulltulla Reward'), lambda state: state.has('Gold Skulltulla Token', 10))
    set_rule(world.get_location('20 Gold Skulltulla Reward'), lambda state: state.has('Gold Skulltulla Token', 20))
    set_rule(world.get_location('30 Gold Skulltulla Reward'), lambda state: state.has('Gold Skulltulla Token', 30) and state.guarantee_hint())
    set_rule(world.get_location('40 Gold Skulltulla Reward'), lambda state: state.has('Gold Skulltulla Token', 40) and state.guarantee_hint())
    set_rule(world.get_location('50 Gold Skulltulla Reward'), lambda state: state.has('Gold Skulltulla Token', 50) and state.guarantee_hint())
    set_rule(world.get_location('Heart Piece Grave Chest'), lambda state: state.has('Suns Song'))
    set_rule(world.get_entrance('Composer Grave'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Composer Grave Chest'), lambda state: state.has_fire_source())
    set_rule(world.get_entrance('Bottom of the Well'), lambda state: state.has('Song of Storms'))
    set_rule(world.get_location('Bottom of the Well Front Left Hidden Wall'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Front Center Bombable'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Bottom of the Well Right Bottom Hidden Wall'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Center Large Chest'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Center Small Chest'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Back Left Bombable'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Bottom of the Well Defeat Boss'), lambda state: state.has('Zeldas Lullaby') and state.has('Kokiri Sword')) #Sword not strictly necessary but frankly being forced to do this with sticks isn't fair
    set_rule(world.get_location('Bottom of the Well Invisible Chest'), lambda state: state.has('Zeldas Lullaby') and state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Underwater Front Chest'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Bottom of the Well Underwater Left Chest'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Bottom of the Well Basement Chest'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Bottom of the Well Locked Pits'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Lens of Truth') and state.has('Magic Meter')) #These pits are really unfair.
    set_rule(world.get_location('Bottom of the Well Behind Right Grate'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_entrance('Death Mountain Entrance'), lambda state: state.has('Zeldas Letter') or state.is_adult())
    set_rule(world.get_location('Death Mountain Bombable Chest'), lambda state: state.can_blast())
    set_rule(world.get_location('Biggoron'), lambda state: state.can_blast() and state.is_adult() and state.can_finish_adult_trades() and state.guarantee_hint())
    set_rule(world.get_location('Goron City Leftmost Maze Chest'), lambda state: state.is_adult() and (state.has('Progressive Strength Upgrade', 2) or state.has('Hammer')))
    set_rule(world.get_location('Goron City Left Maze Chest'), lambda state: state.can_blast() or (state.has('Progressive Strength Upgrade', 2) and state.is_adult()))
    set_rule(world.get_location('Goron City Right Maze Chest'), lambda state: state.can_blast() or (state.has('Progressive Strength Upgrade', 2) and state.is_adult()))
    set_rule(world.get_location('Rolling Goron as Child'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_entrance('Darunias Chamber'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Darunias Joy'), lambda state: state.has('Sarias Song'))
    set_rule(world.get_entrance('Goron City from Woods'), lambda state: state.can_blast() and (world.open_forest or (state.has('Slingshot') and state.has('Kokiri Sword'))))
    set_rule(world.get_entrance('Dodongos Cavern Rocks'), lambda state: state.can_blast() or state.has('Progressive Strength Upgrade') or state.is_adult())
    set_rule(world.get_entrance('Dodongos Cavern Lobby'), lambda state: state.can_blast() or state.has('Progressive Strength Upgrade'))
    set_rule(world.get_entrance('Dodongos Cavern Slingshot Target'), lambda state: state.has('Slingshot') or ((state.has('Bow') or state.has('Hover Boots')) and state.is_adult()))
    set_rule(world.get_location('Dodongos Cavern End of Bridge Chest'), lambda state: state.has('Bomb Bag') or ((state.has('Bow') or state.has('Hover Boots')) and state.is_adult() and state.has('Hammer')))
    set_rule(world.get_entrance('Dodongos Cavern Bomb Drop'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Song from Saria'), lambda state: state.has('Zeldas Letter'))
    set_rule(world.get_entrance('Mountain Summit Fairy'), lambda state: state.can_blast())
    set_rule(world.get_location('Crater Fairy Reward'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Mountain Summit Fairy Reward'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Mountain Crater Entrance'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Hyrule Castle Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Hyrule Castle Fairy Reward'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Ganons Castle Grounds'), lambda state: state.is_adult())
    set_rule(world.get_entrance('Ganons Castle Fairy'), lambda state: state.has('Progressive Strength Upgrade', 3))
    set_rule(world.get_location('Bombchu Bowling Bomb Bag'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Bombchu Bowling Piece of Heart'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Adult Shooting Gallery'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('10 Big Poes'), lambda state: state.has('Bow') and state.has('Epona') and state.has_bottle() and state.is_adult() and state.guarantee_hint())
    set_rule(world.get_location('Treasure Chest Game'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_entrance('Lost Woods Dive Warp'), lambda state: state.can_dive() and (world.open_forest or (state.has('Slingshot') and state.has('Kokiri Sword'))))
    set_rule(world.get_entrance('Zora River Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Lake Hylia Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zoras Domain Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zora River Waterfall'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Zora River Rocks'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Frog Ocarina Game'), lambda state: state.has('Zeldas Lullaby') and state.has('Sarias Song') and state.has('Suns Song') and state.has('Eponas Song') and state.has('Song of Time') and state.has('Song of Storms'))
    set_rule(world.get_location('Frogs in the Rain'), lambda state: state.has('Song of Storms'))
    set_rule(world.get_location('Underwater Bottle'), lambda state: state.can_dive())
    set_rule(world.get_location('King Zora Moves'), lambda state: state.has('Bottle with Letter'))
    set_rule(world.get_entrance('Behind King Zora'), lambda state: state.has('Bottle with Letter'))
    set_rule(world.get_entrance('Zora River Adult'), lambda state: state.is_adult())
    set_rule(world.get_entrance('Zoras Domain Adult Access'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Zoras Fountain Adult Access'), lambda state: state.can_reach('Zoras Fountain'))
    set_rule(world.get_entrance('Jabu Jabus Belly'), lambda state: state.has_bottle())
    set_rule(world.get_entrance('Zoras Fountain Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Zoras Fountain Fairy Reward'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Jabu Jabus Belly Ceiling Switch'), lambda state: state.has('Slingshot') or state.has('Bomb Bag') or state.has('Boomerang'))
    set_rule(world.get_entrance('Jabu Jabus Belly Tentacles'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('Ice Cavern Map Chest'), lambda state: state.has_bottle())
    set_rule(world.get_location('Ice Cavern Compass Chest'), lambda state: state.has_bottle())
    set_rule(world.get_location('Ice Cavern Iron Boots Chest'), lambda state: state.has_bottle())
    set_rule(world.get_location('Sheik in Ice Cavern'), lambda state: state.has_bottle() and state.is_adult())
    set_rule(world.get_location('Ocarina of Time'), lambda state: state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire') and state.guarantee_hint())
    set_rule(world.get_location('Song from Ocarina of Time'), lambda state: state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire') and state.guarantee_hint())
    set_rule(world.get_entrance('Door of Time'), lambda state: state.has('Song of Time') or world.open_door_of_time)
    set_rule(world.get_location('Talons Chickens'), lambda state: state.has('Zeldas Letter'))
    set_rule(world.get_location('Epona'), lambda state: state.has('Eponas Song') and state.is_adult())
    set_rule(world.get_entrance('Adult Forest Warp Pad'), lambda state: state.has('Minuet of Forest') and state.is_adult())
    set_rule(world.get_entrance('Child Forest Warp Pad'), lambda state: state.has('Minuet of Forest'))
    set_rule(world.get_entrance('Adult Meadow Access'), lambda state: state.has('Sarias Song') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Entrance'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Song of Time Block'), lambda state: state.has('Song of Time'))
    set_rule(world.get_entrance('Forest Temple Lobby Eyeball Switch'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Lobby Locked Door'), lambda state: state.has('Progressive Strength Upgrade') and state.has('Small Key (Forest Temple)', 1))
    set_rule(world.get_entrance('Forest Temple Well Connection'), lambda state: ((state.has('Iron Boots') or state.has('Progressive Hookshot', 2)) and state.is_adult()) or state.has('Progressive Scale', 2)) #Longshot can grab some very high up vines to drain the well.
    set_rule(world.get_entrance('Forest Temple Scarecrows Song'), lambda state: False) #For some reason you can't actually activate this from below. Cool game.
    set_rule(world.get_entrance('Forest Temple Elevator'), lambda state: state.has('Bow') and state.is_adult() and state.has('Progressive Strength Upgrade') and state.has('Small Key (Forest Temple)', 3))
    set_rule(world.get_entrance('Forest Temple Outside Backdoor'), lambda state: state.has('Hover Boots') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Twisted Hall'), lambda state: state.has('Small Key (Forest Temple)', 3))
    set_rule(world.get_entrance('Forest Temple Straightened Hall'), lambda state: state.has('Small Key (Forest Temple)', 2) and state.has('Bow'))
    set_rule(world.get_entrance('Forest Temple Drop to Falling Room'), lambda state: state.has('Small Key (Forest Temple)', 5) and (state.has('Bow') or (state.has('Dins Fire') and state.has('Magic Meter'))))
    set_rule(world.get_location('Forest Temple Block Push Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Forest Temple Red Poe Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Forest Temple Blue Poe Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Phantom Ganon'), lambda state: state.has('Boss Key (Forest Temple)'))
    set_rule(world.get_entrance('Dampes Grave'), lambda state: state.is_adult())
    set_rule(world.get_location('Song at Windmill'), lambda state: state.is_adult())
    set_rule(world.get_entrance('Temple Warp Pad'), lambda state: state.has('Prelude of Light'))
    set_rule(world.get_location('Sheik at Temple'), lambda state: state.has('Forest Medallion') and state.is_adult())
    set_rule(world.get_location('Diving in the Lab'), lambda state: state.has('Progressive Scale', 2))
    set_rule(world.get_location('Child Fishing'), lambda state: state.has('Kokiri Sword') and state.guarantee_hint())
    set_rule(world.get_location('Adult Fishing'), lambda state: state.is_adult() and (state.has('Progressive Hookshot') or state.has('Magic Bean')) and state.guarantee_hint())
    set_rule(world.get_location('Lake Hylia Sun'), lambda state: state.has('Progressive Hookshot', 2) and state.has('Bow') and state.is_adult())
    set_rule(world.get_entrance('Crater Hover Boots'), lambda state: state.is_adult() and state.has('Hover Boots'))
    set_rule(world.get_entrance('Crater Ascent'), lambda state: state.is_adult() and (state.has('Goron Tunic') or (state.has('Progressive Wallet') and state.has('Bomb Bag'))) and (state.has('Hover Boots') or state.has('Hammer')))
    set_rule(world.get_entrance('Crater Scarecrow'), lambda state: state.is_adult() and state.has('Progressive Hookshot', 2) and (state.has('Goron Tunic') or (state.has('Progressive Wallet') and state.has('Bomb Bag'))))
    set_rule(world.get_entrance('Crater Bridge'), lambda state: state.is_adult() and (state.has('Hover Boots') or state.has('Progressive Hookshot')))
    set_rule(world.get_entrance('Crater Bridge Reverse'), lambda state: state.is_adult() and (state.has('Hover Boots') or state.has('Progressive Hookshot')))
    set_rule(world.get_entrance('Crater Warp Pad'), lambda state: state.has('Bolero of Fire'))
    set_rule(world.get_entrance('Crater Fairy'), lambda state: state.is_adult() and state.has('Hammer'))
    set_rule(world.get_entrance('Fire Temple Entrance'), lambda state: state.is_adult() and (state.has('Goron Tunic') or (state.has('Progressive Wallet') and state.has('Bomb Bag'))))
    set_rule(world.get_entrance('Fire Temple Early Climb'), lambda state: state.has('Small Key (Fire Temple)', 3) and state.has('Progressive Strength Upgrade') and (state.has('Bomb Bag') or ((state.has('Bow') or state.has('Progressive Hookshot')) and state.is_adult())))
    set_rule(world.get_entrance('Fire Temple Fire Maze Escape'), lambda state: state.has('Small Key (Fire Temple)', 7) or (state.has('Small Key (Fire Temple)', 6) and state.has('Hover Boots') and state.has('Hammer') and state.is_adult()))
    set_rule(world.get_location('Fire Temple Fire Dancer Chest'), lambda state: state.is_adult() and state.has('Hammer'))
    set_rule(world.get_location('Fire Temple Boss Key Chest'), lambda state: state.is_adult() and state.has('Hammer'))
    set_rule(world.get_location('Fire Temple Big Lava Room Bombable Chest'), lambda state: state.has('Small Key (Fire Temple)', 1) and state.has('Bomb Bag'))
    set_rule(world.get_location('Fire Temple Big Lava Room Open Chest'), lambda state: state.has('Small Key (Fire Temple)', 1))
    set_rule(world.get_location('Fire Temple Map Chest'), lambda state: state.has('Small Key (Fire Temple)', 5) or (state.has('Small Key (Fire Temple)', 4) and state.is_adult() and state.has('Bow')))
    set_rule(world.get_location('Fire Temple Boulder Maze Upper Chest'), lambda state: state.has('Small Key (Fire Temple)', 5))
    set_rule(world.get_location('Fire Temple Boulder Maze Bombable Pit'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Bomb Bag'))
    set_rule(world.get_location('Fire Temple Scarecrow Chest'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('Fire Temple Compass Chest'), lambda state: state.has('Small Key (Fire Temple)', 6))
    set_rule(world.get_location('Fire Temple Highest Goron Chest'), lambda state: state.has('Song of Time') and state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('Fire Temple Megaton Hammer Chest'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Volvagia'), lambda state: state.has('Hammer') and state.is_adult() and state.has('Boss Key (Fire Temple)') and (state.has('Hover Boots') or (state.can_reach('Fire Temple Upper') and (state.has('Song of Time') or state.has('Bomb Bag')))))
    set_rule(world.get_location('Sheik in Crater'), lambda state: state.is_adult())
    set_rule(world.get_location('Link the Goron'), lambda state: state.is_adult() and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag')))
    set_rule(world.get_entrance('Crater Access'), lambda state: state.is_adult() and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag')))
    set_rule(world.get_entrance('Lake Warp Pad'), lambda state: state.has('Serenade of Water'))
    set_rule(world.get_location('King Zora Thawed'), lambda state: state.has_bottle() and (state.can_reach('Ice Cavern') or state.can_reach('Ganons Castle Water Trial') or state.has('Progressive Wallet', 2)))
    set_rule(world.get_entrance('Water Temple Entrance'), lambda state: state.is_adult() and (state.has('Zora Tunic') or (state.has('Progressive Wallet', 2) and state.has_bottle() and state.has('Zeldas Lullaby'))) and state.has('Iron Boots') and state.has('Progressive Hookshot'))
    set_rule(world.get_entrance('Water Temple Central Pillar'), lambda state: (state.has('Bow') or (state.has('Dins Fire') and state.has('Magic Meter')) or state.has('Small Key (Water Temple)', 5)) and state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Water Temple Upper Locked Door'), lambda state: state.has('Small Key (Water Temple)', 5) and (state.has('Zeldas Lullaby') or world.keysanity))
    set_rule(world.get_location('Water Temple Torches Chest'), lambda state: (state.has('Bow') or (state.has('Dins Fire') and state.has('Magic Meter'))) and state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Water Temple Dragon Chest'), lambda state: (state.has('Progressive Strength Upgrade') and state.has('Zeldas Lullaby')) or (state.has('Small Key (Water Temple)', 6) and (state.has('Zeldas Lullaby') or world.keysanity) and state.has('Song of Time') and state.has('Bow')))
    set_rule(world.get_location('Water Temple Central Bow Target Chest'), lambda state: state.has('Bow') and state.has('Progressive Strength Upgrade') and state.has('Zeldas Lullaby') and (state.has('Hover Boots') or state.has('Progressive Hookshot', 2)))
    set_always_allow(world.get_location('Water Temple Boss Key Chest'), lambda state, item: item.name == 'Small Key (Water Temple)')
    set_rule(world.get_location('Water Temple Boss Key Chest'), lambda state: (state.has('Small Key (Water Temple)', 6) and (state.has('Zeldas Lullaby') or world.keysanity) and ((state.has('Bomb Bag') and state.has('Progressive Strength Upgrade')) or state.has('Hover Boots')) and state.has('Progressive Hookshot', 2)) or item_name(state, 'Water Temple Boss Key Chest') == 'Small Key (Water Temple)') #If key for key, this lets the logic reduce the small key reqs for every other locked door.
    set_rule(world.get_location('Morpha'), lambda state: state.has('Boss Key (Water Temple)') and state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('Water Temple Cracked Wall Chest'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Water Temple Dark Link Chest'), lambda state: state.has('Small Key (Water Temple)', 6) and (state.has('Zeldas Lullaby') or world.keysanity))
    set_rule(world.get_location('Water Temple River Chest'), lambda state: state.has('Small Key (Water Temple)', 6) and state.has('Song of Time') and state.has('Bow') and (state.has('Zeldas Lullaby') or world.keysanity))
    set_rule(world.get_location('Sheik in Kakariko'), lambda state: state.has('Forest Medallion') and state.has('Fire Medallion') and state.has('Water Medallion'))
    set_rule(world.get_entrance('Graveyard Warp Pad'), lambda state: state.has('Nocturne of Shadow'))
    set_rule(world.get_entrance('Shadow Temple Entrance'), lambda state: state.has('Dins Fire') and state.has('Magic Meter') and state.has('Lens of Truth') and state.is_adult() and (state.has('Hover Boots') or state.has('Progressive Hookshot')))
    set_rule(world.get_entrance('Shadow Temple First Pit'), lambda state: state.has('Hover Boots'))
    set_rule(world.get_entrance('Shadow Temple Bomb Wall'), lambda state: state.has('Bomb Bag') and state.has('Small Key (Shadow Temple)', 1))
    set_rule(world.get_entrance('Shadow Temple Hookshot Target'), lambda state: state.has('Progressive Hookshot') and state.has('Small Key (Shadow Temple)', 2))
    set_rule(world.get_entrance('Shadow Temple Boat'), lambda state: state.has('Progressive Strength Upgrade') and state.has('Zeldas Lullaby') and state.has('Small Key (Shadow Temple)', 3))
    set_rule(world.get_location('Shadow Temple Falling Spikes Upper Chest'), lambda state: state.has('Progressive Strength Upgrade'))
    set_rule(world.get_location('Shadow Temple Falling Spikes Switch Chest'), lambda state: state.has('Progressive Strength Upgrade'))
    set_rule(world.get_location('Shadow Temple Invisible Spikes Chest'), lambda state: state.has('Small Key (Shadow Temple)', 2))
    set_rule(world.get_location('Bongo Bongo'), lambda state: state.has('Small Key (Shadow Temple)', 4) and state.has('Bow') and state.has('Boss Key (Shadow Temple)'))
    set_rule(world.get_entrance('Bridge Crossing'), lambda state: (state.has('Epona') or state.has('Progressive Hookshot', 2)) and state.is_adult())
    set_rule(world.get_location('Gerudo Valley Hammer Rocks Chest'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_entrance('Fortress Entrance'), lambda state: (state.has('Bow') or state.has('Progressive Hookshot') or state.has('Hover Boots')) and state.is_adult())
    set_rule(world.get_entrance('Gerudo Training Grounds Entrance'), lambda state: state.has('Gerudo Membership Card') and state.is_adult())
    set_rule(world.get_entrance('Haunted Wasteland Entrance'), lambda state: state.has('Gerudo Membership Card') and state.is_adult() and (state.has('Hover Boots') or state.has('Progressive Hookshot', 2)))
    set_rule(world.get_entrance('Haunted Wasteland Crossing'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_entrance('Colossus Warp Pad'), lambda state: state.has('Requiem of Spirit'))
    set_rule(world.get_entrance('Colossus Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Desert Colossus Fairy Reward'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Gerudo Fortress Rooftop Chest'), lambda state: (state.has('Hover Boots') or state.has('Progressive Hookshot', 2)) and state.is_adult())
    set_rule(world.get_location('Horseback Archery 1000 Points'), lambda state: state.has('Gerudo Membership Card') and state.has('Epona') and state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Horseback Archery 1500 Points'), lambda state: state.has('Gerudo Membership Card') and state.has('Epona') and state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Haunted Wasteland Structure Chest'), lambda state: state.has_fire_source())
    set_rule(world.get_entrance('Gerudo Training Ground Left Silver Rupees'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_entrance('Gerudo Training Ground Beamos'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_entrance('Gerudo Training Grounds Right Locked Doors'), lambda state: False) # The nature of the logic in here makes this path only open if you can also get to the destination otherwise.
    set_rule(world.get_entrance('Gerudo Training Grounds Maze Ledge'), lambda state: state.has('Song of Time'))
    set_rule(world.get_entrance('Gerudo Training Grounds Right Hookshot Target'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_entrance('Gerudo Training Grounds Hammer Target'), lambda state: state.has('Hammer') and state.has('Bow') and state.is_adult())
    set_rule(world.get_entrance('Gerudo Training Grounds Hidden Hookshot Target'), lambda state: state.has('Progressive Hookshot') and state.has('Lens of Truth') and state.has('Magic Meter') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Lobby Left Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Lobby Right Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Beamos Chest'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Gerudo Training Grounds Hidden Ceiling Chest'), lambda state: state.has('Small Key (Gerudo Training Grounds)', 2) and state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Gerudo Training Grounds Maze Path First Chest'), lambda state: state.has('Small Key (Gerudo Training Grounds)', 3))
    set_rule(world.get_location('Gerudo Training Grounds Maze Path Second Chest'), lambda state: state.has('Small Key (Gerudo Training Grounds)', 5))
    set_rule(world.get_location('Gerudo Training Grounds Maze Path Third Chest'), lambda state: state.has('Small Key (Gerudo Training Grounds)', 6))
    set_always_allow(world.get_location('Gerudo Training Grounds Maze Path Final Chest'), lambda state, item: item.name == 'Small Key (Gerudo Training Grounds)')
    set_rule(world.get_location('Gerudo Training Grounds Maze Path Final Chest'), lambda state: (state.has('Small Key (Gerudo Training Grounds)', 8)) or (item_name(state, 'Gerudo Training Grounds Maze Path Final Chest') == 'Small Key (Gerudo Training Grounds)' and state.has('Small Key (Gerudo Training Grounds)', 7))) #Allow key for key
    set_rule(world.get_location('Gerudo Training Grounds Underwater Silver Rupee Chest'), lambda state: state.has('Progressive Hookshot') and state.has('Song of Time') and state.has('Iron Boots') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Hammer Room Switch Chest'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Eye Statue Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Near Scarecrow Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Heavy Block First Chest'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.has('Lens of Truth') and state.has('Magic Meter') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Heavy Block Second Chest'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.has('Lens of Truth') and state.has('Magic Meter') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Heavy Block Third Chest'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.has('Lens of Truth') and state.has('Magic Meter') and state.is_adult())
    set_rule(world.get_location('Gerudo Training Grounds Heavy Block Fourth Chest'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.has('Lens of Truth') and state.has('Magic Meter') and state.is_adult())
    set_rule(world.get_entrance('Spirit Temple Crawl Passage'), lambda state: state.has('Requiem of Spirit'))
    set_rule(world.get_entrance('Spirit Temple Silver Block'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.is_adult())
    set_rule(world.get_entrance('Child Spirit Temple Passthrough'), lambda state: state.has('Bomb Bag') and state.has('Small Key (Spirit Temple)', 1))
    set_rule(world.get_entrance('Adult Spirit Temple Passthrough'), lambda state: state.has('Small Key (Spirit Temple)', 1))
    set_rule(world.get_entrance('Spirit Temple Central Locked Door'), lambda state: state.has('Small Key (Spirit Temple)', 4) and state.has('Progressive Strength Upgrade', 2) and state.is_adult())
    set_rule(world.get_entrance('Spirit Temple Final Locked Door'), lambda state: state.has('Small Key (Spirit Temple)', 5) and (state.has('Progressive Hookshot') or state.has('Bow') or state.has('Bomb Bag')))
    set_rule(world.get_location('Spirit Temple Child Left Chest'), lambda state: state.has('Boomerang') or state.has('Slingshot'))
    set_rule(world.get_location('Spirit Temple Child Right Chest'), lambda state: state.has('Boomerang') or state.has('Slingshot'))
    set_rule(world.get_location('Spirit Temple Compass Chest'), lambda state: state.has('Progressive Hookshot') and state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Spirit Temple Early Adult Right Chest'), lambda state: state.has('Bow') or state.has('Progressive Hookshot') or state.has('Bomb Bag')) #Bomb Bag option requires a very specific Bombchu use, Hover Boots can be skipped by jumping on top of the rolling rock.
    set_rule(world.get_location('Spirit Temple First Mirror Right Chest'), lambda state: state.has('Small Key (Spirit Temple)', 3))
    set_rule(world.get_location('Spirit Temple First Mirror Left Chest'), lambda state: state.has('Small Key (Spirit Temple)', 3))
    set_rule(world.get_location('Spirit Temple Map Chest'), lambda state: state.has('Magic Meter') and (state.has('Dins Fire') or (state.has('Fire Arrows') and state.has('Bow') and state.has('Progressive Strength Upgrade', 2) and state.has('Small Key (Spirit Temple)', 3) and state.is_adult())))
    set_rule(world.get_location('Spirit Temple Child Climb East Chest'), lambda state: state.has('Bomb Bag') or ((state.has('Boomerang') or state.has('Slingshot')) and (state.has('Progressive Hookshot') or state.has('Bow'))) or (state.has('Small Key (Spirit Temple)', 3) and state.has('Progressive Strength Upgrade', 2) and state.is_adult() and (state.has('Progressive Hookshot') or state.has('Bow'))) or (state.has('Small Key (Spirit Temple)', 5) and state.has('Requiem of Spirit') and (state.has('Boomerang') or state.has('Slingshot'))))
    set_rule(world.get_location('Spirit Temple Child Climb North Chest'), lambda state: state.has('Bomb Bag') or ((state.has('Boomerang') or state.has('Slingshot')) and (state.has('Progressive Hookshot') or state.has('Bow'))) or (state.has('Small Key (Spirit Temple)', 3) and state.has('Progressive Strength Upgrade', 2) and state.is_adult() and (state.has('Progressive Hookshot') or state.has('Bow'))) or (state.has('Small Key (Spirit Temple)', 5) and state.has('Requiem of Spirit') and (state.has('Boomerang') or state.has('Slingshot'))))
    set_rule(world.get_location('Spirit Temple Sun Block Room Chest'), lambda state: (state.has('Small Key (Spirit Temple)', 5) and state.has('Bomb Bag') and state.has('Requiem of Spirit')) or (state.has_fire_source() and (state.has('Bomb Bag') or state.has('Small Key (Spirit Temple)', 2))))
    set_rule(world.get_location('Spirit Temple Statue Hand Chest'), lambda state: state.has('Small Key (Spirit Temple)', 3) and state.has('Progressive Strength Upgrade', 2) and state.is_adult() and state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Spirit Temple NE Main Room Chest'), lambda state: state.has('Small Key (Spirit Temple)', 3) and state.has('Progressive Strength Upgrade', 2) and state.is_adult() and state.has('Zeldas Lullaby') and state.has('Progressive Hookshot'))
    set_rule(world.get_location('Mirror Shield Chest'), lambda state: state.has('Small Key (Spirit Temple)', 4) and state.has('Progressive Strength Upgrade', 2) and state.is_adult())
    set_rule(world.get_location('Silver Gauntlets Chest'), lambda state: (state.has('Small Key (Spirit Temple)', 3) and state.has('Progressive Hookshot', 2)) or state.has('Small Key (Spirit Temple)', 5))
    set_rule(world.get_location('Spirit Temple Near Four Armos Chest'), lambda state: state.has('Mirror Shield'))
    set_rule(world.get_location('Spirit Temple Hallway Left Invisible Chest'), lambda state: state.has('Magic Meter') and state.has('Lens of Truth'))
    set_rule(world.get_location('Spirit Temple Hallway Right Invisible Chest'), lambda state: state.has('Magic Meter') and state.has('Lens of Truth'))
    set_rule(world.get_location('Spirit Temple Boss Key Chest'), lambda state: state.has('Zeldas Lullaby') and state.has('Bow') and state.has('Progressive Hookshot') and state.can_blast())
    set_rule(world.get_location('Spirit Temple Topmost Chest'), lambda state: state.has('Mirror Shield'))
    set_rule(world.get_location('Twinrova'), lambda state: state.has('Mirror Shield') and state.has('Bomb Bag') and state.has('Progressive Hookshot') and state.has('Boss Key (Spirit Temple)'))
    set_rule(world.get_location('Zelda'), lambda state: state.has('Shadow Medallion') and state.has('Spirit Medallion'))
    set_rule(world.get_entrance('Ganons Castle Light Trial'), lambda state: state.has('Progressive Strength Upgrade', 3))
    set_rule(world.get_entrance('Ganons Castle Tower'), lambda state: state.has('Forest Trial Clear') and state.has('Fire Trial Clear') and state.has('Water Trial Clear') and state.has('Shadow Trial Clear') and state.has('Spirit Trial Clear') and state.has('Light Trial Clear'))
    set_rule(world.get_location('Ganons Castle Forest Trial Clear'), lambda state: state.has('Magic Meter') and state.has('Bow') and state.has('Light Arrows') and (state.has('Fire Arrows') or (state.has('Progressive Hookshot') and state.has('Dins Fire'))))
    set_rule(world.get_location('Ganons Castle Fire Trial Clear'), lambda state: (state.has('Goron Tunic') or (state.has('Progressive Wallet') and state.has('Bomb Bag'))) and state.has('Progressive Strength Upgrade', 3) and state.has('Magic Meter') and state.has('Bow') and state.has('Light Arrows') and state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('Ganons Castle Water Trial Clear'), lambda state: state.has_bottle() and state.has('Hammer') and state.has('Magic Meter') and state.has('Bow') and state.has('Light Arrows'))
    set_rule(world.get_location('Ganons Castle Shadow Trial Clear'), lambda state: state.has('Magic Meter') and state.has('Bow') and state.has('Light Arrows') and state.has('Hammer') and (state.has('Fire Arrows') or state.has('Progressive Hookshot', 2)) and (state.has('Lens of Truth') or (state.has('Hover Boots') and state.has('Progressive Hookshot', 2))))
    set_rule(world.get_location('Ganons Castle Shadow Trial First Chest'), lambda state: (state.has('Magic Meter') and state.has('Bow') and state.has('Fire Arrows')) or state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('Ganons Castle Shadow Trial Second Chest'), lambda state: (state.has('Magic Meter') and state.has('Bow') and state.has('Fire Arrows')) or (state.has('Progressive Hookshot', 2) and state.has('Hover Boots')))
    set_rule(world.get_location('Ganons Castle Spirit Trial Clear'), lambda state: state.has('Magic Meter') and state.has('Bow') and state.has('Light Arrows') and state.has('Mirror Shield') and state.has('Bomb Bag') and state.has('Progressive Hookshot'))
    set_rule(world.get_location('Ganons Castle Spirit Trial First Chest'), lambda state: state.has('Progressive Hookshot') and (state.has('Magic Meter') or state.has('Bomb Bag')))
    set_rule(world.get_location('Ganons Castle Spirit Trial Second Chest'), lambda state: state.has('Progressive Hookshot') and state.has('Magic Meter') and state.has('Bomb Bag') and state.has('Lens of Truth'))
    set_rule(world.get_location('Ganons Castle Light Trial Clear'), lambda state: state.has('Magic Meter') and state.has('Bow') and state.has('Progressive Hookshot') and state.has('Light Arrows') and state.has('Small Key (Ganons Castle)', 2))
    set_rule(world.get_location('Ganons Castle Light Trail Invisible Enemies Chest'), lambda state: state.has('Magic Meter') and state.has('Lens of Truth'))
    set_rule(world.get_location('Ganons Castle Light Trial Lullaby Chest'), lambda state: state.has('Zeldas Lullaby') and state.has('Small Key (Ganons Castle)', 1))
    set_rule(world.get_location('Ganon'), lambda state: state.has('Boss Key (Ganons Castle)'))
    set_rule(world.get_entrance('Kokiri Forest Storms Grotto'), lambda state: state.has('Song of Storms'))
    set_rule(world.get_entrance('Lost Woods Generic Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Lost Woods Sales Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Front of Meadow Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Remote Southern Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Near Lake Inside Fence Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Valley Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field West Castle Town Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Far West Castle Town Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Kakariko Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field North Lon Lon Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Castle Storms Grotto'), lambda state: state.has('Song of Storms'))
    set_rule(world.get_entrance('Kakariko Bombable Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Mountain Bombable Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Mountain Storms Grotto'), lambda state: state.has('Song of Storms'))
    set_rule(world.get_entrance('Top of Crater Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Zora River Plateau Bombable Grotto'), lambda state: state.can_blast())
    set_rule(world.get_location('GS2'), lambda state: state.has_bottle())
    set_rule(world.get_location('GS3'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS4'), lambda state: state.has_bottle())
    set_rule(world.get_location('GS5'), lambda state: state.has_bottle())
    set_rule(world.get_location('GS6'), lambda state: state.has('Magic Bean'))
    set_rule(world.get_location('GS7'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS9'), lambda state: state.has('Slingshot') or state.has('Bomb Bag') or state.has('Boomerang') or (state.has('Dins Fire') and state.has('Magic Meter')))
    set_rule(world.get_location('GS11'), lambda state: state.has('Boomerang') and state.has('Bomb Bag'))
    set_rule(world.get_location('GS12'), lambda state: state.has('Boomerang') or (state.has('Progressive Hookshot') and state.is_adult()))
    set_rule(world.get_location('GS13'), lambda state: (state.has('Hammer') and state.has_fire_source() and state.has('Progressive Hookshot') and state.is_adult()) or (state.has('Boomerang') and state.has('Bomb Bag') and state.has('Dins Fire') and state.has('Magic Meter')))
    set_rule(world.get_location('GS16'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS20'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS21'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS26'), lambda state: state.has('Slingshot') or state.has('Bomb Bag'))
    set_rule(world.get_location('GS27'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS28'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS29'), lambda state: state.has_bottle())
    set_rule(world.get_location('GS30'), lambda state: state.has_bottle() and (state.has('Bomb Bag') or state.has('Progressive Strength Upgrade')))
    set_rule(world.get_location('GS31'), lambda state: state.can_blast())
    set_rule(world.get_location('GS32'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('GS33'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('GS34'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('GS35'), lambda state: state.is_adult())
    set_rule(world.get_location('GS37'), lambda state: state.has('Bolero of Fire') and state.has_bottle())
    set_rule(world.get_location('GS39'), lambda state: state.has('Bomb Bag') or (state.has('Boomerang') or state.has('Slingshot') and state.has('Progressive Strength Upgrade')) or (state.has('Dins Fire') and state.has('Magic Meter')) or (state.is_adult and (state.has('Progressive Hookshot') or state.has('Bow') or state.has('Biggoron Sword'))))
    set_rule(world.get_location('GS41'), lambda state: (state.has('Progressive Hookshot') and state.is_adult()) or (state.has('Boomerang') and (state.has('Bomb Bag') or state.has('Progressive Strength Upgrade'))))
    set_rule(world.get_location('GS42'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS45'), lambda state: state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS46'), lambda state: state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS47'), lambda state: state.has('Progressive Hookshot') or state.has('Bow') or state.has('Magic Meter'))
    set_rule(world.get_location('GS49'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS50'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.can_blast() and state.has('Progressive Hookshot'))
# Jabu Jabu GS need no reqs becuase the access reqs for their zones cover them.
    set_rule(world.get_location('GS55'), lambda state: state.has_bottle())
    set_rule(world.get_location('GS56'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS58'), lambda state: state.is_adult() and state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('GS59'), lambda state: state.is_adult() and state.has('Iron Boots') and state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS60'), lambda state: (state.has('Progressive Hookshot') or state.has('Bow') or (state.has('Dins Fire') and state.has('Magic Meter'))) and state.is_adult())
    set_rule(world.get_location('GS61'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS62'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS63'), lambda state: (state.has('Progressive Hookshot', 2) or (state.has('Progressive Hookshot') and state.can_reach('Forest Temple Outside Upper Ledge'))) and state.is_adult())
    set_rule(world.get_location('GS64'), lambda state: state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS65'), lambda state: state.has('Small Key (Fire Temple)', 1) and state.has('Song of Time'))
    set_rule(world.get_location('GS66'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('GS67'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS68'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS69'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('GS70'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS71'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS72'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS73'), lambda state: state.has('Bomb Bag') and state.has('Magic Meter'))
    set_rule(world.get_location('GS74'), lambda state: state.has('Song of Time') and state.has('Small Key (Water Temple)', 6))
    set_rule(world.get_location('GS75'), lambda state: state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('GS76'), lambda state: state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('GS77'), lambda state: state.has('Progressive Hookshot', 2) and ((state.has('Bomb Bag') and state.has('Progressive Strength Upgrade')) or state.has('Hover Boots')) and state.has('Small Key (Water Temple)', 6)) #5 keys would be better but it wouldn't be compatible with the key for key scenarios, 6 will be identical pre-keysanity.
    set_rule(world.get_location('GS78'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Boomerang') and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag') or (state.has('Lens of Truth') and state.has('Magic Meter'))))
    set_rule(world.get_location('GS79'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Boomerang'))
    set_rule(world.get_location('GS80'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Boomerang'))
    set_rule(world.get_location('GS81'), lambda state: state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS82'), lambda state: state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS84'), lambda state: state.has('Progressive Hookshot', 2) and state.has('Progressive Strength Upgrade') and state.has('Small Key (Shadow Temple)', 3))
    set_rule(world.get_location('GS86'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS87'), lambda state: state.has_bottle())
    set_rule(world.get_location('GS88'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS89'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS90'), lambda state: state.has('Progressive Hookshot') and state.has('Gerudo Membership Card') and state.is_adult())
    set_rule(world.get_location('GS92'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS93'), lambda state: state.has_bottle() and state.has('Requiem of Spirit'))
    set_rule(world.get_location('GS94'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS95'), lambda state: ((state.has('Magic Bean') and state.has('Requiem of Spirit')) or state.has('Progressive Hookshot', 2)) and state.is_adult())
    set_rule(world.get_location('GS96'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS98'), lambda state: (state.has('Boomerang') and state.has('Progressive Hookshot')) or (state.has('Boomerang') and state.has('Small Key (Spirit Temple)', 5) and state.has('Bomb Bag') and state.has('Requiem of Spirit')) or (state.has('Progressive Hookshot') and state.has('Progressive Strength Upgrade', 2) and state.is_adult() and state.has('Small Key (Spirit Temple)', 3)))
    set_rule(world.get_location('GS99'), lambda state: state.has('Song of Time') and (state.has('Bow') or state.has('Progressive Hookshot') or state.has('Bomb Bag')))
    set_rule(world.get_location('GS100'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.has('Small Key (Spirit Temple)', 3) and state.is_adult() and (state.has('Progressive Hookshot') or state.has('Hover Boots')))

    no_ice_traps = [
        'Darunias Joy',
        'Diving Minigame',
        'Child Fishing',
        'Adult Fishing',
        'Diving in the Lab',
        'Link the Goron',
        'King Zora Thawed',
        'Dog Lady',
        'Skull Kid',
        'Ocarina Memory Game',
        '10 Gold Skulltulla Reward',
        '20 Gold Skulltulla Reward',
        '30 Gold Skulltulla Reward',
        '40 Gold Skulltulla Reward',
        '50 Gold Skulltulla Reward',
        'Man on Roof',
        'Frog Ocarina Game',
        'Frogs in the Rain',
        'Horseback Archery 1000 Points',
        'Horseback Archery 1500 Points',
        'Child Shooting Gallery',
        'Adult Shooting Gallery',
        'Target in Woods',
        'Deku Theater Skull Mask',
        'Deku Theater Mask of Truth',
        'Anju as Adult',
        'Biggoron',
        'Anjus Chickens',
        'Talons Chickens',
        '10 Big Poes',
        'Rolling Goron as Child',
        'Hyrule Castle Fairy Reward',
        'Zoras Fountain Fairy Reward',
        'Desert Colossus Fairy Reward',
        'Zelda',
        'Bombchu Bowling Bomb Bag',
        'Bombchu Bowling Piece of Heart',
        'Deku Salesman Woods',
        'Deku Salesman Lost Woods Grotto',
        'Deku Salesman Hyrule Field Grotto',
        'Underwater Bottle',
    ]
    for location in no_ice_traps:
        forbid_item(world.get_location(location), 'Ice Trap')
