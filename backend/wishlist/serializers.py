from rest_framework import serializers
from .models import Wishlist
from games.serializers import GameSerializer

class WishlistSerializer(serializers.ModelSerializer):
    game_details = GameSerializer(source='game', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'game', 'game_details', 'created_at']
        read_only_fields = ['id', 'created_at'] 