import liblo as lo

# create OSC server with port PORT
PORT = 3333



def init():
    bundle_box      = Box()
    server          = lo.Server( PORT, lo.UDP )
    server.add_method(
            path        = "/tuio/2Dcur",
            typespec    = None,
            func        = handle_tuio_2Dcur,
            user_data   = bundle_box)
    server.add_bundle_handlers(
            handle_bundle_start,
            handle_bundle_end,
            user_data   = bundle_box)
    return server



def handle_bundle_start( timestamp, bundle_box ):
    print( "bundle start", timestamp )
    bundle_box( Duct(
        fseq    = None,
        source  = None,
        timestamp = timestamp,
        alive   = list(),
        sets    = list(),
    ))

def handle_bundle_end( bundle_box ):
    bundle = bundle_box()
    alive = set( *bundle.alive )
    start = alive - tuio.objects
    stay  = alive & tuio.objects
    end   = tuio.objects - alive
    tuio.objects = alive
    sets  = bundle.sets
    for sid in end:
        print( "  end", sid )
    for sid in start:
        for aset in sets:
            if aset[0] == sid:
                print( "  start", *aset )
                break
    for sid in stay:
        for aset in sets:
            if aset[0] == sid:
                print( "  move", *aset )
                break
    print( "bundle end" )

def handle_tuio_2Dcur( path, args, typespec, address, bundle_box ):
    # there are profiles redefining methods
    # we only care for the 2D profile
    #  and check the typespec for that
    # see also http://tuio.org/?specification
    bundle = bundle_box()
    method = args[0]
    if False:
        pass
    elif method == "set" and typespec == 'sifffff':
        bundle.sets.append( args[1:] )
    elif method == "alive":
        bundle.alive.append( args[1:] )
    elif method == "fseq":
        bundle.fseq = args[1]
    elif method == "source":
        bundle.source = args[1]



def run_server( server ):
    while True:
        message = server.recv( 1 )
        if not message:
            continue

class Duct( dict ):
    def __getattr__( self, name ):
        return self[name]
    def __setattr__(self, name, value ):
        self[name] = value

class Box:
    def __init__( self ):
        self.value = None
    def __call__( self, value = None ):
        if value is not None:
            self.value = value
        return self.value

def main():
    global tuio
    tuio = Duct( objects = set() )
    server = init()
    run_server( server )

if __name__ == '__main__':
    main()
