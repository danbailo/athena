from typing import Any


from fastapi import Form

from pydantic import Field


from .base import BaseForm, StringType, BooleanType, IntegerType, DateTimeType


class CreateSectionForm(BaseForm):
    title: StringType = Field(
        ..., title='Título', placeholder='Título', required=True)
    body: StringType = Field(
        ..., tag='textarea', placeholder='Body', required=True)
    order_to_show: IntegerType = Field(
        ..., title='Ordem para mostrar', placeholder='Ordem para mostrar')
    visible: BooleanType = Field(..., title='Visível', placeholder='Visível')

    @classmethod
    def as_form(
        cls,
        title: str = Form(),
        body: str = Form(),
        visible: bool = Form(default=False),
        order_to_show: int = Form(default=0),
    ) -> 'CreateSectionForm':
        return cls(
            title=title,
            body=body,
            visible=visible,
            order_to_show=order_to_show
        )


class CreateSubSectionForm(BaseForm):
    sub_title: StringType = Field(
        ..., title='Título', placeholder='Título', required=True)
    sub_body: StringType = Field(
        ..., title='Body', tag='textarea', placeholder='Body', required=True)
    sub_link_image: StringType = Field(
        ..., title='Link', placeholder='Link', required=True)
    sub_order_to_show: IntegerType = Field(
        ..., title='Ordem para mostrar', placeholder='Ordem para mostrar')
    sub_visible: BooleanType = Field(
        ..., title='Visível', placeholder='Visível')

    @classmethod
    def as_form(
        cls,
        sub_title: str = Form(),
        sub_body: str = Form(),
        sub_link_image: str = Form(),
        sub_visible: bool = Form(default=False),
        sub_order_to_show: int = Form(default=0)
    ) -> 'CreateSubSectionForm':
        return cls(
            sub_title=sub_title,
            sub_body=sub_body,
            sub_link_image=sub_link_image,
            sub_visible=sub_visible,
            sub_order_to_show=sub_order_to_show
        )


class UpdateSectionForm(BaseForm):
    id: IntegerType = Field(None, title='ID', is_editable=False, disabled=True)

    title: StringType | None = Field(None, title='Título', disabled=True)
    title_slug: StringType = Field(
        None, title='Título slug', is_editable=False, disabled=True)

    body: StringType | None = Field(None, tag='textarea', disabled=True)
    visible: BooleanType | None = Field(None, title='Visível', disabled=True)
    order_to_show: IntegerType | None = Field(
        None, title='Ordem para mostrar', disabled=True)

    created_at: DateTimeType = Field(
        None, title='Criado em', is_editable=False, disabled=True)
    last_updated: DateTimeType = Field(
        None, title='Última atualização', is_editable=False, disabled=True)

    subsections: list[dict[str, Any]] = Field([], form_value=False)

    @classmethod
    def as_form(
        cls,
        title: str | None = Form(None),
        body: str | None = Form(None),
        visible: bool | None = Form(None),
        order_to_show: int | None = Form(None),
    ) -> 'UpdateSectionForm':
        return cls(
            title=title,
            body=body,
            visible=visible,
            order_to_show=order_to_show,
        )

    class Config:
        allow_population_by_field_name = True


class UpdateSubSectionForm(BaseForm):
    section_id: IntegerType = Field(
        None, title='ID da seção', is_editable=False, disabled=True)
    id: IntegerType = Field(
        None, title='ID da subseção', is_editable=False, disabled=True)

    sub_title: StringType | None = Field(
        None, title='Título da subseção', disabled=True)
    sub_title_slug: StringType = Field(
        None, title='Título slug da subseção', is_editable=False,
        disabled=True)
    sub_link_image: StringType | None = Field(
        None, title='Imagem da subseção', disabled=True)

    sub_body: StringType | None = Field(
        None, title='Body da subseção', tag='textarea', disabled=True)
    sub_visible: BooleanType | None = Field(
        None, title='Subseção visível', disabled=True)
    sub_order_to_show: IntegerType | None = Field(
        None, title='Ordem para mostrar a subseção', disabled=True)

    created_at: DateTimeType = Field(
        None, title='Subseção criada em', is_editable=False, disabled=True)
    sub_last_updated: DateTimeType = Field(
        None, title='Subseção atualizada em', is_editable=False, disabled=True)

    @classmethod
    def as_form(
        cls,
        sub_title: str | None = Form(None),
        sub_link_image: str | None = Form(None),
        sub_body: str | None = Form(None),
        sub_visible: bool | None = Form(None),
        sub_order_to_show: int | None = Form(None),
    ) -> 'UpdateSectionForm':
        return cls(
            sub_title=sub_title,
            sub_link_image=sub_link_image,
            sub_body=sub_body,
            sub_visible=sub_visible,
            sub_order_to_show=sub_order_to_show,
        )
