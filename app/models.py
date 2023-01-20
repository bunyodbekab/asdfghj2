from django.db import models

# Create your models here.

class Profile(models.Model):
    tid = models.IntegerField("TelegramID")
    state = models.CharField(max_length=30, default="start")
    dateCrate = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.phone}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

class Science(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    science = models.ForeignKey(Science, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    dateCrate = models.DateTimeField(auto_now_add=True)

    @property
    def created_time(self):
        return self.dateCrate.strftime("%Y/%m/%d, %H:%M")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.user.phone}"

    class Meta:
        verbose_name = "Topshirdi"
        verbose_name_plural = "Topshirdi"