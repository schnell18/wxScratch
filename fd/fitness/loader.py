# coding=utf-8

import os.path
import sys
from time import sleep

class Loader:

    def __init__(self, cfg, repo, ftp, tfs=None):
        self.cfg = cfg
        self.repo = repo
        self.ftp = ftp
        self.tfs = tfs

    def load(self, bundle, callback):
        path = bundle.path
        (c, l, e) = (bundle.curricula, bundle.lessons, bundle.exercises)

        try:
            # upload audio and video
            self.ftp.connect()
            self._upload_downloadable_resource(path, l, e, callback)

            # upload TFS pictures
            self._upload_tfs_resource(path, c, e, callback)

            # generate and persist meta data
            self._process_meta_data(c, l, e, callback)
        except Exception as x:
            sys.stderr.write("Fail to upload due to: " + str(x))
            raise
        finally:
            self.ftp.disconnect()

    def _upload_tfs_resource(self, base_dir, curricula, exercises,
            callback):
        if callback:
            callback.update_progress(u"准备图片上传", 0)
        for curriculum in curricula:
            curriculum.cover_tfs = self.tfs.upload(os.path.join(base_dir, curriculum.cover))
            if callback:
                callback.update_progress(u"TFS图片上传: " + curriculum.cover, 2)
            curriculum.icon_tfs = self.tfs.upload(os.path.join(base_dir, curriculum.icon))
            if callback:
                callback.update_progress(u"TFS图片上传: " + curriculum.icon, 2)

        for exercise in exercises:
            if exercise.thumbnail:
                exercise.thumbnail_tfs = self.tfs.upload(os.path.join(base_dir, exercise.thumbnail))
                if callback:
                    callback.update_progress(u"TFS图片上传: " + exercise.thumbnail, 2)
            if exercise.illustrations:
                for i in exercise.illustrations:
                    if i.images:
                        tfs_keys = []
                        for img in i.images:
                            tfs_keys.append(self.tfs.upload(os.path.join(base_dir, img)))
                            if callback:
                                callback.update_progress(u"TFS图片上传: " + img, 2)
                        i.images_tfs = '|'.join(tfs_keys)
        if callback:
            callback.update_progress(u"完成图片上传", 0)

    def _upload_downloadable_resource(self, base_dir, lessons,
            exercises, callback):
        if callback:
            callback.update_progress(u"准备FTP上传", 0)

        for lesson in lessons:
            if lesson.bg_music:
                self.ftp.upload(
                    os.path.join(base_dir, lesson.bg_music),
                    'l/' + os.path.dirname(lesson.bg_music)
                )
                if callback:
                    callback.update_progress(u"FTP上传背景音: " + lesson.bg_music, 2)
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
                            if callback:
                                callback.update_progress(
                                    u"FTP上传准备音: " + bv.audio_name, 2)
                    mid_voices = le.mid_voices
                    if mid_voices:
                        for bv in mid_voices:
                            self.ftp.upload(
                                os.path.join(base_dir, bv.audio_name),
                                'l/' + os.path.dirname(bv.audio_name)
                            )
                            if callback:
                                callback.update_progress(
                                    u"FTP上传动作音: " + bv.audio_name, 2)

        for exercise in exercises:
            if exercise.type != 1:
                continue
            self.ftp.upload(
                os.path.join(base_dir, exercise.video_name),
                'l/' + os.path.dirname(exercise.video_name)
            )
            if callback:
                callback.update_progress(u"FTP上传视频: " + exercise.video_name, 3)

        if callback:
            callback.update_progress(u"完成FTP上传", 0)

    def _process_meta_data(self, c, l, e, callback):
        if callback:
            callback.update_progress(u"准备课程元数据导入", 0)
        # save or update all exercises
        for exercise in e:
            exercise.id = self.repo.exercise_repo.save_or_update(exercise)
            if callback:
                callback.update_progress(u"保存动作元数据: " + exercise.title, 1)

        # save or update all lessons
        for lesson in l:
            lesson.id = self.repo.lesson_repo.save_or_update(lesson)
            if callback:
                callback.update_progress(u"保存子课元数据: " + lesson.title, 1)

        # save or update all curricula
        for curriculum in c:
            curriculum.id = self.repo.curriculum_repo.save_or_update(curriculum)
            if callback:
                callback.update_progress(u"保存课程元数据: " + curriculum.title, 1)
        # handle next curricula relation data
        for curriculum in c:
            self.repo.curriculum_repo.save_next_curricula(curriculum)
            if callback:
                callback.update_progress(u"保存推荐课程元数据: " + curriculum.title, 1)

        if callback:
            callback.update_progress(u"完成课程元数据导入", 0)

    def _upload_tfs_file(self, path):
        return self.tfs.upload(path)

    def _make_jump_url(self, jump_spec):
        if not jump_spec or not jump_spec.get('params'):
            return None
        pairs = ['"%s":"%s"' % (kv.get('key'), kv.get('value')) for kv in jump_spec.get('params')]
        return "%s?content={%s}" % (jump_spec['prefix'], ','.join(pairs))
