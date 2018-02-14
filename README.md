# pfsense_freeradius
Manage users in the pfsense freeradius plugin.

## List Users

```
$ python3 users.py list
user1
user2
aj1
aj2
```

## Add Single User

```
$ python users.py --username aj1 add
aj1	RIEL1S
```

## Bulk Add Users

```
$ python3 users.py --userfile ../users bulk_add
aj1	CEI3HB
aj2	DERG9B
```

## Delete Single User

```
$ python users.py --username aj1 del
```
