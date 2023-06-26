from fastapi import Form

from pydantic import Field, root_validator

from .base import BaseForm, StringType


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

    username: StringType = Field(
        ..., title='Usuário', id='floatingInput', placeholder='Usuário',
        required=True)
    password: StringType = Field(
        ..., title='Senha', id='floatingInput', placeholder='Senha',
        type='password', required=True)
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
    name: StringType = Field(
        ..., title='Nome', id='floatingInput', placeholder='Nome',
        required=True)
    email: StringType = Field(
        ..., title='E-mail', id='floatingInput', placeholder='E-mail',
        type='email', required=True)
    username: StringType = Field(
        ..., title='Usuário', id='floatingInput', placeholder='Usuário',
        required=True)
    password: StringType = Field(
        ..., title='Senha', id='floatingInput', placeholder='Senha',
        type='password', required=True)
    password2: StringType = Field(
        ..., title='Repita a senha', type='password', id='floatingInput',
        placeholder='Repita a senha', required=True
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
    username: StringType | None = Field(
        None, title='Usuário', is_editable=False, disabled=True)
    name: StringType | None = Field(None, title='Nome', disabled=True)
    email: StringType | None = Field(None, title='E-mail', disabled=True)

    @classmethod
    def as_form(
        cls,
        name: str | None = Form(None),
        email: str | None = Form(None),
        # username: str | None = Form(None),
    ) -> 'UpdateUserForm':
        return cls(
            name=name,
            email=email,
            # username=username,
        )
