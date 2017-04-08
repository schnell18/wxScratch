# coding=utf-8

from __future__ import print_function

import os.path
import os
import sys
import tempfile

import yaml
from fitness.model import Bundle
from fitness.model import Curriculum
from fitness.model import CurriculumLesson
from fitness.model import Lesson
from fitness.model import Exercise
from fitness.model import LessonExercise
from fitness.model import Illustration
from fitness.model import Audio
from fitness.model import ResourceSet
from fitness.util import validate_filename


class Parser:

    def __init__(self, cfg, repo):
        self.cfg = cfg
        self.repo = repo

    def save_bundle(self, bundle):
        yaml_obj = self.as_yaml_data(bundle)
        # create META-INF directory if absent
        sub_dir = os.path.join(bundle.path, 'META-INF')
        if not os.path.exists(sub_dir):
           os.makedirs(sub_dir)
        # save curriculum.yml
        fp = os.path.join(bundle.path, 'META-INF', 'curriculum.yml')
        with open(fp, 'w') as cf:
            yaml.dump(
                yaml_obj['curricula'],
                cf,
                allow_unicode=True,
                default_flow_style=False
            )

        # save lesson.yml
        fp = os.path.join(bundle.path, 'META-INF', 'lesson.yml')
        with open(fp, 'w') as lf:
            yaml.dump(
                yaml_obj['lessons'],
                lf,
                allow_unicode=True,
                default_flow_style=False
            )

        # save exercise.yml
        fp = os.path.join(bundle.path, 'META-INF', 'exercise.yml')
        with open(fp, 'w') as ef:
            yaml.dump(
                yaml_obj['exercises'],
                ef,
                allow_unicode=True,
                default_flow_style=False
            )

    def as_yaml_data(self, bundle):
        data = {}
        curricula = []
        for c in bundle.curricula:
            rec = {}
            rec['refNo'] = c.ref_no
            rec['cornerLabelType'] = c.corner_label_type
            rec['cover'] = c.cover
            rec['icon'] = c.icon
            rec['title'] = c.title
            rec['description'] = c.description
            rec['previewVideo'] = c.preview_video
            cls = []
            if c.curriculum_lessons:
                for l in c.curriculum_lessons:
                    lesson_rec = {}
                    lesson_rec['lessonRef'] = l.lesson_ref
                    lesson_rec['title'] = l.lesson_title
                    if l.is_break:
                        lesson_rec['break'] = 'y'
                    cls.append(lesson_rec)
                rec['lessons'] = cls
            if c.next_curricula_refs:
                rec['nextCurricula'] = c.next_curricula_refs
            curricula.append({'curriculum': rec})
        data['curricula'] = curricula

        lessons = []
        for c in bundle.lessons:
            rec = {}
            rec['refNo'] = c.ref_no
            rec['type'] = c.type
            rec['title'] = c.title
            rec['bgMusic'] = c.bg_music
            rec['title'] = c.title
            rec['encouragement'] = c.encouragement
            rec['description'] = c.description
            rec['nextDayIntro'] = c.next_day_intro
            if c.lesson_exercises:
                cls = []
                for l in c.lesson_exercises:
                    le_rec = {}
                    le_rec['exerciseRef'] = l.exercise_ref
                    le_rec['repetition'] = l.repetition
                    le_rec['measure'] = l.measure
                    if l.begin_voices:
                        bvs = []
                        for bv in l.begin_voices:
                            bv_rec = {}
                            bv_rec['audioName'] = bv.audio_name
                            bv_rec['position'] = bv.position
                            bvs.append(bv_rec)
                        le_rec['beginVoices'] = bvs
                    if l.mid_voices:
                        bvs = []
                        for bv in l.mid_voices:
                            bv_rec = {}
                            bv_rec['audioName'] = bv.audio_name
                            bv_rec['position'] = bv.position
                            bvs.append(bv_rec)
                        le_rec['midVoices'] = bvs
                    cls.append(le_rec)
                rec['exercises'] = cls
            lessons.append({'lesson': rec})
        data['lessons'] = lessons

        exercises = []
        for c in bundle.exercises:
            rec = {}
            if c.type == 1:
                rec['refNo'] = c.ref_no
                rec['type'] = c.type
                rec['title'] = c.title
                rec['action'] = c.action
                rec['calories'] = c.calories
                rec['duration'] = c.duration
                rec['description'] = c.description
                rec['thumbnail'] = c.thumbnail
                rec['videoName'] = c.video_name
                if c.illustrations:
                    cls = []
                    for l in c.illustrations:
                        illu_rec = {}
                        illu_rec['title'] = l.title
                        illu_rec['description'] = l.description
                        if l.images:
                            illu_rec['images'] = l.images
                        cls.append(illu_rec)
                    rec['illustrations'] = cls
            else:
                rec['refNo'] = c.ref_no
                rec['type'] = c.type
                rec['title'] = c.title
                rec['duration'] = c.duration
            exercises.append({'exercise': rec})
        data['exercises'] = exercises

        return data

    def parse_bundle(self, path):
        if not os.path.isdir(path):
            raise ValueError("Invalid curriculum bundle at: " + path)
        meta_dir = os.path.join(path, 'META-INF')
        def_files = [
            os.path.join(meta_dir, f) for f in os.listdir(meta_dir)
            if os.path.isfile(os.path.join(meta_dir, f)) and f.endswith(".yml")
        ]
        if not os.path.isdir(meta_dir) or len(def_files) == 0:
            raise ValueError("No curriculum definition found at: " + path)

        lines = []
        for f in [open(f) for f in def_files]:
            for l in f.readlines():
                lines.append(l)
        bundle = Bundle(path=path, data=yaml.load(''.join(lines)))
        self._valid_bundle(bundle)
        (c, l, e) = self._parse_bundle(bundle)
        bundle.curricula = sorted(c.values(), key=lambda e : e.sort_no)
        bundle.lessons = sorted(l.values(), key=lambda e : e.sort_no)
        bundle.exercises = sorted(e.values(), key=lambda f : f.sort_no)
        return bundle

    def _valid_bundle(self, bundle):
        data = bundle.data
        # check if required properties are defined
        for e in [e['exercise'] for e in data if e.get('exercise')]:
            if not e.get("refNo"):
                raise ValueError("refNo is required for exercise")
            if not e.get("title"):
                raise ValueError("title is required for exercise")
            if not e.get("duration"):
                raise ValueError("duration is required for exercise")
            ex_type = e.get("type", 1)
            if ex_type == 1:
                if not e.get("action"):
                    raise ValueError("action is required for exercise")
                if not e.get("thumbnail"):
                    raise ValueError("thumbnail is required for exercise")
                if not e.get("videoName"):
                    raise ValueError("videoName is required for exercise")
                if not e.get("calories"):
                    raise ValueError("calories is required for exercise")
                video_name = e.get("videoName")
                if not video_name:
                    raise ValueError("videoName is required for exercise")
                self._validate_file('videoName', video_name, bundle.path)
                thumbnail = e.get("thumbnail")
                if not thumbnail:
                    raise ValueError("thumbnail is required for exercise")
                self._validate_file('thumbnail', thumbnail, bundle.path)

        for e in [e['lesson'] for e in data if e.get('lesson')]:
            if not e.get("refNo"):
                raise ValueError("refNo is required for lesson")
            if not e.get("title"):
                raise ValueError("title is required for lesson")
            if not e.get("encouragement"):
                raise ValueError("encouragement is required for lesson")
            if not e.get("nextDayIntro"):
                raise ValueError("nextDayIntro is required for lesson")
            bg_music = e.get("bgMusic")
            if bg_music:
                self._validate_file('bgMusic', bg_music, bundle.path)

        for e in [e['curriculum'] for e in data if e.get('curriculum')]:
            if not e.get("refNo"):
                raise ValueError("refNo is required for curriculum")
            if not e.get("title"):
                raise ValueError("title is required for curriculum")
            if not e.get("cover"):
                raise ValueError("cover is required for curriculum")
            if not e.get("icon"):
                raise ValueError("icon is required for curriculum")
            preview_video = e.get("previewVideo")
            if not preview_video:
                raise ValueError("previewVideo is required for curriculum")
            icon = e.get("icon")
            if not icon:
                raise ValueError("icon is required for curriculum")
            self._validate_file('icon', icon, bundle.path)
            cover = e.get("cover")
            if not cover:
                raise ValueError("cover is required for curriculum")
            self._validate_file('cover', cover, bundle.path)
            lessons = e.get("lessons")
            if not lessons:
                raise ValueError("curriculum #%s has no lessons defined" % (e.get("refNo"),))
            for lesson in lessons:
                lesson_ref = lesson.get("lessonRef")
                if not lesson_ref and 'n' == lesson.get("break", 'n'):
                    raise ValueError("curriculum #%s has invalid break" % (e.get("refNo"),))

        # resource check

    def _parse_bundle(self, bundle):
        base_dir = bundle.path
        data = bundle.data

        exercises = {}
        for sort_no, e in enumerate(
            [e['exercise'] for e in data if e.get('exercise')]):
            illustrations = []
            for i in e.get('illustrations', []):
                illustrations.append(
                    Illustration(
                        title=i.get('title'),
                        description=i.get('description'),
                        images=i.get('images'),
                    )
                )

            exercises[e['refNo']] = Exercise(
                ref_no=e.get('refNo'),
                type=e.get('type', 1),
                title=e.get('title'),
                action=e.get('action'),
                calories=e.get('calories', 0),
                duration=e.get('duration'),
                description=e.get('description'),
                thumbnail=e.get('thumbnail'),
                video_name=e.get('videoName'),
                illustrations=illustrations,
                sort_no=sort_no
            )

        lessons = {}
        for sort_no, e in enumerate(
            [e['lesson'] for e in data if e.get('lesson')]):
            lesson_exercise_objs = []
            resource_set = ResourceSet()
            for exercise in e.get("exercises", []):
                # referential integrity check
                exercise_obj = self._get_exercise_obj(exercises, exercise['exerciseRef'])
                if not exercise_obj:
                    raise ValueError("Lesson #%s refer to invalid exercise #%s" % (e['refNo'], exercise['exerciseRef']))
                # break has no video
                if exercise_obj.type == 1:
                    if not exercise_obj.id:
                        resource_set.add_resource(
                            self.cfg['download_base_url'],
                            base_dir,
                            exercise_obj.video_name,
                            e['refNo']
                        )
                    else:
                        persistent_resource = self.repo.resource_repo.query_object({'name': exercise_obj.video_name})
                        resource_set.add_persistent_resource(persistent_resource)
                begin_voices = []
                for bv in exercise.get('beginVoices', []):
                    begin_voices.append(
                        Audio(
                            audio_name=bv.get('audioName'),
                            position=bv.get('position')
                        )
                    )
                    resource_set.add_resource(
                        self.cfg['download_base_url'],
                        base_dir,
                        bv.get('audioName'),
                        e['refNo']
                    )

                mid_voices = []
                for bv in exercise.get('midVoices', []):
                    mid_voices.append(
                        Audio(
                            audio_name=bv.get('audioName'),
                            position=bv.get('position')
                        )
                    )
                    resource_set.add_resource(
                        self.cfg['download_base_url'],
                        base_dir,
                        bv.get('audioName'),
                        e['refNo']
                    )

                lesson_exercise_objs.append(
                    LessonExercise(
                        title=exercise_obj.title,
                        exercise_ref=exercise['exerciseRef'],
                        repetition=exercise['repetition'],
                        measure=exercise['measure'],
                        begin_voices=begin_voices,
                        mid_voices=mid_voices
                    )
                )

            resource_set.add_resource(
                self.cfg['download_base_url'],
                base_dir,
                e.get('bgMusic'),
                e['refNo']
            )
            lessons[e['refNo']] = Lesson(
                ref_no=e.get('refNo'),
                title=e.get('title'),
                type=e.get('type', 1),
                description=e.get('description'),
                bg_music=e.get('bgMusic'),
                encouragement=e.get('encouragement'),
                next_day_intro=e.get('nextDayIntro'),
                lesson_exercises=lesson_exercise_objs,
                lesson_resources=resource_set.get_resources(),
                sort_no=sort_no
            )

        curricula = {}
        for sort_no, e in enumerate(
            [e['curriculum'] for e in data if e.get('curriculum')]):
            lesson_objs = []
            for lesson in e.get("lessons", []):
                lesson_ref = lesson.get('lessonRef', None)
                # referential integrity check
                if lesson_ref and not self._get_lesson_obj(lessons, lesson_ref):
                    raise ValueError("Curriculum #%s refer to invalid lesson #%s" % (e['refNo'], lesson_ref))
                lesson_objs.append(
                    CurriculumLesson(
                        lesson_ref=lesson_ref,
                        lesson_title=lesson.get('title'),
                        is_break=True if lesson.get('break', 'n') == 'y' else False,
                    )
                )

            curricula[e['refNo']] = Curriculum(
                ref_no=e.get('refNo'),
                title=e.get('title'),
                cover=e.get('cover'),
                icon=e.get('icon'),
                jump_url=self._make_jump_url(e.get('jumpSpec')),
                preview_video=e.get('previewVideo'),
                corner_label_type=e.get('cornerLabelType'),
                description=e.get('description'),
                curriculum_lessons=lesson_objs,
                next_curricula_refs=e.get('nextCurricula'),
                sort_no=sort_no
            )

        for nc in curricula.keys():
            curriculum_obj = curricula.get(nc)
            if not curriculum_obj.next_curricula_refs:
                continue
            next_curricula = []
            for ref in curriculum_obj.next_curricula_refs:
                # referential integrity check
                ref_obj = self._get_curriculum_obj(curricula, ref)
                if not ref_obj:
                    raise ValueError("Curriculum #%s refer to invalid curriculum #%s" % (curriculum_obj.ref_no, ref))
                next_curricula.append(ref_obj)
            curriculum_obj.set_next_curricula(next_curricula)

        return curricula, lessons, exercises

    def _validate_file(self, prop_name, prop_value, base_dir):
        if not validate_filename(prop_value):
            raise ValueError("%s filename: %s contains invalid char" % (prop_name, prop_value))
        file = os.path.join(base_dir, prop_value)
        if not os.path.isfile(file):
            raise ValueError("%s %s not found" % (prop_name, file))

    def _make_jump_url(self, jump_spec):
        if not jump_spec or not jump_spec.get('params'):
            return None
        pairs = ['"%s":"%s"' % (kv.get('key'), kv.get('value')) for kv in jump_spec.get('params')]
        return "%s?content={%s}" % (jump_spec['prefix'], ','.join(pairs))

    def _get_exercise_obj(self, exercises, ref_no):
        obj = exercises.get(ref_no, None)
        if not obj:
            obj = self.repo.exercise_repo.query_object({'ref_no': ref_no})
        return obj

    def _get_lesson_obj(self, lessons, lesson_ref):
        obj = lessons.get(lesson_ref)
        if not obj:
            obj = self.repo.lesson_repo.query_object({'ref_no': lesson_ref})
        return obj

    def _get_curriculum_obj(self, curricula, curriculum_ref):
        obj = curricula.get(curriculum_ref)
        if not obj:
            obj = self.repo.curriculum_repo.query_object({'ref_no': curriculum_ref})
        return obj
