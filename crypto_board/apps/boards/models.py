from django.db import models

# Create your models here.
# class Board(models.Model):
#     name = models.CharField(max_length=200, blank=True, null=True)
#     owner
#     reference =
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

#     is_full_name_displayed = models.BooleanField(default=True)
#     bio = models.CharField(max_length=500, blank=True, null=True)
#     website = models.URLField(max_length=200, blank=True, null=True)
#     persona = models.ForeignKey(
#         UserPersona, on_delete=models.SET_NULL, blank=True, null=True
#     )
#     interests = models.ManyToManyField(UserInterest, blank=True)
