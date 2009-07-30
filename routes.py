import wheelman.core.router as router

router.add_routes(('handlers',
        ('private', (
                (r'^echo:\s+(?P<message>.+)\s*$', 'echo_verbose'),
                (r'^admin$', 'admin'),
        )),
        ('public', (
                (r'^dance!$', 'dance'),
                (r'^echo:\s+(?P<message>.+)\s*$', 'echo'),
                (r"WheelMan: Who's on first?", 'first_post'),
        )),
        ('passive', (
                (r'^NOP$', 'nop'),
        )),
))
