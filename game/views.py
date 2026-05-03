from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Mission, Player
from django.contrib import messages

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    player, created = Player.objects.get_or_create(user=request.user)

    missions = Mission.objects.filter(player=player)

    return render(request, 'home.html', {
        'player': player,
        'missions': missions
    })

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        Player.objects.create(user=user)

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def complete_mission(request, mission_id):
    if not request.user.is_authenticated:
        return redirect('login')

    player = Player.objects.get(user=request.user)
    mission = Mission.objects.get(id=mission_id, player=player)

    if not mission.completed:
        mission.completed = True
        mission.save()

        player.xp += mission.xp_reward

        if player.xp >= 100:
            player.level += 1
            player.xp -= 100

        player.health = min(player.health + 5, 100)
        player.streak += 1
        player.save()

    return redirect('home')

def submit_proof(request, mission_id):
    if not request.user.is_authenticated:
        return redirect('login')

    player = Player.objects.get(user=request.user)
    mission = Mission.objects.get(id=mission_id, player=player)

    if request.method == 'POST':
        mission.proof_text = request.POST.get('proof_text')
        mission.proof_image = request.FILES.get('proof_image')
        mission.status = 'submitted'
        mission.save()

        messages.success(request, "Proof submitted successfully! 🚀")

        return redirect('home')

    return render(request, 'submit_proof.html', {'mission': mission})

def missions_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    player, created = Player.objects.get_or_create(user=request.user)
    missions = Mission.objects.filter(player=player)

    return render(request, 'missions.html', {
        'player': player,
        'missions': missions
    })

def leaderboard_view(request):
    players = Player.objects.all().order_by('-level', '-xp')

    return render(request, 'leaderboard.html', {
        'players': players
    })

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    player, created = Player.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('avatar'):
            player.avatar = request.FILES.get('avatar')
            player.save()

    return render(request, 'profile.html', {'player': player})

from django.http import JsonResponse

def chat_view(request):
    return render(request, 'chat.html')

def chat_api(request):
    user_msg = request.GET.get('msg', '').lower()

    # Simple intelligent replies
    if "hello" in user_msg:
        reply = "Hey warrior ⚔ Keep grinding!"
    elif "xp" in user_msg:
        reply = "Complete missions and submit proof to earn XP."
    elif "streak" in user_msg:
        reply = "Stay consistent daily to increase streak 🔥"
    elif "job" in user_msg:
        reply = "Apply daily and keep improving your skills."
    else:
        reply = "Stay focused. Small progress daily = big success 🚀"

    return JsonResponse({'reply': reply})