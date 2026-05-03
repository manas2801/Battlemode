from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse

from .models import Player, Mission, MissionSubmission


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    player, created = Player.objects.get_or_create(user=request.user)
    missions = Mission.objects.all()

    submissions = MissionSubmission.objects.filter(player=player)
    submission_dict = {sub.mission.id: sub for sub in submissions}

    return render(request, 'home.html', {
        'player': player,
        'missions': missions,
        'submission_dict': submission_dict
    })


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        Player.objects.create(user=user)

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def missions_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    player, created = Player.objects.get_or_create(user=request.user)
    missions = Mission.objects.all()

    submissions = MissionSubmission.objects.filter(player=player)
    submission_dict = {sub.mission.id: sub for sub in submissions}

    return render(request, 'missions.html', {
        'player': player,
        'missions': missions,
        'submission_dict': submission_dict
    })


def submit_proof(request, mission_id):
    if not request.user.is_authenticated:
        return redirect('login')

    player = get_object_or_404(Player, user=request.user)
    mission = get_object_or_404(Mission, id=mission_id)

    submission, created = MissionSubmission.objects.get_or_create(
        player=player,
        mission=mission
    )

    if request.method == 'POST':
        submission.proof_text = request.POST.get('proof_text', '')

        if request.FILES.get('proof_image'):
            submission.proof_image = request.FILES.get('proof_image')

        submission.status = 'submitted'
        submission.save()

        messages.success(request, "Proof submitted successfully. Waiting for admin approval.")
        return redirect('missions')

    return render(request, 'submit_proof.html', {
        'mission': mission,
        'submission': submission
    })


def leaderboard_view(request):
    players = Player.objects.all().order_by('-level', '-xp', '-streak')

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
            messages.success(request, "Profile image updated successfully.")

        return redirect('profile')

    return render(request, 'profile.html', {
        'player': player
    })


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'chat.html')


def chat_api(request):
    user_msg = request.GET.get('msg', '').lower()

    if "hello" in user_msg or "hi" in user_msg:
        reply = "Hey warrior ⚔ Keep grinding!"
    elif "xp" in user_msg:
        reply = "Complete missions and submit proof. XP is awarded only after admin approval."
    elif "streak" in user_msg:
        reply = "Your streak grows when you complete approved missions consistently."
    elif "mission" in user_msg:
        reply = "Go to Missions Arena, choose a mission, submit proof, and wait for approval."
    elif "job" in user_msg or "placement" in user_msg:
        reply = "Focus on resume, projects, aptitude, and daily applications. Small progress daily wins."
    elif "level" in user_msg:
        reply = "When XP reaches 100, your level increases and XP starts again from the remaining points."
    else:
        reply = "Stay focused. Complete one mission today and keep moving forward 🚀"

    return JsonResponse({'reply': reply})