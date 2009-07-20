from wheelman.core.handlers.default import log_message

DEFAULT_DISPATCH = (
    ('public', ()),
    ('private', ()),
    ('passive', (
            (r'^(?P<message>.+)$', log_message),
    )),
)

