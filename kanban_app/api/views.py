
from rest_framework import generics, permissions
from kanban_app.api.serializers import BoardSerializer, BoardCreateSerializer
from kanban_app.models import Board


class BoardListView(generics.ListCreateAPIView):
    queryset = Board.objects.all()


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer
    
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
