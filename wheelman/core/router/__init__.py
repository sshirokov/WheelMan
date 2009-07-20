from wheelman.core.handlers.default import *
import wheelman.settings as settings

class RouterError(Exception): pass
class InvalidRouteHandler(RouterError): pass

DEFAULT_DISPATCH = (
    ('public', ()),
    ('private', ()),
    ('passive', (
            (r'^(?P<message>.+)$', log_message),
    )),
)

DEFAULT_DEBUG_DISPATCH = (
    ('private', (
            (r'^DEBUG::repl\(\)$', debug_repl),
            (r'^DEBUG::eval:\s+(?P<code>.+)\s*$', debug_eval),
            (r'^DEBUG::db::flush\(\)\s*$', debug_db_flush),
            (r'^DEBUG::db::flush\(\)\s*$', debug_db_commit),
    )),
    ('public', (
            (r'DEBUG::eval:\s+(?P<code>.+)\s*$', debug_eval),
    )),
)

def add_route_to_section(section, route, cur_section):
    if cur_section[0] == section:
        return (section, cur_section[1] + (route,))
    else:
        return cur_section

def resolve_path(base_path, path):
    return getattr(__import__(base_path), path)

def add_routes(route_spec):
    import wheelman.core.router as router
    base_path, section_specs = route_spec[0], route_spec[1:]
    def spec_to_route(section, secspec):
        print "spec_to_route:section:", section
        print "spec_to_route:secspec:", secspec
        route, handler = secspec
        if type(handler) in (str, unicode):
            print "Mapping handler: %s => %s(" % (route, "%s.%s" % (base_path, handler)),
            handler = resolve_path(base_path, handler)
            print handler, ")"
        elif callable(handler):
            print "Mapping callable handler: %s => %s" % (route, handler)
        else:
            raise InvalidRouteHandler("Invalid handler (%s) must be path or callable" % handler)
        return (route, handler)

    for section, specs in dict(section_specs).items():
        print "Building routes for section:", section
        print "Specs:", specs
        specs = map(lambda specs: spec_to_route(section, specs),
                    specs)
        print "Transformed specs:", specs
        for spec in specs:
            router.DISPATCH = map(lambda cur_section: \
                                      add_route_to_section(section, spec, cur_section),
                                  router.DISPATCH)
        
        
DISPATCH = DEFAULT_DISPATCH
if settings.DEBUG:
    print "Loading debug routes ...",
    for section, specs in dict(DEFAULT_DEBUG_DISPATCH).items():
        for spec in specs:
            print "Adding %s::spec(%s)" % (section, spec)
            DISPATCH = map(lambda cur_section: \
                               add_route_to_section(section, spec, cur_section),
                           DISPATCH)
    print "[OK]"
del(DEFAULT_DISPATCH)
    
    
