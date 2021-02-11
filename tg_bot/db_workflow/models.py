from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData
metadata = MetaData()
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('tg_id', String),
    Column('tg_username', String)
    )

wishlist_table = Table(
    'wishlist_tablr', metadata,
    Column()
)
