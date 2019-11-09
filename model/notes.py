from main import db


class Notes(db.Model):
    __table_name__ = 'notes'
    n_id = db.Column(db.INT, primary_key=True)
    uuid = db.Column(db.String)
    note_title = db.Column(db.String)
    note_labels = db.Column(db.String)
    note_instructions = db.Column(db.TEXT)
    note_content = db.Column(db.TEXT)
    creation_time = db.Column(db.String)

    def __init__(self, **kwargs):
        self.uuid = kwargs['uuid']
        self.note_title = kwargs['note_title']
        self.note_labels = kwargs['note_labels']
        self.note_instructions = kwargs['note_instructions']
        self.note_content = kwargs['note_content']
        self.creation_time = kwargs['creation_time']

    @property
    def pri_time(self):
        return self.creation_time
