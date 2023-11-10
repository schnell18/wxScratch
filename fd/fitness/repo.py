# coding=utf-8
import sys

import mysql.connector
from mysql.connector import errorcode
from .model import Curriculum
from .model import Exercise
from .model import Lesson
from .model import Resource


class CompositeRepo:

    def __init__(self, cfg):
        cfg['port'] = int(cfg.get('port', 3306))
        self.resource_repo = ResourceRepo(cfg)
        self.exercise_repo = ExerciseRepo(cfg)
        self.lesson_repo = LessonRepo(cfg, self.exercise_repo, self.resource_repo)
        self.curriculum_repo = CurriculumRepo(cfg, self.lesson_repo)


class BaseRepo:
    def __init__(self, cfg):
        self.config = cfg
        self.__cnx = None

    def save_or_update(self, obj):
        pass

    def _save_or_update(self, obj, record, exist_func, insert_func, update_func, extra_func=None):
        cursor = None
        try:
            cnx = self.__connect()
            cursor = cnx.cursor()
            row_id = exist_func(cursor, record)
            if row_id > 0:
                update_func(cursor, record)
            else:
                row_id = insert_func(cursor, record)
            if extra_func:
                extra_func(obj, row_id, cursor)
            cnx.commit()
            return row_id
        except mysql.connector.Error as err:
            sys.stderr.write("Fail to persist data due to: %s" % (str(err),))
            raise
        finally:
            if cursor:
                cursor.close()

    def _do_exec(self, obj, exec_func):
        cursor = None
        try:
            cnx = self.__connect()
            cursor = cnx.cursor()
            exec_func(obj, cursor)
            cnx.commit()
        except mysql.connector.Error as err:
            sys.stderr.write("Fail to persist data due to: %s" % (str(err),))
            raise
        finally:
            if cursor:
                cursor.close()

    def _do_query(self, obj, query_func):
        cursor = None
        try:
            cnx = self.__connect()
            cursor = cnx.cursor(dictionary=True)
            return query_func(obj, cursor)
        except mysql.connector.Error as err:
            sys.stderr.write("Fail to query data due to: %s" % (str(err),))
            raise
        finally:
            if cursor:
                cursor.close()

    def __connect(self):
        try:
            if not self.__cnx:
                self.__cnx = mysql.connector.connect(**self.config)
            return self.__cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                sys.stderr.write("Something is wrong with your user name or password\n")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                sys.stderr.write("Database does not exist\n")
            else:
                sys.stderr.write(str(err))
            raise

    def __disconnect(self):
        try:
            if self.__cnx:
                self.__cnx.disconnect()
        except mysql.connector.Error as err:
            sys.stderr.write(err)


class ResourceRepo(BaseRepo):

    __sql_exist_res = '''
    select id from resource where name = %s
    '''

    __sql_query_by_uk = '''
    select id,
           name,
           url,
           size,
           checksum
      from resource
     where name = %(name)s
    '''

    __sql_insert_res = '''
    insert into resource(
      id           , name     , url         ,
      size         , checksum , gmt_created ,
      gmt_modified , version
    )
    values (
      %(id)s   , %(name)s     , %(url)s ,
      %(size)s , %(checksum)s , now()   ,
      now()    , 1
    )
    '''

    __sql_update_res = '''
    update resource
       set size         = %(size)s,
           url          = %(url)s,
           checksum     = %(checksum)s,
           gmt_modified = now(),
           version      = version + 1
     where name         = %(name)s
    '''

    def __init__(self, cfg):
        BaseRepo.__init__(self, cfg)

    def check_exist(self, cursor, record):
        cursor.execute(self.__sql_exist_res, (record['name'],))
        result = cursor.fetchone()
        return 0 if not result else result[0]

    def query_object(self, criteria):
        return self._do_query(criteria, self._query_object)

    def _query_object(self, criteria, cursor):
        cursor.execute(self.__sql_query_by_uk, criteria)
        rec = cursor.fetchone()
        if rec:
            return Resource(**rec)

    def insert_record(self, cursor, record):
        cursor.execute(self.__sql_insert_res, record)
        return cursor.lastrowid

    def update_record(self, cursor, record):
        cursor.execute(self.__sql_update_res, record)

    def save_or_update(self, obj):
        record = dict(obj.__dict__)
        return self._save_or_update(
            obj,
            record,
            self.check_exist,
            self.insert_record,
            self.update_record
        )


