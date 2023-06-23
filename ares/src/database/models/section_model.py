from sqlalchemy import (
    Column, ForeignKey, String, Integer, DateTime, Boolean, false, text
)
from sqlalchemy.orm import relationship

from .base import AthenaBase, utcnow


class SubSectionModel(AthenaBase):
    sub_title_slug = Column(String, nullable=False, unique=True)
    sub_title = Column(String, nullable=False)
    sub_link_image = Column(String, nullable=True)
    sub_body = Column(String, nullable=False)
    sub_order_to_show = Column(
        Integer, nullable=False, server_default=text('0'))
    sub_visible = Column(Boolean, nullable=False, server_default=false())
    sub_last_updated = Column(DateTime(), nullable=False,
                              server_default=utcnow())
    section_id = Column(Integer, ForeignKey('section.id'))
    section = relationship('SectionModel', back_populates='subsections')


class SectionModel(AthenaBase):
    title_slug = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    visible = Column(Boolean, nullable=False, server_default=false())
    order_to_show = Column(Integer, nullable=False, server_default=text('0'))
    last_updated = Column(DateTime(), nullable=False, server_default=utcnow())

    subsections = relationship('SubSectionModel', back_populates='section')
