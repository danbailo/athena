from fastapi import Form

from pydantic import Field, root_validator

from .base import BaseForm, FormType


class LoginForm(BaseForm):
    """Is mandatory to return this fields.

    OAuth2PasswordRequestForm
        * grant_type
        * username
        * password
        * scopes
        * client_id
        * client_secret
    """

    username: FormType[str] = Field(..., alias='username', title='Usuário')
    password: FormType[str] = Field(..., alias='password', title='Senha')
    # remember_me: bool

    @classmethod
    def as_form(
        cls,
        username: str = Form(),
        password: str = Form(),
        # remember_me: bool = Form(False)
    ) -> 'LoginForm':
        return cls(
            username=username,
            password=password,
            # remember_me=remember_me
        )


class RegisterForm(BaseForm):
    name: FormType[str] = Field(..., title='Nome')
    email: FormType[str] = Field(..., title='E-mail')
    username: FormType[str] = Field(..., title='Usuário')
    password: FormType[str] = Field(..., title='Senha')
    password2: FormType[str] = Field(
        ..., title='Repita a senha', type='password'
    )

    @root_validator
    @classmethod
    def check_if_passwords_are_equal(cls, root):
        if root['password'] != root['password2']:
            raise ValueError('As senhas precisam ser iguais!')
        return root

    @classmethod
    def as_form(
        cls,
        name: str = Form(),
        email: str = Form(),
        username: str = Form(),
        password: str = Form(),
        password2: str = Form()
    ) -> 'RegisterForm':
        return cls(
            name=name,
            email=email,
            username=username,
            password=password,
            password2=password2
        )


class UpdateUserForm(BaseForm):
    name: FormType[str] | None
    email: FormType[str] | None
    username: FormType[str] | None

    @classmethod
    def as_form(
        cls,
        name: str | None = Form(None),
        email: str | None = Form(None),
        username: str | None = Form(None),
    ) -> 'UpdateUserForm':
        return cls(
            name=name,
            email=email,
            username=username,
        )
