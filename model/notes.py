from main import db


class Notes(db.Model):
    __table_name__ = 'notes'
    uuid = db.Column(db.String(36), primary_key=True, nullable=True)
    note_title = db.Column(db.String(255))
    note_labels = db.Column(db.String(255))
    note_instructions = db.Column(db.TEXT)
    note_content = db.Column(db.TEXT)
    creation_time = db.Column(db.String(255))
    click_number = db.Column(db.INT)

    def __init__(self, **kwargs):
        self.uuid = kwargs['uuid']
        self.note_title = kwargs['note_title']
        self.note_labels = kwargs['note_labels']
        self.note_instructions = kwargs['note_instructions']
        self.note_content = kwargs['note_content']
        self.creation_time = kwargs['creation_time']
        self.click_number = kwargs['click_number']

    @property
    def pri_time(self):
        return self.creation_time
