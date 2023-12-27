import json
from datetime import datetime


class MessageManager:
    def __init__(self):
        self.messageId = 0

    def create_message(self, step_id, action, message):
        self.messageId += 1
        timestamp = datetime.utcnow().isoformat() + "Z"

        messageToSend = {
            "step_id": step_id,
            "id": self.messageId,
            "timestamp": timestamp,
            "action": action,
            "message": message
        }
        return json.dumps(messageToSend)

    def get_message(self, json_message):
        try:
            message = json.loads(json_message)
            return message
        except json.JSONDecodeError:
            print("Erreur lors de l'analyse du message JSON")
            return None