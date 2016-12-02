


class Touch:

    def __init__( self, sid, time, x, y ):
        self.sid = sid
        self.stroke = [ TouchMove( time, x, y ) ]

    def move( self, time, x, y ):
        self.stroke.append( TouchMove( time, x, y ) )

    def age( self ):
        return self.stroke[-1].time - self.stroke[0].time

    def distance2_to_start( self ):
        start = self.stroke[0]
        last = self.stroke[-1]
        dx = last.x - start.x
        dy = last.y - start.y
        return dx*dx + dy*dy

class TouchMove:

    def __init__( self, time, x, y ):
        self.time = time
        self.x = x
        self.y = y



class Recognizers:

    def __init__( self ):
        self.touches = {}
        self.recognizers = [
            SingleFingerTap()
        ]

    def touch_start( self, sid, time, x, y ):
        touch = Touch( sid, time, x, y )
        event = Event( touch, self )
        self.touches[ sid ] = touch
        for recognizer in self.recognizers:
            recognizer.touch_start( event )
        
    def touch_move( self, sid, time, x, y ):
        touch = self.touches[ sid ]
        event = Event( touch, self )
        touch.move( time, x, y )
        for recognizer in self.recognizers:
            recognizer.touch_move( event )

    def touch_end( self, sid, time ):
        touch = self.touches[ sid ]
        event = Event( touch, self )
        touch.move( time, touch.stroke[-1].x, touch.stroke[-1].y )
        del self.touches[ sid ]
        for recognizer in self.recognizers:
            recognizer.touch_end( event )



class Event:

    def __init__( self, touch, recognizers ):
        self.touch = touch
        self.recognizers = recognizers

    def touches( self ):
        return self.recognizers.touches



class Recognizer:

    def __init__( self ):
        self.state = "idle"

    def state_possible( self ):
        self.state = "possible"

    def state_fail( self ):
        self.state = "idle"

    def state_detect( self ):
        if self.continous:
            self.state = "running"
        else:
            self.state = "idle"
        self.on_detected()

    def on_detected( self ):
        print( "!!!", type(self).__name__, "detected" )

class SingleFingerTap( Recognizer ):

    max_age = 0.3
    max_distance = 0.014
    max_distance2 = max_distance*max_distance
    continous = False

    def __init__( self ):
        super( SingleFingerTap, self ).__init__()

    def touch_start( self, event ):
        touches_n = len( event.touches() )
        if touches_n == 1:
            self.state_possible()
        elif touches_n > 1:
            self.state_fail()

    def touch_move( self, event ):
        if not self.state == "possible":
            return
        distance2 = event.touch.distance2_to_start()
        if distance2 > self.max_distance2:
            self.state_fail()
            print( "!!! SingleFingerTap moved too far" )

    def touch_end( self, event ):
        if not self.state == "possible":
            return
        if event.touch.age() < self.max_age:
            self.state_detect()
        else:
            self.state_fail()
            print( "!!! SingleFingerTap took too long" )



























