#coding=utf-8
import os
import site_helper as sh
# ../editor/CropImage.html
# 使用imgareaselect裁剪图片，imgareaselect的参数见:
# http://www.css88.com/EasyTools/javascript/jQueryPlugin/imgAreaSelect/index.html
# 使用方法，在sh.editor_config.menu的crop字段中第一列表示裁剪值字段名，第二列表示预览大小(如:100:200), 后面为fx参数形式传给fx

class CropImage:

    def GET(self):
        inputs = sh.inputs()
        assert inputs.has_key('model_name'), u'请指定需要裁剪的数据类型'
        assert inputs.has_key('model_id'), u'请指定需要裁剪的数据ID'
        assert inputs.has_key('crop'), u'请设置裁剪配置'
        item = sh.model(inputs.model_name).get(inputs.model_id)
        if not item or not item.has_key('Imageid'): return sh.redirectTo404()

        column_name, settings = sh.unquote(inputs.crop).partition(' ')[::2]
        inputs.crop_width, settings = settings.strip().partition(' ')[::2]

        preview_size, settings = settings.strip().partition(' ')[::2]
        inputs.preview_width, inputs.preview_height = preview_size.split(':')

        inputs.column_name = column_name
        inputs.crop_settings = settings
        inputs.image = item.image

        if item.get(column_name):
            inputs.crop = item.get(column_name)
        else:
            inputs.crop = '0 0 %s %s' % tuple(preview_size.split(':'))

        if len(inputs.crop.split()) == 4:
            x1, y1, x2, y2 = map(int, inputs.crop.split(' '))
            inputs.fx_crop = 'x1=%s;y1=%s;x2=%s;y2=%s;' % (x1,y1,x1+x2,y1+y2)
        else:
            inputs.fx_crop = ''

        return sh.editor.CropImage(inputs)

    def POST(self):
        inputs = sh.inputs()
        assert inputs.has_key('model_name'), u'请指定需要裁剪的数据类型'
        assert inputs.has_key('model_id'), u'请指定需要裁剪的数据ID'
        assert inputs.has_key('column_name'), u'请指定裁剪的列名'
        assert int(float(inputs.get('region_width', '0'))) > 0
        assert int(float(inputs.get('region_height', '0'))) > 0

        model = sh.model(inputs.model_name)
        item = model.get(inputs.model_id)
        image = item.image

        real_width, real_height = sh.imageSize(image.url) # 图片的真实宽高
        crop = inputs.crop
        region_width = int(float(inputs.region_width)) # 选择区域的宽度
        region_height = int(float(inputs.region_height)) # 选择区域的高度

        start_x  = int(crop.split()[0]) # 选中的起始位置
        start_y  = int(crop.split()[1])
        region_x  = int(crop.split()[2])# 选中的宽度
        region_y = int(crop.split()[3]) # 选中的高度
        
        # convert 裁剪区域
        region = '%dx%d+%d+%d' % (region_x * real_width / region_width, 
                                region_y * real_height / region_height,
                                real_width * start_x / region_width, 
                                real_height * start_y / region_height)

        path = sh.urlToPath(image.url)
        os.system('convert %s -crop %s %s' % (path, region, path+'.crop'))
        model.update(inputs.model_id, {inputs.column_name: crop})

        # 删除以前裁剪图片的各种尺寸副本
        os.system('rm %s.crop_*' % path)

        return sh.refresh()
