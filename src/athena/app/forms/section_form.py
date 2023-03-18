from fastapi import Form

from .base import BaseForm, FormType


class CreateSectionForm(BaseForm):
    title: FormType[str]
    body: FormType[str]

    @classmethod
    def as_form(
        cls,
        title: str = Form(),
        body: str = Form()
    ) -> 'CreateSectionForm':
        return cls(
            title=title,
            body=body
        )


class UpdateSectionForm(BaseForm):
    title: FormType[str] | None
    body: FormType[str] | None

    @classmethod
    def as_form(
        cls,
        title: str | None = Form(None),
        body: str | None = Form(None)
    ) -> 'UpdateSectionForm':
        return cls(
            title=title,
            body=body
        )
