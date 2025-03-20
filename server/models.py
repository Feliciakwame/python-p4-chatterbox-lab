from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, MetaData
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

gmt_plus_3 = pytz.timezone("Africa/Nairobi")
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    created_at = db.Column(
        DateTime(timezone=True),
        server_default=db.func.now(),
        default=datetime.now(gmt_plus_3),
    )
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=datetime.now(gmt_plus_3),
        default=datetime.now(gmt_plus_3),
    )