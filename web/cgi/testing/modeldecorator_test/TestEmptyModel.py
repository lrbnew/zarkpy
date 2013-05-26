#coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()
user_model = sh.model('User', [('EmptyModel', {})])

class TestEmptyModel(unittest.TestCase):

    def setUp(self):
        db.executeQuery('delete from %s' % user_model.table_name)

    # 对传入的None数据改成Empty
    def test_noneToEmpty(self):
        item = user_model.noneToEmpty(None)
        # 所有出现在column_names中的字段都为''
        for name, ct in user_model.getColumnTypes().items():
            if name[0] != '_':
                if ct.has_key('default'):
                    self.assertEqual(item.get(name), ct.default)
                else:
                    self.assertEqual(item.get(name), '')
        # 可以通过__is_empty来判断是否为空数据
        self.assertTrue(item.get('__is_empty') is True)
        # noneToEmpty也可以传入data列表, 只有is None时才返回Empty
        items = user_model.noneToEmpty([{}, None, sh.storage()])
        self.assertTrue(items[0].get('__is_empty', False) is False)
        self.assertTrue(items[1].get('__is_empty', False) is True)
        self.assertTrue(items[2].get('__is_empty', False) is False)

    # 可以通过getEmptyData直接得到一个Empty
    def test_getEmptyData(self):
        item = user_model.getEmptyData()
        for name, ct in user_model.getColumnTypes().items():
            if name[0] != '_':
                if ct.has_key('default'):
                    self.assertEqual(item.get(name), ct.default)
                else:
                    self.assertEqual(item.get(name), '')
        self.assertTrue(item.get('__is_empty') is True)
