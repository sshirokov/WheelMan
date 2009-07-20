def log_message(meta, message):
    print "Logging: %s=>%s: %s" % (meta.event.source(), meta.event.target(), message)

def debug_repl(meta):
    import pdb; pdb.set_trace()
