from rest_framework import serializers
from kanban_app.models import Board


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