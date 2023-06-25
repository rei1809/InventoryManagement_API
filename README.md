

Request type       | path                                   | Description                     | User access
------------------------------------------------------------------------------------------------------------
post               | /user/signup/                          | Register user                   | Not Staff
post               | /user/login/                           | User Login                      | Not Staff
post               | /items/item/                           | Add an item                     | Not Staff
put                | /items/item/update/{item_id}/          | Update an item                  | Staff User
delete             | /items/item/delete/{item_id}           | Delete an Item                  | Staff User
get                | /items/items                           | get all items                   | Staff User
get                | items/items/{item_id}                  | Retrieve an item                | Not Staff

