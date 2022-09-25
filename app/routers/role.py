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
            

@router.put('/{id}')
def update_role(id: str, payload: schemas.UpdateRoleSchema, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id: {id}")
    updated_role = Role.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_role:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No role with this id: {id} found')
    return roleEntity(updated_role)


@router.get('/{id}')
def get_role(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id: {id}")

    role = Role.find_one({'_id': ObjectId(id)})
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No role with this id: {id} found")
    return roleEntity(role)


@router.delete('/{id}')
def delete_role(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id: {id}")
    role = Role.find_one_and_delete({'_id': ObjectId(id)})
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No role with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
