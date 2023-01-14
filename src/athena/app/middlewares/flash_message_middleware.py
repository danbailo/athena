class FlashMessageMiddleware:
    def __init__(self, app):
        self.app = app
        self._flash_message: str | None = None

    @property
    def flash_message(self):
        return self._flash_message

    @flash_message.setter
    def flash_message(self, value):
        self._flash_message = value

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        async def get_flash_message_from_headers(message):
            if message['type'] != 'http.response.start':
                return await send(message)

            if flash_messages := list(filter(
                lambda x: x[0].decode('utf-8').lower()
                .startswith('x-athena-flash-message'),
                message.get('headers', []))
            ):
                self.flash_message = flash_messages[0][1].decode('utf-8')
            else:
                self.flash_message = None
            await send(message)

        scope['athena_flash_message'] = self.flash_message
        await self.app(scope, receive, get_flash_message_from_headers)
