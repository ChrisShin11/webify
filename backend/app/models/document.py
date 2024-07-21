from tortoise import fields, models

class Document(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    file_path = fields.CharField(max_length=255)
    uploaded_at = fields.DatetimeField(auto_now_add=True)
    # uploaded_by = fields.ForeignKeyField('models.User', related_name='documents')

    def __str__(self):
        return self.title

    class Meta:
        table = "documents"