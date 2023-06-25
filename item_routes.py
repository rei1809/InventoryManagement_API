from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from models import User, Item
from schemas import ItemModel

session = Session(bind=engine)
item_router = APIRouter(
    prefix="/items",
    tags=['items']
)


@item_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):

    """
    ## A sample hello world route
    returns: a message: Hello
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token provided"
                            )

    return {"message": "Hello"}


@item_router.post("/item", status_code=status.HTTP_201_CREATED)
async def add_an_item(item: ItemModel, Authorize: AuthJWT = Depends()):
    """
    ## Create an item
        This requires the following
        ```
                quantity:int
                item_name:str
                item_type:str
        ```
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token provided"
                            )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(current_user == User.username).first()

    new_item = Item(
        quantity=item.quantity,
        item_name=item.item_name,
        item_type=item.item_type,

    )

    new_item.user = user
    session.add(new_item)
    session.commit()

    response = {
        "quantity": new_item.quantity,
        "item_name": new_item.item_name,
        "item_type": new_item.item_type
    }
    return jsonable_encoder(response)


@item_router.get('/items')
async def get_all_items(Authorize: AuthJWT = Depends()):
    """
        ## to get all items
        returns: Json object of all items
        """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token provided"
                            )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        items = session.query(Item).all()
        return jsonable_encoder(items)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User does not have access"
                        )

@item_router.get('/items/{item_id}')
async def retrieve_item_by_id(item_id:int,Authorize: AuthJWT=Depends()):
    """
    :param item_id:
    :param Authorize:
    :return: json object of that item
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token provided"
                            )

    order = session.query(Item).filter(Item.id == item_id).first()
    return jsonable_encoder(order)

@item_router.put("/item/update/{item_id}")
async def update_an_item(item_id: int,item: ItemModel,Authorize: AuthJWT=Depends()):
    """
    :param item_id:
    :param item:
    :param Authorize:
    :return: Updated Item object
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token provided"
                            )
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(current_user == User.username).first()
    if user.is_staff:
        item_to_update = session.query(Item).filter(Item.id == item_id).first()

        item_to_update.item_name = item.item_name
        item_to_update.quantity = item.quantity
        item_to_update.item_type = item.item_type

        session.commit()
        response = {
            "username": item_to_update.item_name,
            "email": item_to_update.quantity,
            "roles": item_to_update.item_type,
        }
        return jsonable_encoder(item_to_update)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User does not have the access!!"
                        )


@item_router.delete("/item/delete/{item_id}")
async def delete_item(item_id, Authorize: AuthJWT=Depends()):
    """
    :param item_id:
    :param Authorize:
    Deletes the item
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token provided"
                            )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(current_user == User.username).first()
    if user.is_staff:
        item_to_delete = session.query(Item).filter(Item.id == item_id).first()
        if item_to_delete:
            session.delete(item_to_delete)
            session.commit()

            return item_to_delete
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No item to delete!"
                            )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User not permitted to delete"
                            )