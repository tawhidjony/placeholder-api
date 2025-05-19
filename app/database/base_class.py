from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import MetaData

# Optional: naming convention helps Alembic generate consistent constraints
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)  # ✅ তুমি এখানে লেখো


@as_declarative()
class Base:
    metadata = metadata  # ✅ Base-এর metadata এটিই হওয়া উচিত

    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
