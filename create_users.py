import os
import random
import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Talk, User

fakegen = Faker(["ja_JP"])

def create_users(n):
    users = [
        User(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]
    User.objects.bulk_create(users, ignore_conflicts=True)

    my_id = User.objects.get(username="admin").id

    user_ids = User.objects.exclude(id=my_id).values_list("id", flat=True)

    talks = []
    for _ in range(len(user_ids)):
        sent_talk = Talk(
            send_from=User.objects.get(id=my_id),
            send_to=User.objects.get(id=random.choice(user_ids)),
            message=fakegen.text(),
        )
        received_talk = Talk(
            send_from=User.objects.get(id=random.choice(user_ids)),
            send_to=User.objects.get(id=my_id),
            message=fakegen.text(),
        )
        talks.extend([sent_talk, received_talk])
    Talk.objects.bulk_create(talks, ignore_conflicts=True)

    talks = Talk.objects.order_by("-date")[: 2 * len(user_ids)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, fields=["date"])

if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(1000)
    print("done")