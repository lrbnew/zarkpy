#coding=utf-8
import site_helper as sh

# ../editor/IndentTable.html

class IndentTable:
    prefix_key = 'indent_table_'

    def GET(self, name):
        menu_config = sh.ctrl('Editor').getMenuConfig()
        # 禁止访问未公开的路径
        if not menu_config: return sh.redirectTo404()

        key = self.prefix_key + name
        value = sh.getSiteConfig(key)
        return sh.editor.IndentTable(value, menu_config)

    def POST(self, name):
        inputs = sh.inputs()
        assert inputs.has_key('value')
        key = self.prefix_key + name
        sh.setSiteConfig(key, inputs.value)
        return sh.refresh()
