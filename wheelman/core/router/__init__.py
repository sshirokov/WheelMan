from wheelman.core.handlers.default import log_message
import wheelman.settings as settings

DEFAULT_DISPATCH = (
    ('public', ()),
    ('private', ()),
    ('passive', (
            (r'^(?P<message>.+)$', log_message),
    )),
)

def add_route_to_section(section, route, cur_section):
    if cur_section[0] == section:
        return (section, cur_section[1] + (route,))
    else:
        return cur_section

if settings.DEBUG:
    print "Loading debug routes ...",
    from wheelman.core.handlers.default import debug_repl
    route = (r'^DEBUG::repl\(\)$', debug_repl)
    DEFAULT_DISPATCH = map(lambda cur_section: \
                               add_route_to_section('private', route, cur_section),
                           DEFAULT_DISPATCH)
    print "[OK]"
    
    
