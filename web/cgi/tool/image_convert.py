#!/usr/bin/env python
#coding=utf-8
import os
import imghdr
import site_helper as sh

'''
使用imagemagick工具包中的convert对图片进行操作, env中可选的参数有:
    resize: widthxheight (压缩, 宽x高)
    crop:   widthxheight+start_x+start_y (裁剪，宽x高+x坐标+y坐标)
    profile: * (删除附加信息)
    save_file: (指定保存路径，默认使用尺寸作为后缀，如abc_25x25.jpg)
    format: 保存的目标格式
    use_exists: 是否使用已存在图片，为False则每次强制重新生成
    async: 异步创建图片
    first_image: 是否仅截取第一帧, 用于gif
'''

def convert(image_path, env):
    env = sh.copy(env)
    if not os.path.exists(image_path):
        return image_path
    assert env.get('resize', '') or env.get('save_file', ''), '必须给出保存路径'
    save_file = getSavePath(image_path, env) if not env.has_key('save_file') else env['save_file']

    if not env.get('use_exists', True) or not os.path.exists(save_file):
        convert_cmd = makeCommand(image_path, save_file, env)
        os.system(convert_cmd)

    return save_file

def getSavePath(image_path, env):
    assert(env.has_key('resize'))
    known_image_types = ['.jpg','.jpeg','.gif','.png']
    # 得到图片的保存类型
    if env.has_key('format'):
        save_type = env['format']
    elif any(map(image_path.endswith, known_image_types)):
        save_type = image_path.rpartition('.')[2]
    else:
        save_type = imghdr.what(None, open(image_path).read())
    # 获得文件名前缀
    if any(map(image_path.endswith, known_image_types)):
        name_pre = image_path.rpartition('.')[0]
    else:
        name_pre = image_path
    return '%s_%s.%s' % (name_pre, env['resize'].strip('!<>'), save_type)

def makeCommand(image_path, save_file, env):
    cmd = ['convert']
    cmd.append('"%s%s"' % (image_path, '[0]' if env.get('first_image', False) else ''))

    for arg in '-crop', '-resize', '+profile': # convert的语法要求resize要在crop之后
        key = arg.strip('-+')
        if env.has_key(key):
            cmd.append('%s "%s"' % (arg, env[key]))

    cmd.append('"%s"' % save_file)
    if env.get('async', True): cmd.append('&')
    return ' '.join(cmd)
