from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import News, Comment, Status, NewsStatus, CommentStatus


class NewsSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['author', 'created', 'updated']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'news', ]


class StatusNewsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = NewsStatus
        fields = "__all__"
        read_only_fields = ['author', 'news', 'status']

    def create(self, validated_data):
        status = get_object_or_404(Status, slug=validated_data['slug'])
        validated_data.pop('slug')
        validated_data['status'] = status
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            news_status = NewsStatus.objects.filter(**validated_data).first()
            if news_status:
                news_status.delete()
                raise serializers.ValidationError('У данного поста есть статус, текущий статус удален!')
            else:
                status = validated_data.pop('status')
                news_status = NewsStatus.objects.get(**validated_data)
                news_status.status = status
                news_status.save()
                instance = news_status
        return instance
