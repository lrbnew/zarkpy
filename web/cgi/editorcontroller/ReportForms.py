#coding=utf-8
# ../editor/ReportForms.html
import site_helper as sh

class ReportForms:

    def GET(self, path):
        mc = sh.ctrl('Editor').getMenuConfig()
        # 禁止访问未公开的路径
        if not mc: return sh.redirectTo404()

        inputs = sh.inputs()
        select = mc.get('select', '').replace('%', '%%') # 因为MySQLdb会转义%
        db = sh.getDBHelper()

        if mc.get('paging', ''):
            if ' limit ' in select.lower():
                return sh.alert('使用paging选项时select中不能使用limit, 请检查后台配置', stay=10)
            # 如果使用了paging, select中就不允许出现limit
            if int(mc.get('paging')) <= 0:
                return sh.alert('paging配置参数应为正整数', stay=10)
            if ' distinct ' in select.lower():
                return sh.alert('抱歉, 暂不支持paging与distinct一起使用', stay=10)
            # 查询count(*)
            form_key = ' from ' if ' from ' in select else ' FROM '
            total = self.__getTotal(select)
            # 设置limit获得数据
            select = select + ' limit %d, %d' % \
                self.__getLimit(inputs.get('page_num', 1), int(mc.paging))
            items = db.fetchSome(select)
            # 获得分页
            pagination_html = '<div fx="paging[style=zarkpy;pageCount=%d;totalCount=%d;displayPages=10;firstText=第一页;lastText=末页;]"></div>' % (int(mc.paging), total)

        else:
            items = db.fetchSome(select)
            pagination_html = ''

        keys = self.__getSortedKeys(select)
        if len(keys) == 0 and len(items) > 0:
            keys = items[0].keys()

        return sh.editor.ReportForms(items, pagination_html, keys, mc)

    def __getLimit(self, page_num, volume):
        return (int(volume) * (int(page_num) - 1), int(volume))

    # 从select语句中获得key顺序
    def __getSortedKeys(self, select):
        form_key = ' from ' if ' from ' in select else ' FROM '
        if '*' in select.partition(form_key)[0] and ',' not in select.partition(form_key)[0]:
            return []

        else:
            keys= []
            key = []
            bracket_count = 0
            for c in select.partition(form_key)[0] + ',':
                if c == '(':
                    bracket_count += 1
                    key.append(c)
                elif c == ')':
                    bracket_count -= 1
                    key.append(c)
                elif bracket_count == 0 and c == ',':
                    key = ''.join(key).strip().rpartition(' ')[2]
                    keys.append(key)
                    key = []
                else:
                    key.append(c)

            if bracket_count != 0:
                return sh.alert('select语句有语法错误', stay=10)

            return keys

    def __getTotal(self, select):
        db = sh.getDBHelper()
        if ' group by ' in select.lower():
            return len(db.fetchSomeFirst(select))
        else:
            form_key = ' from ' if ' from ' in select else ' FROM '
            return db.fetchFirst('select count(*) from ' + select.partition(form_key)[2])
