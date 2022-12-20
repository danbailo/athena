from enum import Enum


class EndPointEnum(str, Enum):
    user = 'user'
    auth = 'auth'
    home = 'home'


MAPPED_API_ENDPOINT_PREFIX = {
    EndPointEnum.user: '/user',
    EndPointEnum.auth: '/auth',
    EndPointEnum.home: ''
}