class CurriculumRepo(BaseRepo):

    __sql_clear_nc = '''
    delete
      from next_curriculum
     where curriculum_id = %(curriculum_id)s
    '''
    __sql_query_by_uk = '''
    select id            as id,
           title         as title,
           cover         as cover_tfs,
           preview_video as preview_video,
           icon          as icon_tfs,
           corner_label  as corner_label,
           description   as description,
           status        as status,
           reference_no  as ref_no,
           jump_url      as jump_url
      from curriculum
     where reference_no = %(ref_no)s
    '''

    __sql_insert_nc = '''
    insert into next_curriculum (
      curriculum_id , next_curriculum_id ,
      gmt_created   , gmt_modified       , version
    )
    values (
      %(curriculum_id)s , %(next_curriculum_id)s ,
      now()             , now()                  , 1
    )
    '''

    __sql_clear_cl = '''
    delete
      from curriculum_lesson
     where curriculum_id = %(curriculum_id)s
    '''

    __sql_insert_cl = '''
    insert into curriculum_lesson (
      id          , curriculum_id , seq_no   ,
      lesson_id   , lesson_title  , is_break ,
      gmt_created , gmt_modified  , version
    )
    values (
      null          , %(curriculum_id)s , %(seq_no)s   ,
      %(lesson_id)s , %(lesson_title)s  , %(is_break)s ,
      now()         , now()             , 1
    )
    '''

    __sql_clear_le = '''
    delete from lesson_exercise where lesson_id = %(lesson_id)s
    '''

    __sql_exist_res = '''
    select id from curriculum where reference_no = %s
    '''

    __sql_insert_res = '''
    insert into curriculum(
      id            , title       , cover        ,
      preview_video , icon        , corner_label ,
      description   , status      , reference_no ,
      jump_url      , gmt_created , gmt_modified ,
      version
    )
    values (
      null              , %(title)s    , %(cover_tfs)s         ,
      %(preview_video)s , %(icon_tfs)s , %(corner_label_type)s ,
      %(description)s   , 2            , %(ref_no)s            ,
      %(jump_url)s      , now()        , now()                 ,
      1
    )
    '''

    __sql_update_res = '''
    update curriculum
       set title         = %(title)s,
           cover         = %(cover_tfs)s,
           preview_video = %(preview_video)s,
           icon          = %(icon_tfs)s,
           corner_label  = %(corner_label_type)s,
           description   = %(description)s,
           jump_url      = %(jump_url)s,
           gmt_modified  = now(),
           version       = version + 1
     where reference_no  = %(ref_no)s
    '''

    def __init__(self, cfg, lesson_repo):
        BaseRepo.__init__(self, cfg)
        self.lesson_repo = lesson_repo

    def check_exist(self, cursor, record):
        cursor.execute(self.__sql_exist_res, (record['ref_no'],))
        result = cursor.fetchone()
        return 0 if not result else result[0]

    def query_object(self, criteria):
        return self._do_query(criteria, self._query_object)

    def _query_object(self, criteria, cursor):
        cursor.execute(self.__sql_query_by_uk, criteria)
        rec = cursor.fetchone()
        if rec:
            return Curriculum(**rec)

    def insert_record(self, cursor, record):
        cursor.execute(self.__sql_insert_res, record)
        return cursor.lastrowid

    def update_record(self, cursor, record):
        cursor.execute(self.__sql_update_res, record)

    def save_or_update(self, obj):
        record = dict(obj.__dict__)
        record.pop("next_curricula_refs", None)
        record.pop("next_curricula", None)
        record.pop("curriculum_lessons", None)
        return self._save_or_update(
            obj,
            record,
            self.check_exist,
            self.insert_record,
            self.update_record,
            self.save_related_data
        )

    def save_next_curricula(self, obj):
        self._do_exec(obj, self._save_next_curricula)

    def _save_next_curricula(self, obj, cursor):
        curriculum_id = self.check_exist(cursor, {'ref_no': obj.ref_no})
        next_curricula = obj.next_curricula
        cursor.execute(self.__sql_clear_nc, {'curriculum_id': curriculum_id})
        if next_curricula:
            for nc in next_curricula:
                rec = {
                    'curriculum_id': curriculum_id,
                    'next_curriculum_id': self.check_exist(cursor, {'ref_no': nc.ref_no})
                }
                cursor.execute(self.__sql_insert_nc, rec)

    def save_related_data(self, obj, curriculum_id, cursor):
        curriculum_lessons = obj.curriculum_lessons
        cursor.execute(self.__sql_clear_cl, {'curriculum_id': curriculum_id})
        if curriculum_lessons:
            for seq_no, cl in enumerate(curriculum_lessons, 1):
                rec = dict(cl.__dict__)
                lesson_id = None
                if cl.lesson_ref:
                    lesson_id = self.lesson_repo.check_exist(cursor, {'ref_no': cl.lesson_ref})
                rec['seq_no'] = seq_no
                rec['lesson_id'] = lesson_id
                rec['curriculum_id'] = curriculum_id
                cursor.execute(self.__sql_insert_cl, rec)


