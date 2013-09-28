#coding=utf-8
# ../../editor/model/Edit.html
import web
import site_helper as sh

class Edit:

    def GET(self, model_name, model_id=None):
        menu_config = sh.ctrl('Editor').getMenuConfig()
        # 禁止访问未公开的路径
        if not menu_config: return sh.redirectTo404()

        model = sh.model(model_name)

        if model_id:
            item = model.get(model_id)
            action = 'update'
            assert item is not None
        else:
            item = None
            action = 'insert'

        return sh.editor.model.Edit(model_name, model.column_names + menu_config.append_column, model.getColumnTypes(), menu_config, item, action)

