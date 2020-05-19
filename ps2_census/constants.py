from enum import Enum

CENSUS_ENDPOINT = "http://census.daybreakgames.com"
PUSH_ENDPOINT = "wss://push.planetside2.com/streaming"

SERVICE_ID_PREFIX = "s:"
EXAMPLE_SERVICE_ID = "example"


class Namespace(str, Enum):
    PS2 = "ps2"
    PS2_V1 = "ps2:v1"
    PS2_V2 = "ps2:v2"


class Verb(str, Enum):
    COUNT = "count"
    GET = "get"


class Collection(str, Enum):
    ABILITY = "ability"
    ABILITY_TYPE = "ability_type"
    ACHIEVEMENT = "achievement"
    ARMOR_FACING = "armor_facing"
    ARMOR_INFO = "armor_info"
    CHARACTER = "character"
    CHARACTERS_ACHIEVEMENT = "characters_achievement"
    CHARACTERS_CURRENCY = "characters_currency"
    CHARACTERS_DIRECTIVE = "characters_directive"
    CHARACTERS_DIRECTIVE_OBJECTIVE = "characters_directive_objective"
    CHARACTERS_DIRECTIVE_TIER = "characters_directive_tier"
    CHARACTERS_DIRECTIVE_TREE = "characters_directive_tree"
    CHARACTERS_EVENT = "characters_event"
    CHARACTERS_EVENT_GROUPED = "characters_event_grouped"
    CHARACTERS_FRIEND = "characters_friend"
    CHARACTERS_ITEM = "characters_item"
    CHARACTERS_LEADERBOARD = "characters_leaderboard"
    CHARACTERS_ONLINE_STATUS = "characters_online_status"
    CHARACTERS_SKILL = "characters_skill"
    CHARACTERS_STAT = "characters_stat"
    CHARACTERS_STAT_BY_FACTION = "characters_stat_by_faction"
    CHARACTERS_STAT_HISTORY = "characters_stat_history"
    CHARACTERS_WEAPON_STAT = "characters_weapon_stat"
    CHARACTERS_WEAPON_STAT_BY_FACTION = "characters_weapon_stat_by_faction"
    CHARACTERS_WORLD = "characters_world"
    CHARACTER_NAME = "character_name"
    CURRENCY = "currency"
    DIRECTIVE = "directive"
    DIRECTIVE_TIER = "directive_tier"
    DIRECTIVE_TREE = "directive_tree"
    DIRECTIVE_TREE_CATEGORY = "directive_tree_category"
    EFFECT = "effect"
    EFFECT_TYPE = "effect_type"
    EMPIRE_SCORES = "empire_scores"
    EVENT = "event"
    EXPERIENCE = "experience"
    EXPERIENCE_RANK = "experience_rank"
    FACILITY_LINK = "facility_link"
    FACILITY_TYPE = "facility_type"
    FACTION = "faction"
    FIRE_GROUP = "fire_group"
    FIRE_GROUP_TO_FIRE_MODE = "fire_group_to_fire_mode"
    FIRE_MODE = "fire_mode"
    FIRE_MODE_2 = "fire_mode_2"
    FIRE_MODE_TO_PROJECTILE = "fire_mode_to_projectile"
    FIRE_MODE_TYPE = "fire_mode_type"
    IMAGE = "image"
    IMAGE_SET = "image_set"
    IMAGE_SET_DEFAULT = "image_set_default"
    ITEM = "item"
    ITEM_ATTACHMENT = "item_attachment"
    ITEM_CATEGORY = "item_category"
    ITEM_PROFILE = "item_profile"
    ITEM_TO_WEAPON = "item_to_weapon"
    ITEM_TYPE = "item_type"
    LEADERBOARD = "leaderboard"
    LOADOUT = "loadout"
    MAP = "map"
    MAP_HEX = "map_hex"
    MAP_REGION = "map_region"
    MARKETING_BUNDLE = "marketing_bundle"
    MARKETING_BUNDLE_ITEM = "marketing_bundle_item"
    MARKETING_BUNDLE_WITH_ONE_ITEM = "marketing_bundle_with_1_item"
    METAGAME_EVENT = "metagame_event"
    METAGAME_EVENT_STATE = "metagame_event_state"
    OBJECTIVE = "objective"
    OBJECTIVE_SET_TO_OBJECTIVE = "objective_set_to_objective"
    OBJECTIVE_TYPE = "objective_type"
    OUTFIT = "outfit"
    OUTFIT_MEMBER = "outfit_member"
    OUTFIT_MEMBER_EXTENDED = "outfit_member_extended"
    OUTFIT_RANK = "outfit_rank"
    PLAYER_STATE = "player_state"
    PLAYER_STATE_GROUP = "player_state_group"
    PLAYER_STATE_GROUP_2 = "player_state_group_2"
    PROFILE = "profile"
    PROFILE_2 = "profile_2"
    PROFILE_ARMOR_MAP = "profile_armor_map"
    PROFILE_RESIST_MAP = "profile_resist_map"
    PROJECTILE = "projectile"
    PROJECTILE_FLIGHT_TYPE = "projectile_flight_type"
    REGION = "region"
    RESIST_INFO = "resist_info"
    RESIST_TYPE = "resist_type"
    RESOURCE_TYPE = "resource_type"
    REWARD = "reward"
    REWARD_GROUP_TO_REWARD = "reward_group_to_reward"
    REWARD_SET_TO_REWARD_GROUP = "reward_set_to_reward_group"
    REWARD_TYPE = "reward_type"
    SINGLE_CHARACTER_BY_ID = "single_character_by_id"
    SKILL = "skill"
    SKILL_CATEGORY = "skill_category"
    SKILL_LINE = "skill_line"
    SKILL_SET = "skill_set"
    TARGET_TYPE = "target_type"
    TITLE = "title"
    VEHICLE = "vehicle"
    VEHICLE_ATTACHMENT = "vehicle_attachment"
    VEHICLE_FACTION = "vehicle_faction"
    VEHICLE_SKILL_SET = "vehicle_skill_set"
    WEAPON = "weapon"
    WEAPON_AMMO_SLOT = "weapon_ammo_slot"
    WEAPON_DATASHEET = "weapon_datasheet"
    WEAPON_TO_ATTACHMENT = "weapon_to_attachment"
    WEAPON_TO_FIRE_GROUP = "weapon_to_fire_group"
    WORLD = "world"
    WORLD_EVENT = "world_event"
    WORLD_STAT_HISTORY = "world_stat_history"
    ZONE = "zone"
    ZONE_EFFECT = "zone_effect"
    ZONE_EFFECT_TYPE = "zone_effect_type"


