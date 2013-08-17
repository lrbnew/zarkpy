#coding=utf-8
# ../editor/SiteConfig.html
import site_helper as sh

class SiteConfig:

    def GET(self, name):
        inputs = sh.inputs()
        menu_config = sh.ctrl('Editor').getMenuConfig()
        # 禁止访问未公开的路径
        if not menu_config: return sh.redirectTo404()

        model = sh.model('SiteConfig')
        env = sh.storage()

        if menu_config.get('filter', None):
            env['where'] = ['name like %s', menu_config['filter']]

        if menu_config.get('orderby', None):
            env.orderby = model.replaceAttr(menu_config.orderby)

        if inputs.get('where', ''):
            env.where = [inputs.where]

        items = model.all(env)
        pagination_html = model.getPaginationHtml(env)

        return sh.editor.SiteConfig(items, pagination_html, menu_config)
