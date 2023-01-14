from enum import Enum


class EndPointEnum(str, Enum):
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
