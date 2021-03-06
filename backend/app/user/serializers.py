from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.db.models import Count
from django.utils import timezone

from rest_framework import  serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from app.generic.models import Image
from app.generic.serializers import ImageSerializer, ContentTypeField
from authenticate.serializers import EmailAddressSerializer
from authenticate.models  import EmailAddress

from .models import User, Address, Skill, WorkTime, Contract, Comment, Application

from middleware.user import CurrentUserDefault

class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):

    content_type = ContentTypeSerializer(many=False)

    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    
    permissions = PermissionSerializer(read_only=True, many=True)

    name = serializers.CharField(required=False, max_length=150)
 
    permission = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = Group
        fields = '__all__'

    def update(self, instance, validated_data):
        permission = validated_data.pop('permission', None)
        if permission is not None:
            if instance.permissions.filter(id=permission).exists():
                instance.permissions.remove(permission)
            else:
                instance.permissions.add(permission)

        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
 
    # groups = GroupSerializer(required=False, many=True)

    # is_active = serializers.BooleanField(required=False)

    # is_superuser = serializers.BooleanField(required=False)

    # first_name = serializers.CharField(required=False)

    # last_name = serializers.CharField(required=False)

    photo = VersatileImageFieldSerializer(required=False, allow_null=True, sizes='image_size')

    groups_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True, queryset=Group.objects.all())

    name = serializers.SerializerMethodField()

    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = (
            'password',
        )
    
    def get_name(self, obj):
        return obj.name

    def get_email(self, obj):
        try:
            email_address = obj.email_address.latest('join')
            serializers = EmailAddressSerializer(email_address, context=self.context)
            return serializers.data    
        except EmailAddress.DoesNotExist:
            return None
        

    # def get_photo(self, obj):
    #     photo = obj.images.all().filter(tag='photo').last()
    #     if photo:
    #         serializer = ImageSerializer(photo, context=self.context)
    #         return serializer.data
        
    def update(self, instance, validated_data):
        groups_id = validated_data.pop('groups_id', None)
        if groups_id is not None:
            for group in list(instance.groups.all()):
                instance.groups.remove(group)
                    
            for id in groups_id:
                instance.groups.add(id)

        return super().update(instance, validated_data)

class VisitSerializer(serializers.Serializer):

    service = serializers.IntegerField()
    
    count = serializers.IntegerField()

class ContractSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(default=serializers.CreateOnlyDefault(CurrentUserDefault()))

    contractID = serializers.SerializerMethodField()

    validity = serializers.SerializerMethodField()

    visits = serializers.SerializerMethodField()
    
    class Meta:
        model = Contract
        fields = '__all__'

    def get_contractID(self, obj):
        return obj.contractID

    def get_validity(self, obj):
        return timezone.now().strftime('%Y-%m-%d') >= obj.issue_date.strftime('%Y-%m-%d') and timezone.now().strftime('%Y-%m-%d') <= obj.expiry_date.strftime('%Y-%m-%d')

    def get_visits(self, obj):
        query = obj.order.all().values('service').annotate(count=Count('service'))
        serializer = VisitSerializer(instance=query, many=True)
        return serializer.data

class AddressSerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(default=serializers.CreateOnlyDefault(CurrentUserDefault()))

    title = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = '__all__'

    def get_title(self, obj):
        if obj.onMap:
            return obj.address

        return '%s / %s / %s / %s / %s' % (obj.city, obj.community, obj.street, obj.building, obj.roomNo)

    def update(self, instance, validated_data):
        defAddr = validated_data.get('defAddr', None)

        if defAddr:
            qs = Address.objects.filter(user_id=instance.user_id)
            for addr in qs:
                addr.defAddr = False
                addr.save()

        return super().update(instance, validated_data)

class SkillSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField()

    class Meta:
        model = Skill
        fields = '__all__'

class WorkTimeSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField()

    class Meta:
        model = WorkTime
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    content_type = ContentTypeField()

    image = VersatileImageFieldSerializer(required=False, allow_null=True, sizes='image_size')

    user = UserSerializer(read_only=True, many=False)

    user_id = serializers.IntegerField(default=serializers.CreateOnlyDefault(CurrentUserDefault()))

    child = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_child(self, obj):
        queryset = Comment.objects.filter(object_id=obj.id, content_type__model='comment')
        serializers = CommentSerializer(queryset, many=True, context=self.context)
        return serializers.data

class ApplicationSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    
    user_id = serializers.IntegerField(default=serializers.CreateOnlyDefault(CurrentUserDefault()))

    class Meta:
        model = Application
        fields = '__all__'