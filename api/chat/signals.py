from django.dispatch import Signal, receiver
import time
update_last_message = Signal(providing_args=['request','user'])

@receiver(update_last_message)
def _update_last_message(sender, **kwargs):
    time.sleep(10)
    return True