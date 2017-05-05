import requests, json

PORT_GESTURES = 49217

def touch_event( type_, id_, timestamp, x, y ):
    print( "touch_event", type_, id_, timestamp, x, y )
    touch = {
            "clientX": int(x * 600),
            "clientY": int(y * 400),
            "touchId": int(id_),
            "name": str(id_)
    }
    
    print( "POST touch", touch )
    response = requests.post(
            "http://127.0.0.1:49217/gestures/touches/",
            data = json.dumps( touch ))
    print( "response", response.headers, response.text )

    touch["id"] = response.headers["location"]
    touch["url"] = "/gestures/touches/" + touch["id"]

    touchgroup = {
            "timeStamp": int(timestamp),
            "type": str(type_),
            "touches": [ touch["id"] ]
    }

    print( "POST touchgroup", touchgroup )
    response = requests.post(
            "http://127.0.0.1:49217/gestures/touchgroups/",
            data = json.dumps( touchgroup ))
    print( "response", response.headers, response.text )

