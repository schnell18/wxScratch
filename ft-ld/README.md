# Introduction
This project implements a collection of utilities to load curriculum
data and shared resources. Curriculum definition is described in YAML
format.

# Setup
This project is developed and tested under Python 2.7.  The third-party
modules required by this project are listed in the *requirements.txt*
file. To install these dependencies in one go, run the following
command:

    pip install -r requirements.txt

# curriculum loader
Curriculum definitions can be organized in bundle. The bundle is a
structured directory which includes both YAML files to describe
curriculum definition as well as resource files such as image, audio and
video. YAML files should be placed under the sub-directory *META-INF*.
Curriculum objects consist of the following types:

- Exercise
- Lesson
- Curriculum

For the sake of clarity, curriculum definitions are typically divided
into the following three files per bundle:

- exercise.yml
- lesson.yml
- curriculum.yml

These files should be self-contained. They should not reference any
curriculum object which is defined inside these files. The contents in
these files must be UTF-8 encoded.

An excerpt of curriculum definition is listed as follows:

    - curriculum:
        refNo: curri01
        cornerLabelType: 0
        cover: images/cover.png
        icon: images/icon.png
        title: 健身课程1
        description: 健身课程1
        previewVideo: video/yugaoshipin_800448.mp4
        jumpSpec:
          prefix: pajk://consult_consultchat_jump
          params:
            - key: chooseKey
              value: 114
            - key: tagId
              value: 123
        lessons:
          - lessonRef: lesson1
            title: 魔鬼训练第一天
          - lessonRef:
            break: y
            title: 不要暴饮暴食即可
          - lessonRef: lesson1
            title: 魔鬼训练第三天
          - lessonRef: lesson1
            title: 魔鬼训练第四天
          - lessonRef: lesson1
            title: 魔鬼训练第五天
          - lessonRef: lesson1
            title: 魔鬼训练第六天
          - lessonRef:
            break: y
            title: 不要暴饮暴食即可
          - lessonRef: lesson1
            title: 魔鬼训练第八天
          - lessonRef: lesson1
            title: 魔鬼训练第九天
          - lessonRef: lesson1
            title: 魔鬼训练第十天
        nextCurricula:
          - curri02
          - curri03
          - curri04

In this example, the *cover* and *icon* properties reference resource
file respectively. Resource files are specified in relative path which
starts with curriculum bundle root directory. For complete example,
please refer to the sample curriculum bundle.


With curriculum bundle defined, you are ready to load the bundle with
curriculum loader utility. This utility implements the following
functions:

- validate the curriculum bundle
- upload image files to specified TFS
- upload lesson-specific audio and video files to specified FTP
- calculate size and checksum of all resource files
- generate and persist meta data of the curriculum in question

It requires a config file to specify:

- database to store curriculum data
- connection information of TFS to store images
- connection information of FTP to store audio and video

An example of such config file is as follows:

    [general]
    download_base_url=http://resource.dev.pajkdc.com/fitness

    [mysql]
    user=pajk
    password=abc
    host=192.168.11.20
    port=3306
    database=fitness

    [ftp.resource]
    user=devel
    password=devel
    host=192.168.11.20
    port=21
    root_dir=fitness

    [tfs]
    base_url=http://static.dev.pajkdc.com/v1/tfs

This file should be placed under the sub directory *.fitness* of home
directory. The basic usage of this tool is as follows:

    load_curriculum.py <curriculum_bundle_dir>

As a bonus, you can generate the QR code image to preview imported curricula
in one go with the following command:

    load_curriculum_qr.py <curriculum_bundle_dir>
    
# shared resource loader
The shared resource loader is capable of performing functions as
follows:

- validate the shared resource zip file
- re-generate *content.lst* file and repack into the zip file
- upload the zip file to specified FTP
- calculate size and checksum of all resource files
- generate and persist meta data of the zip file in question

This tool shares the same config file as curriculum loader utility.
The basic usage is as follows:

    load_shared_res.py <resource_zip_location>

