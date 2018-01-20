from models import *
from table import Table
from table.columns import Column

class AlbumTable(Table):
    id = Column(field='id')
    name = Column(field='name')
    release_date = Column(field='release_date')
    class Meta:
        attrs = {'class': 'paleblue'}