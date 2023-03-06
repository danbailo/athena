from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import AthenaBase, utcnow


class SubSectionModel(AthenaBase):
    sub_title_slug = Column(String, nullable=False, unique=True)
    sub_title = Column(String, nullable=False)
    sub_link_image = Column(String, nullable=True)
    sub_body = Column(String, nullable=False)
    sub_last_updated = Column(DateTime(), nullable=False, server_default=utcnow())

    section_id = Column(Integer, ForeignKey('section.id'))
    section = relationship('SectionModel', back_populates='subsections')


class SectionModel(AthenaBase):
    title_slug = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    last_updated = Column(DateTime(), nullable=False, server_default=utcnow())

    subsections = relationship('SubSectionModel', back_populates='section')
