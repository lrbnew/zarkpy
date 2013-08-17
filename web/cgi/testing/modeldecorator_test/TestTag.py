#coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()

class TestTag(unittest.TestCase):

    def setUp(self):
        db.executeQuery('delete from %s' % 'ForTestTag')
        db.executeQuery('delete from %s' % 'Tag')

    # 测试: insert update get all
    def test_multi_reset(self):
        # 给model添加reset tag功能
        decorator = [('Tag', dict(tag_model_name='Tag', data_key='tags', \
            split_char=' ', auto_operate='reset'))]
        model = sh.model('ForTestTag', decorator)
        # 插入一个带有标签的数据
        new_id = model.insert(dict(title='python', tags='lang computer simple'))
        # get得到的数据带有tags标签(无序)
        self.assertEqual(set(model.get(new_id).tags), set(['lang', 'computer', 'simple']))
        # 使用all得到的数据也有tags属性
        self.assertEqual(set(model.all()[0].tags), set(['lang', 'computer', 'simple']))
        # 更新tags
        model.update(new_id, dict(tags='fast \t  power   easy'))
        # 原有标签被替换
        self.assertEqual(set(model.get(new_id).tags), set(['fast', 'power', 'easy']))
        # 更新时不指定tags, 标签被保留
        model.update(new_id, dict(title='new title'))
        self.assertEqual(set(model.get(new_id).tags), set(['fast', 'power', 'easy']))
        # 使用空字符串更新tags, 标签被清空
        model.update(new_id, dict(tags=''))
        self.assertEqual(model.get(new_id).tags, [])

    # 测试: insert update get
    def test_multi_append(self):
        # 给model添加append tag功能
        decorator = [('Tag', dict(tag_model_name='Tag', data_key='ts', \
            split_char=',', auto_operate='append'))]
        model = sh.model('ForTestTag', decorator)
        # 插入一个带有标签的数据
        new_id = model.insert(dict(title='python', ts='lang, computer, simple'))
        # 更新tags
        model.update(new_id, dict(ts='lang,  fast, \t , power,   easy'))
        # 原有标签被保留
        self.assertEqual(set(model.get(new_id).tags),
                set(['lang', 'computer', 'simple', 'fast', 'power', 'easy']))
        # 使用空字符串更新tags, 标签被保留
        model.update(new_id, dict(ts=''))
        self.assertEqual(set(model.get(new_id).tags),
                set(['lang', 'computer', 'simple', 'fast', 'power', 'easy']))
        
    # 测试: addTag addTags resetTags getTags hasTag getsByTag gets
    def test_multi_tags(self):
        # reset tag model
        decorator = [('Tag', dict(tag_model_name='Tag', data_key='tags', \
            split_char=' ', auto_operate='reset'))]
        model = sh.model('ForTestTag', decorator)
        # 插入一个数据
        new_id = model.insert(dict(title='python', tags='lang'))
        # 使用addTag添加一个标签
        model.addTag(new_id, 'computer')
        self.assertEqual(set(model.get(new_id).tags), set(['lang', 'computer']))
        # 使用addTags添加多个标签
        model.addTags(new_id, ['simple', 'fast', 'power'])
        self.assertEqual(set(model.get(new_id).tags),
                set(['lang', 'computer', 'simple', 'fast', 'power']))
        # 使用getTags获得标签
        self.assertEqual(set(model.getTags(new_id)),
                set(['lang', 'computer', 'simple', 'fast', 'power']))
        # 用hasTag来判断某个item是否拥有某个标签
        self.assertTrue(model.hasTag(new_id, 'fast'))
        # 用removeTag删除一个tag
        model.removeTag(new_id, 'fast')
        self.assertFalse(model.hasTag(new_id, 'fast'))
        # 用resetTags重置标签
        model.resetTags(new_id, ['script', 'funny'])
        self.assertEqual(set(model.getTags(new_id)), set(['script', 'funny']))
        # 用getsByTag根据标签获得数据带tags
        new_id_2 = model.insert(dict(title='shell', tags='script'))
        self.assertEqual(set(model.getTags(new_id_2)), set(['script']))
        new_id_3 = model.insert(dict(title='c++', tags='compiled'))
        items = model.getsByTag('script')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].id, new_id)
        self.assertEqual(items[1].id, new_id_2)
        self.assertEqual(set(items[0].tags), set(['script', 'funny']))
        self.assertEqual(set(items[1].tags), set(['script']))
        # 用gets获得数据带tags
        items = model.gets([new_id, new_id_2, new_id_3])
        self.assertEqual(set(items[0].tags), set(['script', 'funny']))
        self.assertEqual(set(items[1].tags), set(['script']))
        self.assertEqual(set(items[2].tags), set(['compiled']))

    # 测试: delete removeTag 
    def test_multi_delete(self):
        # reset tag model
        decorator = [('Tag', dict(tag_model_name='Tag', data_key='tags', \
            split_char=' ', auto_operate='reset'))]
        model = sh.model('ForTestTag', decorator)
        tag_model = sh.model('Tag')
        # 插入一个数据
        new_id_1 = model.insert(dict(title='python', tags='script'))
        new_id_2 = model.insert(dict(title='c++', tags='compiled'))
        # Tag表保存了相关数据
        tag_items = tag_model.all()
        self.assertEqual(len(tag_items), 2)
        self.assertEqual(tag_items[0].name, 'script')
        self.assertEqual(tag_items[1].name, 'compiled')
        # 删除这个数据, Tag表中的数据也被删除
        model.delete(new_id_1)
        tag_items = tag_model.all()
        self.assertEqual(len(tag_items), 1)
        self.assertEqual(tag_items[0].name, 'compiled')
        # 使用removeTag删除标签，Tag表中的数据也被删除
        model.removeTag(new_id_2, 'compiled')
        self.assertFalse(model.hasTag(new_id_2, 'compiled'))
        self.assertEqual(tag_model.all(), [])
        # 每个标签在Tag表中保存一个记录
        model.insert(dict(title='shell', tags='power complex cool'))
        self.assertEqual(len(tag_model.all()), 3)

# 用于测试Tag的类
from model import Model
class ForTestTag(Model):
    table_name      = 'ForTestTag'
    column_names    = ['title']
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            title       varchar(100)  charset utf8 not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''

from .. import registerModel
registerModel(ForTestTag)
