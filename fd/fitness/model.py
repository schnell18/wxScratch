# coding=utf-8
from os.path import basename
from os.path import getsize
from os.path import join
from util import md5sum


class Bundle:
    def __init__(self, **kwargs):
        self.path = kwargs['path']
        self.data = kwargs['data']
        self.curricula = None
        self.lessons = None
        self.exercise = None

    def __str__(self):
        return "path: %s data: %s" % (self.path, self.data)

    def __repr__(self):
        return self.__str__()


class Curriculum:
    def __init__(self, ref_no, **kwargs):
        self.id = kwargs.get("id")
        self.ref_no = ref_no
        self.title = kwargs.get("title")
        self.cover = kwargs.get("cover")
        self.icon = kwargs.get("icon")
        self.preview_video = kwargs.get("preview_video")
        self.corner_label_type = kwargs.get("corner_label_type")
        self.description = kwargs.get("description")
        self.jump_url = kwargs.get("jump_url")
        self.curriculum_lessons = kwargs.get("curriculum_lessons")
        self.next_curricula_refs = kwargs.get("next_curricula_refs")
        self.next_curricula = None
        self.cover_tfs = kwargs.get("cover_tfs")
        self.icon_tfs = kwargs.get("icon_tfs")
        self.preview_video_url = None
        self.sort_no = kwargs.get("sort_no")

    def set_next_curricula(self, next_curricula):
        self.next_curricula = next_curricula

    def name_for_ui(self):
        return self.__class__.__name__ + '-' + self.ref_no

    def __str__(self):
        return "ref_no: %s title: %s" % (self.ref_no, self.title)

    def __repr__(self):
        return self.__str__()


class Lesson:
    def __init__(self, ref_no, **kwargs):
        self.id = kwargs.get("id")
        self.ref_no = ref_no
        self.title = kwargs.get("title")
        self.type = kwargs.get("type")
        self.description = kwargs.get("description")
        self.bg_music = kwargs.get("bg_music")
        self.bg_music_base = basename(self.bg_music) if self.bg_music else None
        self.encouragement = kwargs.get("encouragement")
        self.next_day_intro = kwargs.get("next_day_intro")
        self.lesson_exercises = kwargs.get("lesson_exercises")
        self.lesson_resources = kwargs.get("lesson_resources")
        self.sort_no = kwargs.get("sort_no")

    def name_for_ui(self):
        return self.__class__.__name__ + '-' + self.ref_no


class CurriculumLesson:
    def __init__(self, **kwargs):
        self.lesson_ref = kwargs.get("lesson_ref")
        self.lesson_title = kwargs.get("lesson_title")
        self.is_break = kwargs.get("is_break")

    def __str__(self):
        return "CurriculumLesson: %s %s %s" % (self.lesson_ref, self.lesson_title, self.is_break)

    def __repr__(self):
        return self.__str__()


class Exercise:
    def __init__(self, ref_no, type, **kwargs):
        self.id = kwargs.get("id")
        self.ref_no = ref_no
        self.type = type
        self.title = kwargs.get("title")
        self.action = kwargs.get("action")
        self.calories = kwargs.get("calories")
        self.duration = kwargs.get("duration")
        self.description = kwargs.get("description")
        self.thumbnail = kwargs.get("thumbnail")
        self.video_name = kwargs.get("video_name")
        self.video_name_base = basename(self.video_name) if self.video_name else None
        self.illustrations = kwargs.get("illustrations")
        self.thumbnail_tfs = kwargs.get("thumbnail_tfs")
        self.sort_no = kwargs.get("sort_no")

    def name_for_ui(self):
        return self.__class__.__name__ + '-' + self.ref_no


class LessonExercise:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.exercise_ref = kwargs.get("exercise_ref")
        self.repetition = kwargs.get("repetition")
        self.measure = kwargs.get("measure")
        self.begin_voices = kwargs.get("begin_voices")
        self.mid_voices = kwargs.get("mid_voices")
        self.ui_ref_no = None

    def name_for_ui(self):
        return self.ui_ref_no


class Audio:
    def __init__(self, **kwargs):
        self.audio_name = kwargs.get("audio_name")
        self.audio_name_base = basename(self.audio_name) if self.audio_name else None
        self.position = kwargs.get("position")


class Illustration:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.images = kwargs.get("images")
        self.images_tfs = None
        self.ui_ref_no = None

    def name_for_ui(self):
        return self.ui_ref_no


class Resource:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.size = kwargs.get("size")
        self.checksum = kwargs.get("checksum")
        self.lesson_ref = kwargs.get("lesson_ref")


class ResourceSet:
    def __init__(self):
        self.resource_set = {}

    def add_persistent_resource(self, resource):
        # calculate checksum
        if not resource:
            return
        checksum = resource.checksum
        if not self.resource_set.get(checksum):
            self.resource_set[checksum] = resource

    def add_resource(self, base_url, base_dir, path, lesson_ref=None, id=None):
        # calculate checksum
        if not path:
            return
        fp = join(base_dir, path)
        checksum = md5sum(fp)
        filename = basename(path)
        if not self.resource_set.get(checksum):
            sub_dir = 'l' if lesson_ref else 's'
            # calculate size and download url
            self.resource_set[checksum] = Resource(
                id=id,
                lesson_ref=lesson_ref,
                name=filename,
                size=getsize(fp),
                checksum=checksum,
                url="%s/%s/%s" % (base_url, sub_dir, path)
            )

    def get_resources(self):
        return self.resource_set.values()
