from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    network_ip_range = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusinessGame(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    win_probability = models.FloatField(help_text="0.0 - 1.0 arası kazanma olasılığı")

    class Meta:
        unique_together = ('business', 'game')

    def __str__(self):
        return f"{self.business.name} - {self.game.name}"


class Reward(models.Model):
    business_game = models.ForeignKey(BusinessGame, on_delete=models.CASCADE, null=True, blank=True, related_name='rewards')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)  # geçici olarak nullable

    def __str__(self):
        return f"{self.title} ({self.business_game})"


class GamePlay(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, default=2)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    result = models.BooleanField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.business_game.business.name} - {self.business_game.game.name} - {'Kazandı' if self.result else 'Kaybetti'}"

