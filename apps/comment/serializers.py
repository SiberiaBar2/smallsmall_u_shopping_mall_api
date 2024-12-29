from apps.comment.models import Comment
from rest_framework import serializers

class CommentSerializers(serializers.ModelSerializer):
    # 没有这个会报错
    class Meta:
        model = Comment
        fields = "__all__"