from rest_framework import  serializers

from .models import Job
from middleware.user import CurrentUserDefault
from app.user.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):

    worker = UserSerializer(read_only=True)

    worker_id = serializers.IntegerField(default=serializers.CreateOnlyDefault(CurrentUserDefault()))

    jobID = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'

    def get_jobID(self, obj):
        return obj.jobID