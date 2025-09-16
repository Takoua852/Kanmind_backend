
from rest_framework import generics
from kanban_app.api.serializers import BoardSerializer, BoardCreateSerializer
from kanban_app.models import Board
from .permissions import  IsBoardMemberOrOwner

class BoardListView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsBoardMemberOrOwner]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer
    
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsBoardMemberOrOwner]
    serializer_class = BoardSerializer
