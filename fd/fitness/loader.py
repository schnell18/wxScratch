# coding=utf-8

from __future__ import print_function

import os.path
import sys

class Loader:

    def __init__(self, cfg, repo, ftp, tfs=None):
        self.cfg = cfg
        self.repo = repo
        self.ftp = ftp
        self.tfs = tfs

    def load(self, bundle):
        (c, l, e) = (bundle.curricula, bundle.lessons, bundle.exercises)

        # upload audio and video
        try:
            self.ftp.connect()
            self._upload_downloadable_resource(path, l, e)
        except Exception as x:
            sys.stderr.write("Fail to upload due to: " + str(x))
            raise
        finally:
            self.ftp.disconnect()

        # upload TFS pictures
        self._upload_tfs_resource(path, c, e)

        # generate and persist meta data
        self._process_meta_data(c, l, e)


    def _upload_tfs_resource(self, base_dir, curricula, exercises):
        for curriculum in curricula:
            curriculum.cover_tfs = self.tfs.upload(os.path.join(base_dir, curriculum.cover))
            curriculum.icon_tfs = self.tfs.upload(os.path.join(base_dir, curriculum.icon))

        for exercise in exercises:
            if exercise.thumbnail:
                exercise.thumbnail_tfs = self.tfs.upload(os.path.join(base_dir, exercise.thumbnail))
            if exercise.illustrations:
                for i in exercise.illustrations:
                    if i.images:
                        tfs_keys = []
                        for img in i.images:
                            tfs_keys.append(self.tfs.upload(os.path.join(base_dir, img)))
                        i.images_tfs = '|'.join(tfs_keys)

    def _upload_downloadable_resource(self, base_dir, lessons, exercises):
        for lesson in lessons:
            if lesson.bg_music:
                self.ftp.upload(
                    os.path.join(base_dir, lesson.bg_music),
                    'l/' + os.path.dirname(lesson.bg_music)
                )
            lesson_exercises = lesson.lesson_exercises
            if lesson_exercises:
                for le in lesson_exercises:
                    begin_voices = le.begin_voices
                    if begin_voices:
                        for bv in begin_voices:
                            self.ftp.upload(
                                os.path.join(base_dir, bv.audio_name),
                                'l/' + os.path.dirname(bv.audio_name)
                            )
                    mid_voices = le.mid_voices
                    if mid_voices:
                        for bv in mid_voices:
                            self.ftp.upload(
                                os.path.join(base_dir, bv.audio_name),
                                'l/' + os.path.dirname(bv.audio_name)
                            )

        for exercise in exercises:
            if exercise.type != 1:
                continue
            self.ftp.upload(
                os.path.join(base_dir, exercise.video_name),
                'l/' + os.path.dirname(exercise.video_name)
            )

    def _process_meta_data(self, c, l, e):
        # save or update all exercises
        for exercise in e:
            exercise.id = self.repo.exercise_repo.save_or_update(exercise)

        # save or update all lessons
        for lesson in l:
            lesson.id = self.repo.lesson_repo.save_or_update(lesson)

        # save or update all curricula
        for curriculum in c:
            curriculum.id = self.repo.curriculum_repo.save_or_update(curriculum)
        # handle next curricula relation data
        for curriculum in c:
            self.repo.curriculum_repo.save_next_curricula(curriculum)

    def _upload_tfs_file(self, path):
        return self.tfs.upload(path)

    def _make_jump_url(self, jump_spec):
        if not jump_spec or not jump_spec.get('params'):
            return None
        pairs = ['"%s":"%s"' % (kv.get('key'), kv.get('value')) for kv in jump_spec.get('params')]
        return "%s?content={%s}" % (jump_spec['prefix'], ','.join(pairs))
