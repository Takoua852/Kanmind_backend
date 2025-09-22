from rest_framework import serializers
from kanban_app.models import Board
from users_auth_app.models import User
from tasks_app.models import Task


class BoardSerializer(serializers.ModelSerializer):
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
    title = serializers.CharField(required=True)  # <--- fix

    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        default=[]
    )

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
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

class TaskSerializer(serializers.ModelSerializer):
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
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]
        
    def get_tasks(self, obj):
        # Alle Tasks des Boards zurückgeben
        tasks = Task.objects.filter(board=obj)
        return TaskSerializer(tasks, many=True).data
  
    

class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    owner_data = BoardMemberSerializer(source="owner", read_only=True)
    members_data = BoardMemberSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "members", "owner_data", "members_data"]

    def update(self, instance, validated_data):
        members_ids = validated_data.pop("members", None)
        
        # Titel ändern
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        # Mitglieder aktualisieren (nur wenn übergeben)
        if members_ids is not None:
            instance.members.set(members_ids)

        return instance

class EmailCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]