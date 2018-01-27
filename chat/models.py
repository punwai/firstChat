from django.db import models
import json
from channels import Group


# Create your models here.
class Room(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default="")
    display_name = models.CharField(max_length=20, default="")
    @property
    def websocket_group(self):
        return Group("room-%s" % self.id)

    def send_message(self, message, user):
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username}

        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
