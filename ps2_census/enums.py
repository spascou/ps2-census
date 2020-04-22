from enum import IntEnum


class ArmorFacing(IntEnum):
    FRONT = 0
    RIGHT = 1
    TOP = 2
    REAR = 3
    LEFT = 4
    BOTTOM = 5
    ALL = 6


class FacilityType(IntEnum):
    AMP_STATION = 2
    BIO_LAB = 3
    TECH_PLANT = 4
    LARGE_OUTPOST = 5
    SMALL_OUTPOST = 6
    WARPGATE = 7
    INTERLINK_FACILITY = 8
    CONSTRUCTION_OUTPOST = 9
    RELIC_OUTPOST = 10


class Faction(IntEnum):
    VANU_SOVEREIGNTY = 1
    NEW_CONGLOMERATE = 2
    TERRAN_REPUBLIC = 3
    NS_OPERATIVES = 4


class FireModeType(IntEnum):
    PROJECTILE = 0
    IRON_SIGHT = 1
    MELEE = 3
    TRIGGER_ITEM_ABILITY = 8
    THROWN = 12


class ItemType(IntEnum):
    WEAPON = 26
    ATTACHMENT = 27
    VEHICLE_EQUIPMENT = 33
    INFANTRY_EQUIPMENT = 36
    IMPLANT = 45
    LEGACY_IMPLANT = 46


class ItemCategory(IntEnum):
    KNIFE = 2
    PISTOL = 3
    SHOTGUN = 4
    SMG = 5
    LMG = 6
    ASSAULT_RIFLE = 7
    CARBINE = 8
    AV_MAX_LEFT = 9
    AI_MAX_LEFT = 10
    SNIPER_RIFLE = 11
    SCOUT_RIFLE = 12
    ROCKET_LAUNCHER = 13
    HEAVY_WEAPON = 14
    FLAMETHROWER_MAX = 15
    FLAK_MAX = 16
    GRENADE = 17
    EXPLOSIVE = 18
    BATTLE_RIFLE = 19
    AA_MAX_RIGHT = 20
    AV_MAX_RIGHT = 21
    AI_MAX_RIGHT = 22
    AA_MAX_LEFT = 23
    CROSSBOW = 24


class MetagameEventState(IntEnum):
    STARTED = 135
    RESTARTED = 136
    CANCELED = 137
    ENDED = 138
    XP_BONUS_CHANGED = 139


class PlayerState(IntEnum):
    STANDING = 0
    CROUCHING = 1
    RUNNING = 2
    SPRINTING = 3
    FALLINH_LONG = 4
    CROUCH_WALKING = 5


class ProjectileFlightType(IntEnum):
    BALLISTIC = 1
    TRUE_BALLISTIC = 3
    DYNAMIC = 9
    PROXIMITY_DETONATE = 10


class ResistType(IntEnum):
    NONE = 0
    MELEE = 1
    SMALL_ARM = 2
    HEAVY_MACHINE_GUN = 4
    HEAVY_ANTI_ARMOR = 5
    EXPLOSIVE = 6
    TANK_SHELL = 7
    AIRCRAFT_MACHINE_GUN = 8
    ANTI_VEHICLE_MINE = 9
    FLAK_EXPLOSIVE_BLAST = 12
    ANTI_AIRCRAFT_MACHINE_GUN = 22
    AIR_TO_GROUND_WARHEAD = 23
    ARMOR_PIERCING_CHAIN_GUN = 28
    DEFAULT_ROCKET_LAUNCHER = 34
    ANTI_MATERIEL_RIFLE = 40
    WHALE_HUNTER = 45
    CORE_EXPLOSION = 46


class ResourceType(IntEnum):
    FUEL = 7
    HEAVY_SHIELD = 9
    CLOAKER_JUICE = 35
    MEDIC_FUEL = 38
    CORTIUM = 58
    AMBUSHER_FUEL = 75


class RewardType(IntEnum):
    ITEM = 1
    XP = 3


class TargetType(IntEnum):
    SELF = 1
    ANY = 2
    ENEMY = 3
    ALLY = 4


class Vehicle(IntEnum):
    FLASH = 1
    SUNDERER = 2
    LIGHTNING = 3
    MAGRIDER = 4
    VANGUARD = 5
    PROWLER = 6
    SCYTHE = 7
    REAVER = 8
    MOSQUITO = 9
    LIBERATOR = 10
    GALAXY = 11
    HARASSER = 12
    DROP_POD = 13
    VALKYRIE = 14
    ANT = 15


class World(IntEnum):
    JAEGER = 19
    EMERALD = 17
    CONNERY = 1
    MILLER = 10
    COBALT = 13
    SOLTECH = 40
    BRIGGS = 25
