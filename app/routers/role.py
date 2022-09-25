from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.oauth2 import require_user
from app.database import Role
from app.serializers.roleSerializers import roleEntity, rolesListEntity
from bson.objectid import ObjectId

router = APIRouter()


@router.get('/')
def get_roles():
    roles = rolesListEntity(Role.find())

    return {'status': 'success', 'results': len(roles), 'roles': roles}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_role(role: schemas.CreateRoleSchema, user_id: str = Depends(require_user)):
    role.user = ObjectId(user_id)
    role.created_at = datetime.utcnow()
    role.updated_at = role.created_at
    try:
        result = Role.insert_one(role.dict())
        new_role = roleEntity(Role.find_one({'_id': result.inserted_id}))
        return new_role
    except Exception as e:
        print(e)
        if e == 'MissingTokenError':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="MissingTokenError")
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Role with name: {role.name} already exists")