from rest_framework import serializers
from tasks_app.models import Task, Comment
from users_auth_app.models import User
from kanban_app.models import Board



class TaskUserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

class TaskSerializer(serializers.ModelSerializer):
    assignee = TaskUserSerilaizer(read_only=True)
    reviewer = TaskUserSerilaizer(read_only=True)
    comments_count = serializers.SerializerMethodField() 

    class Meta:
        model = Task
        fields = [
            "id", "board", "title", "description", "status", "priority",
            "assignee", "reviewer", "due_date", "comments_count"
        ]

    def get_comments_count(self, obj):
        return obj.comments.count() 
    
class TaskUpdateSerializer(serializers.ModelSerializer):

    assignee = TaskUserSerilaizer(read_only=True)
    reviewer = TaskUserSerilaizer(read_only=True)

    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "title", "description", "status", "priority",
            "assignee", "reviewer", "assignee_id", "reviewer_id", "due_date"
        ]

    def validate(self, data):
        board = self.instance.board if self.instance else data.get("board")
        assignee_id = data.get("assignee_id")
        reviewer_id = data.get("reviewer_id")
        
        # Prüfen, ob assignee/reviewer Mitglieder des Boards sind
        if assignee_id and not board.members.filter(id=assignee_id).exists():
            raise serializers.ValidationError("Assignee muss Mitglied des Boards sein.")
        if reviewer_id and not board.members.filter(id=reviewer_id).exists():
            raise serializers.ValidationError("Reviewer muss Mitglied des Boards sein.")
        return data
    
    def update(self, instance, validated_data):
        assignee_id = validated_data.pop("assignee_id", None)
        reviewer_id = validated_data.pop("reviewer_id", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if assignee_id is not None:
            instance.assignee = User.objects.get(id=assignee_id) if assignee_id else None
        if reviewer_id is not None:
            instance.reviewer = User.objects.get(id=reviewer_id) if reviewer_id else None

        instance.save()
        return instance

    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]



