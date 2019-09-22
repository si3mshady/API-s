#Device Registry Service

## Usage

All responses will have the form 

```json
{
  "data": "HTTP response code",
  "message": "Description of action taken"
}
``` 
### List all devices 

**Definition**
`GET /devices`

**Response**

- `200 OK` on success
```json
[

{
    "_id": "wifi-stereo",
    "name": "Stereo",
    "device_type": "sound-device",
    "device_controller": "192.168.10.4"
},

{
    "_id": "temp-control",
    "name": "Thermostat",
    "device_type": "temperature-controller",
    "device_controller": "192.168.10.5"
}
]
```
### Registering a new device

***Definition***
`POST /devices`

***Arguments***
- `"identifier":string` a unique identifier for the device
- `"name":string` a common name of the device
- `"device_type":string` description of the device
- `"network_address":string` the network address of the device's controller

**Response**

- `201 Created` on success

```json
{
    "_id": "wifi-stereo",
    "name": "Stereo",
    "device_type": "sound-device",
    "device_controller": "192.168.10.4"
}
```

## Lookup device details 

`GET /device/<identifer>`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
{
    "_id": "wifi-stereo",
    "name": "Stereo",
    "device_type": "sound-device",
    "device_controller": "192.168.10.4"
}
```

## Delete a device

**Definition**
`DELETE /devices/<identifier>`

**Responses**

- `404 Not Found` if the device does not exist
- `204 No Content`




