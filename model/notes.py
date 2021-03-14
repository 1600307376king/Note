from main import db


class Notes(db.Model):
    __table_name__ = 'notes'
    note_id = db.Column(db.INT, primary_key=True, nullable=True, autoincrement=True)
    note_title = db.Column(db.String(255))
    note_labels = db.Column(db.String(255))
    note_instructions = db.Column(db.TEXT)
    note_content = db.Column(db.TEXT)
    creation_time = db.Column(db.String(255))
    click_number = db.Column(db.INT)

    def __init__(self, **kwargs):
        self.note_title = kwargs['note_title']
        self.note_labels = kwargs['note_labels']
        self.note_instructions = kwargs['note_instructions']
        self.note_content = kwargs['note_content']
        self.creation_time = kwargs['creation_time']
        self.click_number = kwargs['click_number']

    def __repr__(self):
        return 'note-id = {0}'.format(self.note_id)

    @property
    def pri_time(self):
        return self.creation_time
