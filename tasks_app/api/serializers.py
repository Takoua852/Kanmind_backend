from rest_framework import serializers
from tasks_app.models import Task, Comment
from users_auth_app.models import User
from django.core.exceptions import ObjectDoesNotExist


class TaskUserSerializer(serializers.ModelSerializer):

    """
    Serializer for displaying basic user info for task assignee or reviewer.

    Fields:
    - id: User ID
    - email: User email
    - fullname: User full name
    """
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class TaskSerializer(serializers.ModelSerializer):

    """
    Serializer for Task objects.

    Fields:
    - id: Task ID
    - board: Board the task belongs to
    - title: Task title
    - description: Task description
    - status: Task status
    - priority: Task priority
    - assignee: Nested user info (read-only)
    - reviewer: Nested user info (read-only)
    - assignee_id: ID of the user to assign (write-only)
    - reviewer_id: ID of the reviewer (write-only)
    - due_date: Task due date
    - comments_count: Number of comments on this task
    """
    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            "id", "board", "title", "description", "status", "priority",
            "assignee", "reviewer", "assignee_id", "reviewer_id",
            "due_date", "comments_count"
        ]
    def get_comments_count(self, obj):
        """
        Returns the number of comments related to this task.
        """
        return obj.comments.count()


class TaskUpdateSerializer(serializers.ModelSerializer):
    
    """
    Serializer for updating a Task.

    Fields:
    - title: Task title
    - description: Task description
    - status: Task status
    - priority: Task priority
    - assignee: Nested user info (read-only)
    - reviewer: Nested user info (read-only)
    - assignee_id: ID of user to assign (write-only, optional, can be null)
    - reviewer_id: ID of user to review (write-only, optional, can be null)
    - due_date: Task due date

    Validation:
    - Assignee and reviewer must be members of the task's board.
    - Assignee/Reviewer IDs must exist in the database if provided.
    """

    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)

    assignee_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "title", "description", "status", "priority",
            "assignee", "reviewer", "assignee_id", "reviewer_id", "due_date"
        ]

    def validate(self, data):
        """
        Validate that assignee and reviewer are members of the board.
        """
        board = self.instance.board if self.instance else data.get("board")
        assignee_id = data.get("assignee_id")
        reviewer_id = data.get("reviewer_id")

        if assignee_id and not board.members.filter(id=assignee_id).exists():
            raise serializers.ValidationError(
                "Assignee muss Mitglied des Boards sein.")
        if reviewer_id and not board.members.filter(id=reviewer_id).exists():
            raise serializers.ValidationError(
                "Reviewer muss Mitglied des Boards sein.")
        return data

    def update(self, instance, validated_data):
        """
        Update Task instance with new data.
        Handles assigning/removing assignee and reviewer.
        """
        assignee_id = validated_data.pop("assignee_id", None)
        reviewer_id = validated_data.pop("reviewer_id", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if assignee_id is not None:
            if assignee_id:
                try:
                    instance.assignee = User.objects.get(id=assignee_id)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError("Assignee existiert nicht.")
            else:
                instance.assignee = None 
        
        if reviewer_id is not None:
            if reviewer_id:
                try:
                    instance.reviewer = User.objects.get(id=reviewer_id)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError("Reviewer existiert nicht.")
            else:
                instance.reviewer = None

        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment objects.

    Fields:
    - id: Comment ID
    - created_at: Timestamp when the comment was created
    - author: Full name of the comment author (read-only)
    - content: Comment text
    """
    author = serializers.CharField(source="author.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]


