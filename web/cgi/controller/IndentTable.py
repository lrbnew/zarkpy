#coding=utf-8
# 请通过测试文件来了解IndentTable
# ../testing/controller_test/TestIndentTable.py
import web
import site_helper as sh

class IndentTable:

    # 根据config返回递归的二元组list
    def indent(self, config):
        assert isinstance(config, (str, unicode)), u'config必须是一个字符串缩进表'
        queue = []
        ret_list = []
        for l in config.replace('\r','').split('\n'):
            assert '\t' not in l, u'表中不能出现table字符'
            if l.strip() == '': continue
            space_len = len(l)-len(l.lstrip())
            l = l.strip()
            if len(queue) == 0:
                next_indent = []
                ret_list.append([l, next_indent])
                queue.append([space_len, next_indent])
            else:
                if space_len > queue[-1][0]:
                    next_indent.append([l, []])
                    next_indent = next_indent[-1][1]
                    queue.append([space_len, next_indent])
                elif space_len == queue[-1][0]:
                    assert len(queue) > 0, 'queue=%s\nspace_len=%d' % (str(queue),space_len)
                    if len(queue) > 1:
                        queue.pop()
                        next_indent = queue[-1][1]
                        next_indent.append([l, []])
                        next_indent = next_indent[-1][1]
                        queue.append([space_len, next_indent])
                    elif len(queue) == 1:
                        queue.pop()
                        next_indent = []
                        ret_list.append([l, []])
                else:
                    while len(queue)>1 and space_len < queue[-1][0]:
                        queue.pop()
                    queue.pop()
                    if len(queue) > 0:
                        next_indent = queue[-1][1]
                        next_indent.append([l, []])
                        next_indent = next_indent[-1][1]
                        queue.append([space_len, next_indent])
                    else:
                        next_indent = []
                        ret_list.append([l, next_indent])
                        queue.append([space_len, next_indent])
        return ret_list

    # 求indents的最大缩进层级数
    def getIndentsLevel(self, indents):
        def _findMaxLevel(i, curr_level):
            return max([_findMaxLevel(v, curr_level+1) if isinstance(v, list) else curr_level for k,v in i]) if i else curr_level
        return _findMaxLevel(indents, 0)

    # 把indents还原为缩进配置表
    def indentsToConfig(self, indents, space=4):
        def _toString(i, level):
            configs = []
            for k, v in i:
                configs.append(' ' * space * level + k.strip() + '\n')
                if isinstance(v, list):
                    configs.append(_toString(v, level+1))
            return ''.join(configs)
        return _toString(indents, 0).strip()

    def refill(self, indents):
        ret_list = []
        queue = []
        def _indentsToLines(indents):
            for a,b in indents:
                ret_list.append(sh.copy(queue+[a]))
                if len(b) != 0:
                    queue.append(a)
                    _indentsToLines(b)
                    queue.pop()
        _indentsToLines(indents)
        assert(len(queue) == 0)
        return ret_list

    def indentsToDict(self, indents, add_index=False):

        def _indentsToDict(key, values):
            if len(values) == 0:
                if ':' not in key:
                    return str(key.strip())
                else:
                    a,b,c = key.partition(':')
                    return [a, c.strip()]
            else:
                ret_dict = {} if not add_index else {'__index': _indentsToDict._index}
                ret_dict = sh.storage(ret_dict)
                _indentsToDict._index += 1
                for a,b in values:
                    sub = _indentsToDict(a, b)
                    if isinstance(sub, str):
                        ret_dict[sub] = ''
                    elif isinstance(sub, list):
                        ret_dict[sub[0]] = sub[1]
                    else:
                        ret_dict[a.rstrip(':')] = sub
                return ret_dict

        _indentsToDict._index = 0
        return _indentsToDict('root', indents) if len(indents) > 0 else {}

    def indentsToList(self, indents):

        def _indentsToList(key, values):
            if not values:
                if ':' not in key:
                    return str(key)
                else:
                    a,b,c = key.partition(':')
                    return [a.strip(), c.strip()]
            else:
                ret_list = []
                ret_dict = sh.storage()
                for a,b in values:
                    sub = _indentsToList(a, b)
                    if not b and isinstance(sub, list) and len(sub) == 2:
                        ret_dict[sub[0]] = sub[1]
                    else:
                        ret_list.append(sub)
                return [key, ret_dict] if ret_dict else [key, ret_list]

        root = _indentsToList('root', indents) if len(indents) > 0 else []
        return root[1] if root and len(root) == 2 and root[0]=='root' else root

    def toModel(self, list_or_dict, default_model=None):

        if default_model:
            assert isinstance(default_model, str)
            default_model = sh.model(default_model)

        def _toModel(ld):

            if isinstance(ld, str):
                ld = ld.strip()
                if ld.isdigit() and default_model:
                    return default_model.get(ld)
                else:
                    return ld
            elif isinstance(ld, (dict, sh.storage_class)) \
                    and ld.has_key('model') and ld.has_key('id') and ld.id.isdigit():
                 item = sh.model(ld.model).get(ld.id)
                 del ld['model'], ld['id']
                 if item: item.update(ld)
                 return item
            elif isinstance(ld, (list, tuple)) and len(ld) == 2 \
                    and isinstance(ld[0], str) \
                    and ld[0].isdigit() and default_model \
                    and isinstance(ld[1], (dict, sh.storage_class)):
                item = default_model.get(ld[0])
                if item: item.update(ld[1])
                return item
            elif isinstance(ld, list):
                items = map(_toModel, ld)
                return items if len(items) > 1 else items[0]
            elif hasattr(ld, 'items'):
                ret_dict = sh.storage()
                for k, v in ld.items():
                    k = k.strip()
                    if k.isdigit() and hasattr(v, 'items') \
                            and (default_model
                                or (v.has_key('model') and v.has_key('id')) 
                            ):
                        if v.has_key('model') and v.has_key('id'):
                            item = sh.model(v.model).get(v.id)
                            del v['model'], v['id']
                        else:
                            item = default_model.get(k)
                        if item: item.update(v)
                        ret_dict[k] = item
                    elif k.isdigit() and v == '' and default_model:
                        ret_dict[k] = default_model.get(k)
                    else:
                        ret_dict[k] = _toModel(v)
                return ret_dict
            else:
                raise u'未知的情况'

        if isinstance(list_or_dict, (tuple,list)) and not list_or_dict:
            return []
        res = _toModel(list_or_dict)
        if isinstance(list_or_dict, list) and not isinstance(res, list):
            res = [res]
        return res

    def contentToRefill(self, content):
        return self.refill(self.indent(content))

    def contentToList(self, content):
        return self.indentsToList(self.indent(content))

    def contentToDict(self, content, add_index=False):
        return self.indentsToDict(self.indent(content), add_index=add_index)
