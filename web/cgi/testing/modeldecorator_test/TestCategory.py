#coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()

class TestCategory(unittest.TestCase):

    def setUp(self):
        db.executeQuery('delete from %s' % 'ForTestCategory')
        db.executeQuery('delete from %s' % 'ForTestCategory2')
        db.executeQuery('delete from %s' % sh.model('Category').table_name)

    # 测试: insert update setCategory getCategory getAllCategory hasCategory addNewCategory
    def test_multi(self):
        model = sh.model('ForTestCategory')
        # 插入ForTestCategory
        new_id = model.insert(dict(title='python', cat='computer'))
        item = model.get(new_id)
        # 自动插入了Categoryid
        self.assertIsNotNone(item.category)
        self.assertEqual(item.category.name, 'computer')
        self.assertEqual(model.getCategory(new_id), 'computer')
        # 设置不存在的分类时抛出异常
        self.assertRaises(AssertionError, model.setCategory, new_id, 'psychics')
        # 但可以通过addCategory添加一个新分类
        model.addCategory('psychics')
        self.assertEqual(model.getCategory(new_id), 'computer')
        # 然后用setCategory设置
        model.setCategory(new_id, 'psychics')
        self.assertEqual(model.getCategory(new_id), 'psychics')
        # 用getAllCategory获得已有的两个分类
        self.assertEqual(model.getAllCategory(), ['computer', 'psychics'])
        # 可用hasCategory判断是否已有某分类
        self.assertTrue(model.hasCategory('computer'))
        self.assertTrue(model.hasCategory('psychics'))
        self.assertFalse(model.hasCategory('math'))
        # addNewCategory也可以添加分类，但是不能已存在
        model.addNewCategory('math')
        self.assertTrue(model.hasCategory('math'))
        self.assertRaises(AssertionError, model.addNewCategory, 'math')
        # 通过update可以自动设置新分类
        model.update(new_id, dict(cat='language'))
        self.assertEqual(model.getCategory(new_id), 'language')
        self.assertEqual(model.get(new_id).category.name, 'language')
        
    # 测试: delete removeCategory deleteCategory
    def test_multi2(self):
        model = sh.model('ForTestCategory')
        new_id_1 = model.insert(dict(title='python', cat='computer'))
        item_1 = model.get(new_id_1)
        new_id_2 = model.insert(dict(title='pascal', cat='computer'))
        # 使用removeCategory删除python的分类
        model.removeCategory(new_id_1)
        self.assertEqual(model.getCategory(new_id_1), None)
        self.assertIsNotNone(item_1.category)
        item_1 = model.get(new_id_1)
        self.assertIsNone(item_1.category)
        # 但是分类依然存在
        self.assertTrue(model.hasCategory('computer'))
        # item2的分类不受影响
        self.assertEqual(model.getCategory(new_id_2), 'computer')
        # 使用deleteCategory删除所有computer的分类
        model.deleteCategory('computer')
        self.assertFalse(model.hasCategory('computer'))
        # item2的分类也没了
        item_2 = model.get(new_id_2)
        self.assertEqual(item_2.Categoryid , 0)
        self.assertEqual(model.getCategory(new_id_2), None)
        # 给item2设置新分类，并删除item2数据
        model.update(new_id_2, dict(cat='old'))
        model.delete(new_id_2)
        # item2的分类依然存在
        self.assertTrue(model.hasCategory('old'))

    # 测试: get getsByCategory 
    def test_multi3(self):
        model = sh.model('ForTestCategory')
        new_id_1 = model.insert(dict(title='python', cat='computer'))
        new_id_2 = model.insert(dict(title='c++', cat='computer'))
        new_id_3 = model.insert(dict(title='wii', cat='game'))
        item = model.get(new_id_1)
        # getsByCategory能得到所有某个分类的数据
        items = model.getsByCategory('computer')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].category.name, 'computer')
        self.assertEqual(items[1].category.name, 'computer')
        self.assertEqual(items[0].id, new_id_1)
        self.assertEqual(items[1].id, new_id_2)
        
    def test_not_auto_new(self):
        model = sh.model('ForTestCategory2')
        # 插入ForTestCategory2
        new_id = model.insert(dict(title='c++', cat='computer'))
        item = model.get(new_id)
        # 当auto_set=False时，get并不会添加category_name
        self.assertNotIn('cat',  item.keys())
        # 因为auto_new=False, 所以没有自动插入Category
        self.assertEqual(item.catid, 0)
        # 如果先addCategory, 就会设置分类
        model.addCategory('computer')
        self.assertTrue(model.hasCategory('computer'))
        new_id_2 = model.insert(dict(title='perl', cat='computer'))
        item_2 = model.get(new_id_2)
        self.assertNotEqual(item_2.catid, 0)
        self.assertEqual(model.getCategory(new_id_2), 'computer')

    # 如果设置了auto_set=True, 则get all getOneByWhere等函数得到的item
    # 会自动把分类值赋值给data_key指定的字段
    def test_auto_set(self):
        model = sh.model('ForTestCategory')
        # 插入ForTestCategory2
        new_id = model.insert(dict(title='c++', cat='computer'))
        self.assertEqual(model.get(new_id).cat, 'computer')
        self.assertEqual(model.getOneByWhere('title=%s', 'c++').cat, 'computer')
        self.assertEqual(model.all()[0].cat, 'computer')
        self.assertEqual(model.gets([new_id])[0].cat, 'computer')
        

# 用于测试Category的类
from model import Model
class ForTestCategory(Model):
    table_name      = 'ForTestCategory'
    column_names    = ['Categoryid', 'title', ]
    test_decorator  = [
        ('Category',{'cat_id_key': 'Categoryid', 'cat_model_name': 'Category', 
            'data_key': 'cat', 'auto_new': True, 'auto_set': True}),
    ]
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Categoryid  int unsigned not null default 0,
            title       varchar(100)  charset utf8 not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''

class ForTestCategory2(ForTestCategory):
    table_name      = 'ForTestCategory2'
    column_names    = ['catid', 'title', ]
    test_decorator  = [
        ('Category',{'cat_id_key': 'catid', 'cat_model_name': 'Category', 
            'data_key': 'cat', 'auto_new': False, 'auto_set': False}),
    ]
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            catid       int unsigned not null default 0,
            title       varchar(100)  charset utf8 not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''

from .. import registerModel
registerModel(ForTestCategory)
registerModel(ForTestCategory2)
