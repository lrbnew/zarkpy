#coding=utf-8
import site_helper as sh

class EditorImage:

    # 处理tiny_mce富文本编辑器插入图片的请求
    def POST(self):
        inputs = sh.inputs()
        if not inputs.has_key('image_file'):
            return '<script>window.close();</script>'

        model = sh.model('EditorImage')
        inputs.title = inputs.image_file.filename
        new_id = model.insert(inputs)
        return self.insert_image_callback % model.get(new_id).image.url

    # tiny_mce插入图片的回调函数
    insert_image_callback = '''
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>insertcallback</title>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <script type="text/javascript" src="/plugins/jquery-plugins/jquery-1.3.2.js"></script>
            <script type="text/javascript" src="/plugins/jquery-plugins/tiny_mce/tiny_mce_popup.js"></script>
            <script type="text/javascript" src="/plugins/jquery-plugins/tiny_mce/plugins/sparker5imagemanager/js/dialog.js"></script>
            <script>
                tinyMCEPopup.editor.execCommand('mceInsertContent', false,'<img src="%s" />');
                tinyMCEPopup.close();
            </script>
        </head> <body> </body> </html>
    '''
