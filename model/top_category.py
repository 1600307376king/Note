from main import db


class TopCategory(db.Model):
    __table_name__ = 'top_category'
    uuid = db.Column(db.String(36), primary_key=True, nullable=True)
    top_category_name = db.Column(db.String(255), nullable=False, unique=True)
    sec_category = db.Column(db.Text)

    def __init__(self, **kwargs):
        self.uuid = kwargs['uuid']
        self.top_category_name = kwargs['top_category_name']
        self.sec_category = kwargs['sec_category']
