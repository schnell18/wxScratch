# coding=utf-8
import sys

from time import sleep
from model import Curriculum
from model import Exercise
from model import Lesson
from model import Resource


class MockCompositeRepo:

    def __init__(self, cfg):
        cfg['port'] = int(cfg.get('port', 3306))
        self.resource_repo = MockResourceRepo(cfg)
        self.exercise_repo = MockExerciseRepo(cfg)
        self.lesson_repo = MockLessonRepo(cfg, self.exercise_repo, self.resource_repo)
        self.curriculum_repo = MockCurriculumRepo(cfg, self.lesson_repo)


class MockBaseRepo:
    def __init__(self, cfg):
        self.config = cfg
        self.__cnx = None

    def save_or_update(self, obj):
        pass

class MockResourceRepo(MockBaseRepo):

    def __init__(self, cfg):
        MockBaseRepo.__init__(self, cfg)

    def check_exist(self, cursor, record):
        return 0

    def query_object(self, criteria):
        pass

    def insert_record(self, cursor, record):
        sleep(0.05)
        return 1

    def update_record(self, cursor, record):
        sleep(0.05)
        return 1

    def save_or_update(self, obj):
        sleep(0.05)
        return 1

class MockCurriculumRepo(MockBaseRepo):

    def __init__(self, cfg, lesson_repo):
        MockBaseRepo.__init__(self, cfg)
        self.lesson_repo = lesson_repo

    def check_exist(self, cursor, record):
        return 0

    def query_object(self, criteria):
        sleep(0.05)
        return 1

    def insert_record(self, cursor, record):
        sleep(0.05)
        return 1

    def update_record(self, cursor, record):
        sleep(0.05)
        return 1

    def save_or_update(self, obj):
        sleep(0.05)
        return 1

    def save_next_curricula(self, obj):
        sleep(0.05)
        return 1

    def save_related_data(self, obj, curriculum_id, cursor):
        sleep(0.05)
        return 1


class MockLessonRepo(MockBaseRepo):

    def __init__(self, cfg, exercise_repo, resource_repo):
        MockBaseRepo.__init__(self, cfg)
        self.exercise_repo = exercise_repo
        self.resource_repo = resource_repo

    def check_exist(self, cursor, record):
        return 0

    def query_object(self, criteria):
        return 1

    def insert_record(self, cursor, record):
        sleep(0.05)
        return 1

    def update_record(self, cursor, record):
        sleep(0.05)
        return 1

    def save_or_update(self, obj):
        sleep(0.05)
        return 1

    def save_related_data(self, obj, lesson_id, cursor):
        sleep(0.05)
        return 1

class MockExerciseRepo(MockBaseRepo):

    def __init__(self, cfg):
        MockBaseRepo.__init__(self, cfg)

    def check_exist(self, cursor, record):
        return 0

    def query_object(self, criteria):
        return 1

    def insert_record(self, cursor, record):
        sleep(0.05)
        return 1

    def update_record(self, cursor, record):
        sleep(0.05)
        return 1

    def save_or_update(self, obj):
        sleep(0.05)
        return 1

    def save_related_data(self, obj, exercise_id, cursor):
        sleep(0.05)
        return 1
