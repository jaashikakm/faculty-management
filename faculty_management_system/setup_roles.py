from django.contrib.auth.models import Group, Permission

roles = ["Faculty", "HOD", "Dean", "Director", "Principal"]
for role in roles:
    Group.objects.get_or_create(name=role)

print("Created/verified groups:", ", ".join(roles))
print("Create users in /admin/ and assign each user to the required group.")
