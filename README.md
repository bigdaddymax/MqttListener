## MQTT listener

Very simple service that subscribes to and analyzes a couple of MQTT topics of IOT infra. The script listens to the topics and stores all messages into MySQL DB.

### Topics

 - `garage/buttons/b1`
 - `house/stairs/sensors/s1`

### Publishing

Messages from topic `house/stairs/sensors/s1` are analyzed and depending on the movement and illumination sends message to topic `house/stairs/switches/l1` to turn lights on or off.

Message to turn lights on:
```json
{"light": "on", "level":  30}
```
`level` - int in range 0 - 100 which represents the level of brightness of the LED.