class LessonRepo(BaseRepo):

    __sql_clear_lr = '''
    delete
      from lesson_resource
     where lesson_id = %(lesson_id)s
    '''
    __sql_query_by_uk = '''
    select id             as id,
           type           as type,
           title          as title,
           bg_music       as bg_music,
           description    as description,
           encouragement  as encouragement,
           next_day_intro as next_day_intro,
           reference_no   as ref_no
      from lesson
     where reference_no = %(ref_no)s
    '''

    __sql_insert_lr_rec = '''
    insert into lesson_resource(
      id          , lesson_id    , resource_id ,
      gmt_created , gmt_modified , version
    )
    values (
      null  , %(lesson_id)s , %(resource_id)s ,
      now() , now()         , 1
    )
    '''

    __sql_clear_bv = '''
    delete t1
      from lesson_exercise_audio t1
     inner join lesson_exercise t2 on (t1.le_id = t2.id)
     where t2.lesson_id = %(lesson_id)s
    '''

    __sql_insert_bv = '''
    insert into lesson_exercise_audio (
      id           , type     , le_id       ,
      audio_name   , position , gmt_created ,
      gmt_modified , version
    )
    select null                , %(type)s     , id    ,
           %(audio_name_base)s , %(position)s , now() ,
           now()               , 1
      from lesson_exercise
     where exercise_id = %(exercise_id)s
       and lesson_id = %(lesson_id)s
       and seq_no = %(seq_no)s
    '''

    __sql_clear_le = '''
    delete from lesson_exercise where lesson_id = %(lesson_id)s
    '''

    __sql_insert_le = '''
    insert into lesson_exercise(
      lesson_id    , exercise_id , repetition  ,
      measure      , seq_no      , gmt_created ,
      gmt_modified , version
    )
    values (
      %(lesson_id)s , %(exercise_id)s , %(repetition)s ,
      %(measure)s   , %(seq_no)s      , now()          ,
      now()         , 1
    )
    '''

    __sql_exist_res = '''
    select id from lesson where reference_no = %s
    '''

    __sql_insert_res = '''
    insert into lesson(
      id             , type         , title         ,
      bg_music       , description  , encouragement ,
      next_day_intro , reference_no , gmt_created   ,
      gmt_modified   , version
    )
    values (
      null               , %(type)s        , %(title)s         ,
      %(bg_music_base)s  , %(description)s , %(encouragement)s ,
      %(next_day_intro)s , %(ref_no)s      , now()             ,
      now()              , 1
    )
    '''

    __sql_update_res = '''
    update lesson
       set type           = %(type)s,
           title          = %(title)s,
           bg_music       = %(bg_music_base)s,
           description    = %(description)s,
           encouragement  = %(encouragement)s,
           next_day_intro = %(next_day_intro)s,
           gmt_modified   = now(),
           version        = version + 1
     where reference_no   = %(ref_no)s
    '''

    def __init__(self, cfg, exercise_repo, resource_repo):
        BaseRepo.__init__(self, cfg)
        self.exercise_repo = exercise_repo
        self.resource_repo = resource_repo

    def check_exist(self, cursor, record):
        cursor.execute(self.__sql_exist_res, (record['ref_no'],))
        result = cursor.fetchone()
        return 0 if not result else result[0]

    def query_object(self, criteria):
        return self._do_query(criteria, self._query_object)

    def _query_object(self, criteria, cursor):
        cursor.execute(self.__sql_query_by_uk, criteria)
        rec = cursor.fetchone()
        if rec:
            return Lesson(**rec)

    def insert_record(self, cursor, record):
        cursor.execute(self.__sql_insert_res, record)
        return cursor.lastrowid

    def update_record(self, cursor, record):
        cursor.execute(self.__sql_update_res, record)

    def save_or_update(self, obj):
        record = dict(obj.__dict__)
        record.pop('lesson_exercises', None)
        record.pop('lesson_resources', None)
        return self._save_or_update(
            obj,
            record,
            self.check_exist,
            self.insert_record,
            self.update_record,
            self.save_related_data
        )

    def save_related_data(self, obj, lesson_id, cursor):
        lesson_exercises = obj.lesson_exercises
        if lesson_exercises:
            cursor.execute(self.__sql_clear_bv, {'lesson_id': lesson_id})
            cursor.execute(self.__sql_clear_le, {'lesson_id': lesson_id})
            for seq_no, le in enumerate(lesson_exercises, 1):
                rec = dict(le.__dict__)
                begin_voices = rec.pop('begin_voices', None)
                mid_voices = rec.pop('mid_voices', None)
                exercise_id = self.exercise_repo.check_exist(cursor, {'ref_no': le.exercise_ref})
                rec['seq_no'] = seq_no
                rec['lesson_id'] = lesson_id
                rec['exercise_id'] = exercise_id
                cursor.execute(self.__sql_insert_le, rec)
                if begin_voices:
                    for v in begin_voices:
                        rec1 = dict(v.__dict__)
                        rec1['type'] = 1
                        rec1['lesson_id'] = lesson_id
                        rec1['exercise_id'] = exercise_id
                        rec1['seq_no'] = seq_no
                        cursor.execute(self.__sql_insert_bv, rec1)
                if mid_voices:
                    for v in mid_voices:
                        rec1 = dict(v.__dict__)
                        rec1['type'] = 2
                        rec1['lesson_id'] = lesson_id
                        rec1['exercise_id'] = exercise_id
                        rec1['seq_no'] = seq_no
                        cursor.execute(self.__sql_insert_bv, rec1)

        lesson_resources = obj.lesson_resources
        if lesson_resources:
            cursor.execute(self.__sql_clear_lr, {'lesson_id': lesson_id})
            for lr in lesson_resources:
                # if the resource is already persisted
                resource_id = lr.id
                if not resource_id:
                    # save or update resource
                    resource_id = self.resource_repo.save_or_update(lr)
                # create lesson_resource record
                lr_rec = {'lesson_id': lesson_id, 'resource_id': resource_id}
                cursor.execute(self.__sql_insert_lr_rec, lr_rec)


