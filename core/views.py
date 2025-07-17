from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import random
import json

from .models import Business, Game, BusinessGame, GamePlay, Reward

@csrf_exempt
def play_game(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Sadece POST isteği kabul edilir.'}, status=405)

    try:
        data = json.loads(request.body)
        unique_code = data.get('unique_code')
        game_id = data.get('game_id')
        ip_address = data.get('ip_address')

        if not all([unique_code, game_id, ip_address]):
            return JsonResponse({'error': 'unique_code, game_id ve ip_address zorunludur.'}, status=400)

        # İşletme kontrolü
        try:
            business = Business.objects.get(unique_code=unique_code)
        except Business.DoesNotExist:
            return JsonResponse({"error": "İşletme bulunamadı."}, status=404)

        # IP adresi kontrolü
        if not is_ip_allowed(ip_address, business.network_ip_range):
            return JsonResponse({"error": "Bu IP adresi işletmenin ağına ait değil."}, status=403)

        # Günlük oyun hakkı kontrolü
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        play_count_today = GamePlay.objects.filter(
            ip_address=ip_address,
            business=business,
            timestamp__range=(today_start, today_end)
        ).count()

        if play_count_today >= business.daily_game_limit_per_ip:
            return JsonResponse({'error': 'Bu IP adresi bugün maksimum oyun hakkını kullanmıştır.'}, status=403)

        # Game ve BusinessGame kontrolü
        try:
            game = Game.objects.get(id=game_id)
            business_game = BusinessGame.objects.get(business=business, game=game)
        except Game.DoesNotExist:
            return JsonResponse({"error": "Oyun bulunamadı."}, status=404)
        except BusinessGame.DoesNotExist:
            return JsonResponse({"error": "İşletme bu oyunu sunmuyor."}, status=403)

        # Kazanma durumu
        won = random.random() < business_game.win_probability

        # Oyun kaydını oluştur
        gameplay = GamePlay.objects.create(
            business=business,
            game=game,
            ip_address=ip_address,
            result=won,
            timestamp=timezone.now()
        )

        # Yanıt verisi
        response_data = {
            'business': business.name,
            'game': game.name,
            'ip_address': ip_address,
            'result': 'Kazandı' if won else 'Kaybetti'
        }

        # Ödül varsa ekle
        if won:
            rewards = business_game.rewards.all()
            if rewards.exists():
                reward = random.choice(rewards)
                response_data['reward'] = {
                    'title': reward.title,
                    'description': reward.description
                }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Geçersiz JSON formatı.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'İşlem sırasında hata oluştu: {str(e)}'}, status=500)

# Yardımcı fonksiyon: IP kontrolü
def is_ip_allowed(ip, range_str):
    if range_str.endswith("*"):
        return ip.startswith(range_str[:-1])
    return ip == range_str
@csrf_exempt
def business_games(request, business_code):
    try:
        business = Business.objects.get(unique_code=business_code)
        games = BusinessGame.objects.filter(business=business).select_related('game')
        data = [{
            'game_id': bg.game.id,
            'game_name': bg.game.name,
            'win_probability': bg.win_probability
        } for bg in games]
        return JsonResponse(data, safe=False)
    except Business.DoesNotExist:
        return JsonResponse({"error": "Business not found"}, status=404)
