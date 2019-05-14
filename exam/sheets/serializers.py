from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sheets.models import ExamSheet, Task, Answer, Solution


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'task', 'grade', 'choice_answer', 'text_answer', 'submit', 'solution', 'calculated_grade')
        read_only_fields = ('id',)

    def validate(self, attrs):
        if self.context['request'].method == 'POST' and attrs['task'] != attrs['solution'].task:
            raise ValidationError('you chose wrong solution')
        return attrs

    def validate_solution(self, solution):
        if solution.answer.filter(creator=self.context['request'].user).exists():
            raise ValidationError('You can not answer twice on the same solution')
        return solution

    def create(self, validated_data):
        answer = super().create(validated_data)
        if not ExamSheet.objects.filter(creator=self.context['request'].user, template=False).exists():
            self._create_exam_based_on_template(answer)
        else:
            self._add_task_to_existing_exam(answer)
        return answer

    def _create_exam_based_on_template(self, answer):
        template_exam = answer.task.exam_sheet.filter(template=True).first()
        template_exam.pk = None
        template_exam.template = False
        template_exam.save()
        template_exam.tasks.add(answer.task.id)
        template_exam.creator = self.context['request'].user
        template_exam.save()

    def _add_task_to_existing_exam(self, answer):
        exam_sheet = ExamSheet.objects.get(creator=self.context['request'].user, template=False)
        exam_sheet.tasks.add(answer.task.id)
        exam_sheet.save()


class SolutionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Solution
        fields = ('task', 'choice_answer', 'text_answer', 'answer', 'points')

    def validate(self, attrs):
        if attrs['task'].creator != self.context['request'].user:
            raise ValidationError('You can not create solution to task that is not yours')
        return attrs

    def validate_task(self, task):
        if task.type != Task.MULTI_CHOICE and task.related_solutions.all().exists():
            raise ValidationError('You cant assign more than two solutions to this type of task')
        return task


class TaskSerializer(serializers.ModelSerializer):
    related_solutions = SolutionSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'exam_sheet', 'created', 'edited', 'creator', 'editor', 'question', 'type', 'related_solutions')
        read_only_fields = ('id', 'created', 'edited', 'creator', 'editor')

    def validate(self, attrs):
        if attrs['exam_sheet'][0].creator != self.context['request'].user:
            raise ValidationError('You can not add task to template exam which is not yours.')
        if not attrs['exam_sheet'][0].template:
            raise ValidationError('You can not add task to exam which is not template.')
        return attrs


class ExamSheetSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = ExamSheet
        fields = ('id', 'created', 'edited', 'creator', 'editor', 'name', 'tasks', 'template')
        read_only_fields = ('id', 'created', 'edited', 'creator', 'editor', 'your_final_grade', 'tasks')

    def get_your_final_grade(self, obj):
        return obj.get_user_final_grade(self.context['request'].user)
