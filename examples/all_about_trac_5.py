##
#
#  This example gets pretty much everything that's to know about the TR TRAC-5 carbine.
#  Output is in the adjacent JSON file.
#
##

from typing import Callable

from ps2_census import Collection, Join, Query

item_to_weapon_join_factory: Callable[[], Join] = (
    Join(Collection.ITEM_TO_WEAPON)
    .on("item_id")
    .to("item_id")
    .inject_at("item_to_weapon")
    .get_factory()
)

weapon_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon")
    .get_factory()
)

weapon_to_fire_group_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON_TO_FIRE_GROUP)
    .list(1)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon_to_fire_groups")
    .get_factory()
)

fire_group_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_GROUP)
    .on("fire_group_id")
    .to("fire_group_id")
    .inject_at("fire_group")
    .get_factory()
)

fire_group_to_fire_mode_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_GROUP_TO_FIRE_MODE)
    .list(1)
    .on("fire_group_id")
    .to("fire_group_id")
    .inject_at("fire_group_to_fire_modes")
    .get_factory()
)

fire_mode_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_MODE_2)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode")
    .get_factory()
)

fire_mode_to_damage_direct_effect_join_factory: Callable[[], Join] = (
    Join(Collection.EFFECT)
    .on("damage_direct_effect_id")
    .to("effect_id")
    .inject_at("damage_direct_effect")
    .nest(
        Join(Collection.EFFECT_TYPE)
        .on("effect_type_id")
        .to("effect_type_id")
        .inject_at("effect_type")
    )
    .get_factory()
)

fire_mode_to_damage_indirect_effect_join_factory: Callable[[], Join] = (
    Join(Collection.EFFECT)
    .on("damage_indirect_effect_id")
    .to("effect_id")
    .inject_at("damage_indirect_effect")
    .nest(
        Join(Collection.EFFECT_TYPE)
        .on("effect_type_id")
        .to("effect_type_id")
        .inject_at("effect_type")
    )
    .get_factory()
)

fire_mode_to_projectile_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_MODE_TO_PROJECTILE)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode_to_projectile")
    .get_factory()
)

projectile_join_factory: Callable[[], Join] = (
    Join(Collection.PROJECTILE).inject_at("projectile").get_factory()
)

player_state_group_join_factory: Callable[[], Join] = (
    Join(Collection.PLAYER_STATE_GROUP_2)
    .list(1)
    .on("player_state_group_id")
    .to("player_state_group_id")
    .inject_at("player_state_groups")
    .get_factory()
)

item_attachment_join_factory: Callable[[], Join] = (
    Join(Collection.ITEM_ATTACHMENT)
    .on("item_id")
    .to("item_id")
    .list(1)
    .inject_at("item_attachments")
    .nest(
        Join(Collection.ITEM)
        .on("attachment_item_id")
        .to("item_id")
        .inject_at("item")
        .nest(
            Join(Collection.ZONE_EFFECT)
            .on("passive_ability_id")
            .to("ability_id")
            .list(1)
            .inject_at("zone_effects")
            .nest(
                Join(Collection.ZONE_EFFECT_TYPE)
                .on("zone_effect_type_id")
                .to("zone_effect_type_id")
                .inject_at("zone_effect_type")
            )
        )
    )
    .get_factory()
)

weapon_datasheet_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON_DATASHEET)
    .on("item_id")
    .to("item_id")
    .inject_at("weapon_datasheet")
    .get_factory()
)

# Query
trac_5_query: Query = (
    Query(Collection.ITEM)
    .lang("en")
    .filter("name.en", "TRAC-5")
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(
                weapon_to_fire_group_join_factory().nest(
                    fire_group_join_factory().nest(
                        fire_group_to_fire_mode_join_factory().nest(
                            fire_mode_join_factory()
                            .nest(player_state_group_join_factory())
                            .nest(
                                fire_mode_to_projectile_join_factory().nest(
                                    projectile_join_factory()
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(
                weapon_to_fire_group_join_factory().nest(
                    fire_group_join_factory().nest(
                        fire_group_to_fire_mode_join_factory().nest(
                            fire_mode_join_factory().nest(
                                fire_mode_to_damage_direct_effect_join_factory()
                            )
                        )
                    )
                )
            )
        )
    )
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(
                weapon_to_fire_group_join_factory().nest(
                    fire_group_join_factory().nest(
                        fire_group_to_fire_mode_join_factory().nest(
                            fire_mode_join_factory().nest(
                                fire_mode_to_damage_indirect_effect_join_factory()
                            )
                        )
                    )
                )
            )
        )
    )
    .join(item_attachment_join_factory())
    .join(weapon_datasheet_join_factory())
)


# Execute query and print results
if __name__ == "__main__":
    import json

    result: dict = trac_5_query.get()
    print(json.dumps(result, sort_keys=True, indent=2))
