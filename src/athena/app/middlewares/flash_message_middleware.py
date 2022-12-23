class FlashMessageMiddleware:
    def __init__(self, app):
        self.app = app
        self._flash_message = None

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
                self._flash_message = flash_messages[0][1].decode('utf-8')
            else:
                self._flash_message = None

            await send(message)

        scope['athena_flash_message'] = self._flash_message

        await self.app(scope, receive, get_flash_message_from_headers)
