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



import math
def handle_bundle_start( timestamp, bundle_box ):
    # I can't handle the fractional part of the OSC timetag
    timestamp = lo.time()
    print( "bundle start", timestamp )
    bundle_box( Duct(
        fseq    = None,
        source  = None,
        timestamp = timestamp,
        start   = set(),
    ))

def handle_bundle_end( bundle_box ):
    print( "bundle end" )

def handle_tuio_2Dcur( path, args, typespec, address, bundle_box ):
    # there are profiles redefining methods
    # we only care for the 2D profile
    #  and check the typespec for that
    # see also http://tuio.org/?specification
    bundle = bundle_box()
    method = args[0]
    if method == "set" and typespec == 'sifffff':
        sid, x, y, X, Y, m = args[1:]
        if sid in bundle.start:
            print( "  start", sid )
            handle_touch_start( sid, bundle.timestamp, x, y )
        elif sid in tuio.objects:
            print( "  move", sid )
            handle_touch_move( sid, bundle.timestamp, x, y )
        else:
            print( "  set for dead", sid )
    elif method == "alive":
        alive = set( args[1:] )
        start = alive - tuio.objects
        end   = tuio.objects - alive
        for sid in end:
            print( "  end", sid )
            tuio.objects.remove( sid )
            handle_touch_end( sid, bundle.timestamp )
        for sid in start:
            print( "  alive start", sid )
            bundle.start.add( sid )
            tuio.objects.add( sid )
    elif method == "fseq":
        print( "  fseq", args[1] )
        bundle.fseq = args[1]
    elif method == "source":
        print( "  source", args[1] )
        bundle.source = args[1]



import recognition
recognizers = recognition.Recognizers()

def handle_touch_start( sid, time, x, y ):
    recognizers.touch_start( sid, time, x, y )

def handle_touch_move( sid, time, x, y ):
    recognizers.touch_move( sid, time, x, y )

def handle_touch_end( sid, time ):
    recognizers.touch_end( sid, time )



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
