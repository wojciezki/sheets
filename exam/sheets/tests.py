# Create your tests here.


from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from rest_framework.test import APIClient, APISimpleTestCase

from sheets.models import ExamSheet, Task, Solution, Answer

User = get_user_model()


class ExamViewsTest(APISimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        self.superuser = User.objects.create_superuser('adminadmin',
                                                       'adminadmin@admin.com',
                                                       'TajneHaslo',
                                                       id=12,
                                                       first_name='Test',
                                                       last_name='Nazwisko')

        self.exam_list_url = '/exam_sheets/'
        self.exams_list_url = '/exam_sheets/exams/'
        self.templates_list_url = '/exam_sheets/templates/'
        self.factory = RequestFactory()
        self.client = APIClient()
        self.request = self.factory.get('/')
        self.request.user = User.objects.get(pk=self.superuser.pk)

    def test_create_exam(self):
        start_amount = ExamSheet.objects.all().count()
        self.client.force_authenticate(self.superuser)
        response = self.client.post(self.exam_list_url, {"name": "exam_template",
                                                         "template": True})
        self.assertEqual(len(response.data.keys()), 8)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExamSheet.objects.all().count(), start_amount + 1)
        response = self.client.post(self.exam_list_url, {"name": "exam_template2",
                                                         "template": True})
        self.assertEqual(len(response.data.keys()), 8)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExamSheet.objects.all().count(), start_amount + 2)

    def test_list_exam(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get(self.exam_list_url)
        amount = len(response.data)
        self.assertEqual(len(response.data), amount)
        self.client.post(self.exam_list_url, {"name": "exam_template3",
                                              "template": True})
        response = self.client.get(self.exam_list_url)
        self.assertEqual(len(response.data), amount + 1)

    def test_exams_view(self):
        self.client.force_authenticate(self.superuser)
        start_amount = ExamSheet.objects.filter(template=False).count()
        response = self.client.get(self.exams_list_url)

        self.assertEqual(len(response.data), start_amount)

        self.client.post(self.exam_list_url, {"name": "exam1",
                                              "template": False})
        response = self.client.get(self.exams_list_url)
        self.assertEqual(len(response.data), start_amount + 1)

    def test_template_view(self):
        start_amount = ExamSheet.objects.filter(template=True).count()
        self.client.force_authenticate(self.superuser)
        response = self.client.get(self.templates_list_url)

        self.assertEqual(len(response.data), start_amount)

        self.client.post(self.exam_list_url, {"name": "exam1",
                                              "template": True})
        response = self.client.get(self.templates_list_url)
        self.assertEqual(len(response.data), start_amount + 1)


class TaskViewsTest(APISimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        self.superuser = User.objects.create_superuser('adminadmin',
                                                       'adminadmin@admin.com',
                                                       'TajneHaslo',
                                                       id=12,
                                                       first_name='Test',
                                                       last_name='Nazwisko')
        self.exam_sheet = ExamSheet.objects.create(template=True,
                                                   name='template1',
                                                   creator=self.superuser)

        self.task_list_url = '/tasks/'
        self.factory = RequestFactory()
        self.client = APIClient()
        self.request = self.factory.get('/')
        self.request.user = User.objects.get(pk=self.superuser.pk)

    def test_create_task(self):
        start_amount = Task.objects.all().count()
        self.client.force_authenticate(self.superuser)
        response = self.client.post(self.task_list_url, {"type": "MULTI_CHOICE",
                                                         "exam_sheet": self.exam_sheet.pk,
                                                         'question': "how old are you?"})

        self.assertEqual(len(response.data.keys()), 9)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.all().count(), start_amount + 1)
        response = self.client.post(self.task_list_url, {"type": "MULTI_CHOICE",
                                                         "exam_sheet": self.exam_sheet.pk,
                                                         'question': "task2?"})
        self.assertEqual(len(response.data.keys()), 9)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.all().count(), start_amount + 2)


class SolutionViewsTest(APISimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        self.superuser = User.objects.create_superuser('adminadmin',
                                                       'adminadmin@admin.com',
                                                       'TajneHaslo',
                                                       id=12,
                                                       first_name='Test',
                                                       last_name='Nazwisko')
        self.exam_sheet = ExamSheet.objects.create(template=True,
                                                   name='template1',
                                                   creator=self.superuser)
        self.task = Task.objects.create(type='MULTI_CHOICE',
                                        creator=self.superuser)
        self.task.exam_sheet.add(self.exam_sheet)

        self.solution_list_url = '/solutions/'
        self.factory = RequestFactory()
        self.client = APIClient()
        self.request = self.factory.get('/')
        self.request.user = User.objects.get(pk=self.superuser.pk)

    def test_create_solution(self):
        start_amount = Solution.objects.all().count()
        self.client.force_authenticate(self.superuser)
        response = self.client.post(self.solution_list_url, {"task": self.task.pk,
                                                             "text_answer": "response",
                                                             'choice_answer': False,
                                                             'points': 2})

        self.assertEqual(len(response.data.keys()), 5)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Solution.objects.all().count(), start_amount + 1)
        response = self.client.post(self.solution_list_url, {"task": self.task.pk,
                                                             "text_answer": "respo2nse",
                                                             'choice_answer': False,
                                                             'points': 2})
        self.assertEqual(len(response.data.keys()), 5)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Solution.objects.all().count(), start_amount + 2)


