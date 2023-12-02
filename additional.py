import json


async def on_member_join(member):
    scratch_user_data = {
        "alts": [],
        "won_tourneys": [],
        "won_games": 0,
        "lost_games": 0
    }

    with open("users.json", "r") as users:
        users_data = json.load(users)

    users_data[str(member.id)] = scratch_user_data

    with open("users.json", "w") as users:
        users.write(json.dumps(users_data, indent=2))
