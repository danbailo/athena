from enum import StrEnum


class EndPointEnum(StrEnum):
    user = 'user'
    auth = 'auth'
    home = 'home'
    admin = 'admin'


MAPPED_API_ENDPOINT_PREFIX = {
    EndPointEnum.admin: '/admin',
    EndPointEnum.auth: '/auth',
    EndPointEnum.user: '/user',
    EndPointEnum.home: ''
}
