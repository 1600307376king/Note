from main import db


class TopCategory(db.Model):
    __table_name__ = 'top_category'
    category_id = db.Column(db.INT, primary_key=True, nullable=True, autoincrement=True)
    top_category_name = db.Column(db.String(255), nullable=False, unique=True)
    sec_category = db.Column(db.Text)

    def __init__(self, **kwargs):
        self.top_category_name = kwargs['top_category_name']
        self.sec_category = kwargs['sec_category']

    def __repr__(self):
        return 'category_id {0}'.format(self.category_id)
