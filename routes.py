import wheelman.core.router as router

router.add_routes(('handlers',
        ('private', (
                (r'^echo:\s+(?P<message>.+)\s*$', 'echo_verbose'),
        )),
        ('public', (
                (r'^echo:\s+(?P<message>.+)\s*$', 'echo'),
                (r'^(?P<name>[^\s]+):\s+(?P<message>.+)\s*$', 'targetted_public_message'),
        )),
        ('passive', (
                (r'^NOP$', 'nop'),
        )),
))