class ExerciseRepo(BaseRepo):

    __sql_exist_res = '''
    select id from exercise where reference_no = %s
    '''

    __sql_query_by_uk = '''
    select id           as id,
           type         as type,
           duration     as duration,
           calories     as calories,
           thumbnail    as thumbnail_tfs,
           description  as description,
           action       as action,
           video_name   as video_name,
           reference_no as ref_no
      from exercise
     where reference_no = %(ref_no)s
    '''

    __sql_insert_res = '''
    insert into exercise(
      id          , type         , duration     ,
      calories    , thumbnail    , description  ,
      action      , video_name   , reference_no ,
      gmt_created , gmt_modified , version
    )
    values (
      null         , %(type)s            , %(duration)s    ,
      %(calories)s , %(thumbnail_tfs)s   , %(description)s ,
      %(action)s   , %(video_name_base)s , %(ref_no)s      ,
      now()        , now()               , 1
    )
    '''

    __sql_update_res = '''
    update exercise
       set type         = %(type)s,
           duration     = %(duration)s,
           calories     = %(calories)s,
           thumbnail    = %(thumbnail_tfs)s,
           description  = %(description)s,
           action       = %(action)s,
           video_name   = %(video_name_base)s,
           gmt_modified = now(),
           version      = version + 1
     where reference_no = %(ref_no)s
    '''

    __sql_clear_illustration = '''
    delete from illustration where exercise_id = %(exercise_id)s
    '''

    __sql_insert_illustration = '''
    insert into illustration (
      id           , title       , description ,
      images       , exercise_id , gmt_created ,
      gmt_modified , version
    )
    values (
      null           , %(title)s       , %(description)s ,
      %(images_tfs)s , %(exercise_id)s , now()           ,
      now()          , 1
    )
    '''

    def __init__(self, cfg):
        BaseRepo.__init__(self, cfg)

    def check_exist(self, cursor, record):
        cursor.execute(self.__sql_exist_res, (record['ref_no'],))
        result = cursor.fetchone()
        return 0 if not result else result[0]

    def query_object(self, criteria):
        return self._do_query(criteria, self._query_object)

    def _query_object(self, criteria, cursor):
        cursor.execute(self.__sql_query_by_uk, criteria)
        rec = cursor.fetchone()
        if rec:
            return Exercise(**rec)

    def insert_record(self, cursor, record):
        cursor.execute(self.__sql_insert_res, record)
        return cursor.lastrowid

    def update_record(self, cursor, record):
        cursor.execute(self.__sql_update_res, record)

    def save_or_update(self, obj):
        record = dict(obj.__dict__)
        record.pop('illustrations', None)
        return self._save_or_update(
            obj,
            record,
            self.check_exist,
            self.insert_record,
            self.update_record,
            self.save_related_data
        )

    def save_related_data(self, obj, exercise_id, cursor):
        illustrations = obj.illustrations
        cursor.execute(self.__sql_clear_illustration, {'exercise_id': exercise_id})
        if illustrations:
            for i in illustrations:
                rec = dict(i.__dict__)
                rec.pop("images", None)
                rec['exercise_id'] = exercise_id
                cursor.execute(self.__sql_insert_illustration, rec)


