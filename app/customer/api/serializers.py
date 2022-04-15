from rest_framework import serializers

from customer.models import CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializes Customer Profile Object"""
    subscription_details = serializers.SerializerMethodField('get_subscription_detail')
    
    def get_subscription_detail(self, obj):
        from subscription.api.serializers import SubscriptionSerializer
        
        if obj.subscription:
            return SubscriptionSerializer(obj.subscription).data
        return None
    
    class Meta:
        model = CustomerProfile
        fields = "__all__"
        read_only_fields = ("user", "subscription", "total_check_ins", "remaining_check_ins")


class CustomerSubscriptionSerializer(serializers.ModelSerializer):
    """Serializes Customer Profile subscription"""
    subscription_details = serializers.SerializerMethodField('get_subscription_detail')
    
    def get_subscription_detail(self, obj):
        from subscription.api.serializers import SubscriptionSerializer
        
        if obj.subscription:
            return SubscriptionSerializer(obj.subscription).data
        return None
    
    class Meta:
        model = CustomerProfile
        fields = "__all__"
        read_only_fields = ("user", "description", "total_check_ins", "remaining_check_ins")
    
    def validate(self, attrs):
        subscription = attrs.get("subscription", None)
        if not subscription:
            raise serializers.ValidationError("Subscription is Required", 400)
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        subscription = validated_data.get("subscription")
        instance.remaining_check_ins += subscription.valid_for
        instance.save()
        return super().update(instance, validated_data)