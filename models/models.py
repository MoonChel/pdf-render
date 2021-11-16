import uuid
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey

Base = declarative_base()


class AuditMixin:
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())


class File(Base, AuditMixin):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)
    processed = Column(Boolean, default=False)

    images = relationship("Image", back_populates="file")

    @classmethod
    def get_pk_name(self):
        return self.__tablename__ + ".id"


class Image(Base, AuditMixin):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)

    file_id = Column(
        UUID(as_uuid=True),
        ForeignKey(File.get_pk_name()),
    )
    file = relationship("File", back_populates="images")
