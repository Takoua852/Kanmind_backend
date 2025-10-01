from rest_framework import serializers
from kanban_app.models import Board
from users_auth_app.models import User
from tasks_app.models import Task


class BoardSerializer(serializers.ModelSerializer):

    """
    Serialize a Board instance for list or read operations.

    Fields:
    - id: Board ID
    - title: Board title
    - member_count: Number of members in the board
    - ticket_count: Total number of tasks in the board
    - tasks_to_do_count: Number of tasks with status 'to-do'
    - tasks_high_prio_count: Number of tasks with high priority
    - owner_id: ID of the user who owns the board
    """
    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]

class BoardCreateSerializer(serializers.ModelSerializer):

    """
    Serializer for creating a new Board.

    - title: Board title (required)
    - members: List of user IDs to add as members (optional)
    
    The owner of the board is automatically set to the logged-in user.
    """
    title = serializers.CharField(required=True) 

    members = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False, default=[] )

    class Meta:
        model = Board
        fields = ["id", "title", "members"]

    def create(self, validated_data):
        members_ids = validated_data.pop("members", [])
        request = self.context.get("request")
        board = Board.objects.create(owner=request.user, title=validated_data["title"])
        if members_ids:
            board.members.set(members_ids)
        board.members.add(request.user)
        return board

    def to_representation(self, instance):
        return BoardSerializer(instance, context=self.context).data
    
class BoardMemberSerializer(serializers.ModelSerializer):

    """
    Serialize basic user info for board members or task assignees/reviewers.
    """
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

class TaskSerializer(serializers.ModelSerializer):

    """
    Serializer for Task objects.

    - assignee: Nested BoardMemberSerializer
    - reviewer: Nested BoardMemberSerializer
    - comments_count: Number of comments on the task
    """
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "priority",
                  "assignee", "reviewer", "due_date", "comments_count"]
        
    def get_comments_count(self, obj):
        return obj.comments.count()

class BoardDetailSerializer(serializers.ModelSerializer):

    """
    Detailed serializer for a Board, including members and tasks.

    - members: Nested BoardMemberSerializer (read-only)
    - tasks: List of tasks in this board (nested TaskSerializer)
    - owner_id: ID of the owner
    """
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]
        
    def get_tasks(self, obj):
        tasks = Task.objects.filter(board=obj)
        return TaskSerializer(tasks, many=True).data
  

class BoardUpdateSerializer(serializers.ModelSerializer):

    """
    Serializer for updating a Board.

    - members: List of user IDs to set as members
    - owner_data: Nested owner info (read-only)
    - members_data: Nested members info (read-only)
    """
    members = serializers.ListField( child=serializers.IntegerField(), write_only=True, required=False)
    owner_data = BoardMemberSerializer(source="owner", read_only=True)
    members_data = BoardMemberSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "members", "owner_data", "members_data"]

    def update(self, instance, validated_data):
        members_ids = validated_data.pop("members", None)
        
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        if members_ids is not None:
            instance.members.set(members_ids)

        return instance



class EmailCheckSerializer(serializers.ModelSerializer):

    """
    Serializer for checking if a user exists by email.
    """
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Kein User mit dieser E-Mail gefunden.")
        return value