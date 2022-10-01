from main import ma


class SubjectSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("subject_id", "title", "credits", "description")


subject_schema = SubjectSchema()
subjects_schema = SubjectSchema(many=True)
