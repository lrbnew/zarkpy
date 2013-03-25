#coding=utf-8
import web
import site_helper as sh

# ../../editor/model/List.html
# ../../subpage/editor/ViewItem.html

class List:

    def GET(self, model_name):
        model = sh.model(model_name)
        menu_config = sh.ctrl('Editor').getMenuConfig()
        # 禁止访问未公开的路径
        if not menu_config: return sh.redirectTo404()

        env = self._getEnv(model, menu_config)

        items = model.all(env)
        pagination_html = model.getPaginationHtml(env) \
                if hasattr(model, 'getPaginationHtml') else ''

        return sh.editor.model.List(model_name, model.column_names + menu_config.append_column,
                model.getColumnTypes(), menu_config, items, pagination_html, )

    def _getEnv(self, model, menu_config):
        inputs = sh.inputs()
        env = sh.storage(dict(paging=True))
        env.orderby = model.replaceAttr(menu_config.orderby  \
                if menu_config.orderby else '{$primary_key} desc')

        if inputs.get('action', '') == 'search':
            where = []
            argvs = []
            for query in sh.splitAndStrip(inputs.query):
                where.append('('+ ' or '.join([c+' like %s' for c in menu_config.search]) +')')
                argvs += ['%'+query+'%'] * len(menu_config.search)
            env.where = (' and '.join(where), argvs)

        return env
