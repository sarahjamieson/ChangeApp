from django.db import models


# have dates and users on all models
class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hub(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

