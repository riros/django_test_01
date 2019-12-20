from django.db.models import \
    UUIDField, Model, DateTimeField

import uuid


class BaseModel(Model):
    class Meta:
        abstract = True

    id = UUIDField(db_column='Id', primary_key=True, default=uuid.uuid4)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
