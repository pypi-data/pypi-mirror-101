# pwbus-request

API to make request for PWBus.

Install:

```
$ pip3 install pwbus-request
```

Bootle request
```
@get('/ping')
def ping():
    print("PING (request)")
    sys.stdout.flush()
    try:
        pwbus = PwbusBootleRequest(
            request=request,
            response=response,
            channel="scarlet-web-channel", 
            task_id="pwbus.Pwbus_ping_task"
        )
        
        headers = pwbus.getHeaders()
        
        if pwbus.isRetry():
            payload = {}
        else:
            payload = {'value': 'PING'}
 
        resp = pwbus.post(payload, headers)
        return json.dumps({'success': True, 'data': resp["data"]})

    except:
        traceback.print_exc()
        sys.stdout.flush()
        return json.dumps({'success': False})
```

Flask request
```
TODO
```
