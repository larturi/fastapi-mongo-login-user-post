
def roleEntity(role) -> dict:
    return {
        "id": str(role["_id"]),
        "name": role["name"],
        "description": role["description"],
        "user": str(role["user"]),
        "enabled": role["enabled"],
        "created_at": role["created_at"],
        "updated_at": role["updated_at"]
    }


def rolesListEntity(roles) -> list:
    return [roleEntity(role) for role in roles]
