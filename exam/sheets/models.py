from django.contrib.auth.models import AbstractUser
from django.db import models

from sheets.fields import RelatedNameField


class User(AbstractUser):
    pass


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    creator = RelatedNameField(User,
                               related_name="created_{underscore_name}s",
                               on_delete=models.CASCADE)
    editor = RelatedNameField(User,
                              related_name="edited_{underscore_name}s",
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)

    class Meta:
        abstract = True


class ExamSheet(BaseModel):
    template = models.BooleanField(default=True)
    name = models.CharField(max_length=256)

    def get_user_final_grade(self, user):
        answers = Answer.objects.filter(task__exam_sheet=self, creator=user)
        return sum([answer.calculated_grade for answer in answers])


class Task(BaseModel):
    MULTI_CHOICE = 'MULTI_CHOICE'
    TEXT = 'TEXT'
    TRUE_FALSE = 'TRUE_FALSE'

    TYPE_CHOICES = (
        (MULTI_CHOICE, 'Multi choice'),
        (TEXT, 'Text'),
        (TRUE_FALSE, 'True false choice')
    )

    type = models.CharField(choices=TYPE_CHOICES,
                            default='TEXT',
                            max_length=56)

    exam_sheet = models.ManyToManyField(ExamSheet,
                                        related_name='tasks')
    max_grade = models.IntegerField(null=True,
                                    default=None)
    question = models.TextField()

    def __str__(self):
        return f'{self.question}'


class BaseAnswer(BaseModel):
    task = RelatedNameField(Task,
                            related_name='related_{underscore_name}s',
                            on_delete=models.CASCADE)
    text_answer = models.TextField(null=True,
                                   default=None)

    choice_answer = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Solution(BaseAnswer):
    points = models.IntegerField(null=True,
                                 default=1)

    def __str__(self):
        return f'{self.text_answer}-{self.choice_answer}'


class Answer(BaseAnswer):
    class Meta:
        unique_together = (('creator', 'solution'),)

    submit = models.BooleanField(default=False)
    grade = models.IntegerField(null=True,
                                default=None)
    solution = models.ForeignKey(Solution,
                                 related_name='answer',
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)

    @property
    def calculated_grade(self):
        if self.choice_answer == self.solution.choice_answer and self.submit:
            return self.solution.points
        else:
            return 0