class AnswerViewsTest(APISimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        self.superuser = User.objects.create_superuser('adminadmin',
                                                       'adminadmin@admin.com',
                                                       'TajneHaslo',
                                                       id=12,
                                                       first_name='Test',
                                                       last_name='Nazwisko')
        self.exam_sheet = ExamSheet.objects.create(template=True,
                                                   name='template1',
                                                   creator=self.superuser)
        self.task = Task.objects.create(type='MULTI_CHOICE',
                                        creator=self.superuser)
        self.task.exam_sheet.add(self.exam_sheet)

        self.solution = Solution.objects.create(task=self.task,
                                                text_answer='answer',
                                                points=5,
                                                creator=self.superuser)
        self.solution2 = Solution.objects.create(task=self.task,
                                                 text_answer='answer',
                                                 points=5,
                                                 creator=self.superuser)

        self.answer_list_url = '/answers/'
        self.factory = RequestFactory()
        self.client = APIClient()
        self.request = self.factory.get('/')
        self.request.user = User.objects.get(pk=self.superuser.pk)

    def test_create_answer(self):
        start_amount = Answer.objects.all().count()
        self.client.force_authenticate(self.superuser)
        response = self.client.post(self.answer_list_url, {"task": self.task.pk,
                                                           "text_answer": "response",
                                                           'choice_answer': False,
                                                           'points': 2,
                                                           'submit': True,
                                                           'solution': self.solution.pk})

        self.assertEqual(len(response.data.keys()), 8)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Answer.objects.all().count(), start_amount + 1)
        response = self.client.post(self.answer_list_url, {"task": self.task.pk,
                                                           "text_answer": "response",
                                                           'choice_answer': False,
                                                           'points': 2,
                                                           'submit': True,
                                                           'solution': self.solution2.pk})
        self.assertEqual(len(response.data.keys()), 8)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Answer.objects.all().count(), start_amount + 2)


class TestAnswerModel(APISimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        self.superuser = User.objects.create_superuser('adminadmin',
                                                       'adminadmin@admin.com',
                                                       'TajneHaslo',
                                                       id=12,
                                                       first_name='Test',
                                                       last_name='Nazwisko')
        self.exam_sheet = ExamSheet.objects.create(template=True,
                                                   name='template1',
                                                   creator=self.superuser)
        self.task = Task.objects.create(type='MULTI_CHOICE',
                                        creator=self.superuser)
        self.task.exam_sheet.add(self.exam_sheet)

        self.solution = Solution.objects.create(task=self.task,
                                                text_answer='answer',
                                                points=5,
                                                creator=self.superuser,
                                                choice_answer=True)
        self.solution2 = Solution.objects.create(task=self.task,
                                                 text_answer='answer',
                                                 points=4,
                                                 creator=self.superuser,
                                                 choice_answer=False)
        self.answer = Answer.objects.create(task=self.task,
                                            text_answer='answer',
                                            creator=self.superuser,
                                            choice_answer=True,
                                            solution=self.solution,
                                            submit=True)
        self.answer2 = Answer.objects.create(task=self.task,
                                             text_answer='answer',
                                             creator=self.superuser,
                                             choice_answer=True,
                                             solution=self.solution2,
                                             submit=True)

    def test_calculate_grade(self):
        self.assertEqual(self.answer.calculated_grade, 5)
        self.assertEqual(self.answer2.calculated_grade, 0)


class TestExamSheetModel(APISimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        self.superuser = User.objects.create_superuser('adminadmin',
                                                       'adminadmin@admin.com',
                                                       'TajneHaslo',
                                                       id=12,
                                                       first_name='Test',
                                                       last_name='Nazwisko')
        self.exam_sheet = ExamSheet.objects.create(template=True,
                                                   name='template1',
                                                   creator=self.superuser)
        self.task = Task.objects.create(type='MULTI_CHOICE',
                                        creator=self.superuser)
        self.task.exam_sheet.add(self.exam_sheet)

        self.solution = Solution.objects.create(task=self.task,
                                                text_answer='answer',
                                                points=5,
                                                creator=self.superuser,
                                                choice_answer=True)
        self.solution2 = Solution.objects.create(task=self.task,
                                                 text_answer='answer',
                                                 points=4,
                                                 creator=self.superuser,
                                                 choice_answer=False)
        self.answer = Answer.objects.create(task=self.task,
                                            text_answer='answer',
                                            creator=self.superuser,
                                            choice_answer=True,
                                            solution=self.solution,
                                            submit=True)
        self.answer2 = Answer.objects.create(task=self.task,
                                             text_answer='answer',
                                             creator=self.superuser,
                                             choice_answer=True,
                                             solution=self.solution2,
                                             submit=True)

    def test_get_user_final_grade(self):
        final_grade = self.exam_sheet.get_user_final_grade(self.superuser)
        self.assertEqual(final_grade, 5)


class TestPermissions(APISimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        self.superuser = User.objects.create_superuser('adminadmin111',
                                                       'adminadmin@admin.com',
                                                       'TajneHaslo',
                                                       id=10,
                                                       first_name='Test',
                                                       last_name='Nazwisko')

        self.superuser2 = User.objects.create_superuser('adminadmin222',
                                                        'adminadmin2222@admin.com',
                                                        'TajneHaslo2',
                                                        id=12,
                                                        first_name='Test2',
                                                        last_name='Nazwisko2')
        self.exam_list_url = '/exam_sheets/'

    def test_permissions(self):
        self.client.force_authenticate(self.superuser)

        response = self.client.post(self.exam_list_url, {"name": "exam_template",
                                                         "template": True})
        self.client.force_authenticate(self.superuser2)

        status_code = self.client.delete(f'{self.exam_list_url}{response.data["id"]}/').status_code
        self.assertEqual(status_code, 403)

        status_code = self.client.patch(f'{self.exam_list_url}{response.data["id"]}/', data={'name': "ddd"}).status_code
        self.assertEqual(status_code, 403)

        status_code = self.client.get(f'{self.exam_list_url}{response.data["id"]}/').status_code
        self.assertEqual(status_code, 200)
