##
#
#  This example gets pretty much everything that's to know about the TR TRAC-5 carbine.
#  Output is in the adjacent JSON file.
#
##

from ps2_census import Collection, Join, Query

# From item to fire mode
item_to_weapon_join: Join = (
    Join(Collection.ITEM_TO_WEAPON)
    .outer(0)
    .on("item_id")
    .to("item_id")
    .inject_at("item_to_weapon")
)

weapon_join: Join = (
    Join(Collection.WEAPON).outer(0).on("weapon_id").to("weapon_id").inject_at("weapon")
)


weapon_to_fire_group_join: Join = (
    Join(Collection.WEAPON_TO_FIRE_GROUP)
    .outer(0)
    .on("weapon_id")
    .to("weapon_id")
    .list(1)
    .inject_at("weapon_to_fire_groups")
)

fire_group_to_fire_mode_join: Join = (
    Join(Collection.FIRE_GROUP_TO_FIRE_MODE)
    .outer(0)
    .on("fire_group_id")
    .to("fire_group_id")
    .list(1)
    .inject_at("fire_group_to_fire_modes")
)


fire_mode_join: Join = (
    Join(Collection.FIRE_MODE_2)
    .outer(0)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode")
)

# From fire mode to projectile
fire_mode_to_projectile_join: Join = (
    Join(Collection.FIRE_MODE_TO_PROJECTILE)
    .outer(0)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode_to_projectile")
)

projectile_join: Join = Join(Collection.PROJECTILE).outer(0).inject_at("projectile")

# From fire mode to player state
player_state_group_join: Join = (
    Join(Collection.PLAYER_STATE_GROUP_2)
    .outer(0)
    .on("player_state_group_id")
    .to("player_state_group_id")
    .list(1)
    .inject_at("player_state_groups")
)

# From item to attachments and their effects
item_attachment_join: Join = (
    Join(Collection.ITEM_ATTACHMENT)
    .outer(0)
    .on("item_id")
    .to("item_id")
    .list(1)
    .inject_at("item_attachments")
    .nest(
        Join(Collection.ITEM)
        .outer(0)
        .on("attachment_item_id")
        .to("item_id")
        .inject_at("item")
        .nest(
            Join(Collection.ZONE_EFFECT)
            .outer(0)
            .on("passive_ability_id")
            .to("ability_id")
            .list(1)
            .inject_at("zone_effects")
            .nest(
                Join(Collection.ZONE_EFFECT_TYPE)
                .outer(0)
                .on("zone_effect_type_id")
                .to("zone_effect_type_id")
                .inject_at("zone_effect_type")
            )
        )
    )
)

# Weapon datasheet
weapon_datasheet_join: Join = (
    Join(Collection.WEAPON_DATASHEET)
    .outer(0)
    .on("item_id")
    .to("item_id")
    .inject_at("weapon_datasheet")
)

# Query
trac_5_query: Query = (
    Query(Collection.ITEM)
    .lang("en")
    .filter("name.en", "TRAC-5")
    .sort(("item_id", 1))
    .join(
        item_to_weapon_join.nest(
            weapon_join.nest(
                weapon_to_fire_group_join.nest(
                    fire_group_to_fire_mode_join.nest(
                        fire_mode_join.nest(player_state_group_join).nest(
                            fire_mode_to_projectile_join.nest(projectile_join)
                        )
                    )
                )
            )
        )
    )
    .join(item_attachment_join)
    .join(weapon_datasheet_join)
)


# Execute query and print results
if __name__ == "__main__":
    import json

    result: dict = trac_5_query.get()
    print(json.dumps(result, sort_keys=True, indent=2))
