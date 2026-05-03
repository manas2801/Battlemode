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
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    xp_reward = models.IntegerField(default=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    proof_text = models.TextField(blank=True)
    proof_image = models.ImageField(upload_to='mission_proofs/', blank=True, null=True)

from datetime import date, timedelta

def approve_mission(self):
    if self.status != 'approved':
        player = self.player

        # XP logic
        player.xp += self.xp_reward

        while player.xp >= 100:
            player.level += 1
            player.xp -= 100

        # Health increase
        player.health = min(player.health + 5, 100)

        # 🔥 STREAK LOGIC
        today = date.today()

        if player.last_active_date == today:
            pass  # already counted today

        elif player.last_active_date == today - timedelta(days=1):
            player.streak += 1  # continue streak

        else:
            player.streak = 1  # reset streak

        player.last_active_date = today

        player.save()

        self.status = 'approved'
        self.save()

    def __str__(self):
        return self.title