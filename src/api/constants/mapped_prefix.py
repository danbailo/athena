from enum import Enum


class EndPointEnum(str, Enum):
    user = 'user'
    auth = 'auth'


MAPPED_ENDPOINT_PREFIX = {
    EndPointEnum.user: '/user',
    EndPointEnum.auth: '/auth'
}
