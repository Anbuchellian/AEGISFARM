import json


class MQTTBridge:
    def __init__(self, enabled: bool, broker: str, port: int, topic: str):
        self.enabled = enabled
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = None
        if enabled:
            try:
                import paho.mqtt.client as mqtt
                self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
                self.client.connect(broker, port, 30)
                self.client.loop_start()
            except Exception:
                self.client = None

    def publish(self, payload: dict) -> bool:
        if not self.client:
            return False
        self.client.publish(self.topic, json.dumps(payload), qos=1)
        return True
