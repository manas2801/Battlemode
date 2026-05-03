from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    health = models.IntegerField(default=100)
    streak = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    last_active_date = models.DateField(null=True, blank=True)  # 👈 add this
    def __str__(self):
        return self.user.username

class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    xp_reward = models.IntegerField(default=20)

    def __str__(self):
        return self.title


class MissionSubmission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    proof_text = models.TextField(blank=True)
    proof_image = models.ImageField(upload_to='mission_proofs/', blank=True, null=True)

    class Meta:
        unique_together = ('player', 'mission')

    def approve_submission(self):
        if self.status != 'approved':
            player = self.player
            player.xp += self.mission.xp_reward

            while player.xp >= 100:
                player.level += 1
                player.xp -= 100

            player.health = min(player.health + 5, 100)
            player.streak += 1
            player.save()

            self.status = 'approved'
            self.save()

    def __str__(self):
        return f"{self.player.user.username} - {self.mission.title}"