class SearchModifier(str, Enum):
    CONTAINS = "*"
    GREATER = ">"
    GREATER_OR_EQUAL = "]"
    LESS = "<"
    LESS_OR_EQUAL = "["
    NOT = "!"
    STARTS_WITH = "^"


COMMAND_PREFIX = "c:"
FIELD_SEPARATOR = ","


class Command(str, Enum):
    CASE = "case"
    DISTINCT = "distinct"
    EXACT_MATCH_FIRST = "exactMatchFirst"
    HAS = "has"
    HIDE = "hide"
    INCLUDE_NULL = "includeNull"
    JOIN = "join"
    LANG = "lang"
    LIMIT = "limit"
    LIMIT_PER_DB = "limitPerDB"
    RETRY = "retry"
    SHOW = "show"
    SORT = "sort"
    START = "start"
    TIMING = "timing"
    TREE = "tree"


JOIN_ITEM_DELIMITER = "^"
JOIN_VALUE_DELIMITER = "'"


class JoinKey(str, Enum):
    HIDE = "hide"
    INJECT_AT = "inject_at"
    LIST = "list"
    ON = "on"
    OUTER = "outer"
    SHOW = "show"
    TERMS = "terms"
    TO = "to"


TREE_ITEM_DELIMITER = "^"


class TreeKey(str, Enum):
    FIELD = "field"
    LIST = "list"
    PREFIX = "prefix"
    START = "start"


class CharacterEvent(str, Enum):
    ACHIEVEMENT_EARNED = "AchievementEarned"
    BATTLE_RANK_UP = "BattleRankUp"
    DEATH = "Death"
    GAIN_EXPERIENCE = "GainExperience"
    ITEM_ADDED = "ItemAdded"
    PLAYER_FACILITY_CAPTURE = "PlayerFacilityCapture"
    PLAYER_FACILITY_DEFEND = "PlayerFacilityDefend"
    PLAYER_LOGIN = "PlayerLogin"
    PLAYER_LOGOUT = "PlayerLogout"
    SKILL_ADDED = "SkillAdded"
    VEHICLE_DESTROY = "VehicleDestroy"


class WorldEvent(str, Enum):
    CONTINENT_LOCK = "ContinentLock"
    CONTINENT_UNLOCK = "ContinentUnlock"
    FACILITY_CONTROL = "FacilityControl"
    METAGAME_EVENT = "MetagameEvent"
    PLAYER_LOGIN = "PlayerLogin"
    PLAYER_LOGOUT = "PlayerLogout"


class GenericEvent(str, Enum):
    ALL = "all"


class GenericCharacter(str, Enum):
    ALL = "all"


class EventStreamAction(str, Enum):
    SUBSCRIBE = "subscribe"
    ECHO = "echo"
    CLEAR_SUBSCRIBE = "clearSubscribe"
    RECENT_CHARACTER_IDS = "recentCharacterIds"
    RECENT_CHARACTER_IDS_COUNT = "recentCharacterIdsCount"


class EventStreamService(str, Enum):
    EVENT = "event"


class EventStreamWorld(str, Enum):
    JAEGER = "19"
    EMERALD = "17"
    CONNERY = "1"
    MILLER = "10"
    COBALT = "13"
    SOLTECH = "40"
    BRIGGS = "25"
    ALL = "all"
