from django.db import models

class Library(models.Model):

    title = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length = 50, null=False)
    
    class Meta:
        verbose_name = ("library")
        verbose_name_plural = ("libraries")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("library_detail", kwargs={"pk": self.pk})
    