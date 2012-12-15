#coding=utf-8
from Decorator import Decorator
import site_helper as sh

# 分类装饰，如果你想对你的数据进行简单分类，那么可以使用此装饰
# 此装饰的分类功能是基于分类名称的，而不强调分类的id，因此不提供与Categoryid有关的方法
# 你需要在你的model中添加cat_id_key指定的分类主键，它将对应到cat_model_name表的主键
# data_key是data中分类的属性名称，如果auto_new=True就会自动创建新分类,否则会忽略分类值
# 多个model的分类数据共同保存在Category表中,用data_name和data_id与其它表关联
# 你也可以通过get(id).category.name来得到分类名称

class Category(Decorator):
    ''' decorator = [
        ('Category',{'cat_id_key': 'Categoryid', 'cat_model_name': 'Category'
                     'data_key': 'category_name', 'auto_new': True}),
    ] '''

    # 插入data，并自动插入分类数据
    def insert(self, data):
        new_id = self.model.insert(data)
        self.__autoSetCategory(new_id, data.get(self.arguments.data_key, ''))
        return new_id

    # 更新data，并自动更新分类数据
    def update(self, item_id, data):
        self.__autoSetCategory(item_id, data.get(self.arguments.data_key, ''))
        return self.model.update(item_id, data)

    # 给model添加分类名称, 返回新分类id或已存在分类的id
    def addCategory(self, name):
        exists = self._getExistsCategory(name)
        return self.__insertCategory(name) if not exists else exists.id

    # 给model添加分类名称, 返回新分类id，若已存在则抛出异常
    def addNewCategory(self, name):
        exists = self._getExistsCategory(name)
        assert exists is None, '插入了重复的分类: %s %s' % (self.getModelTableName(), name)
        return self.__insertCategory(name)

    # 删除model的分类，并重置相关数据的分类id为0
    def deleteCategory(self, name):
        exists = self._getExistsCategory(name)
        ret = self.__getCatModel().delete(exists.id) if exists else 0
        query = self.replaceAttr('update {$table_name} set %s=0 where %s=%%s' % (self.arguments.cat_id_key, self.arguments.cat_id_key) )
        self.db.update(query, exists.id)
        return ret

    # 获得model的所有分类名称
    def getAllCategory(self):
        return [c.name for c in self.__getCatModel().all({'where': ('data_name=%s', [self.getModelTableName()])})]

    # 判断model是否已有莫个分类
    def hasCategory(self, name):
        return self._getExistsCategory(name) is not None

    # 获得数据的分类名
    def getCategory(self, item_id):
        item = self.get(item_id)
        return item.category.name if item and item.category else None

    # 设置数据的分类
    def setCategory(self, item_id, name):
        exists = self._getExistsCategory(name)
        assert exists is not None, '分类不存在: %s %s' % (self.getModelTableName(), name)
        return self.model.update(item_id, {self.arguments.cat_id_key: exists.id})

    # 取消数据的分类
    def removeCategory(self, item_id):
        return self.model.update(item_id, {self.arguments.cat_id_key: 0})

    # 根据分类名获得数据
    def getsByCategory(self, name):
        assert(isinstance(name, str) and len(name.strip()) > 0)
        cat_id = self.__getCategoryId(name)
        query = self.model.replaceAttr('select {$primary_key} from {$table_name} where %s=%%s' % self.arguments.cat_id_key)
        item_ids = self.model.db.fetchSomeFirst(query, [cat_id])
        return self.model.gets(item_ids)

    def __autoSetCategory(self, item_id, name):
        if name:
            if self.arguments.auto_new:
                self.addCategory(name)
            if self.hasCategory(name):
                self.setCategory(item_id, name)

    def __insertCategory(self, name):
        return self.__getCatModel().insert(dict( data_name = self.getModelTableName(), name = name ))

    def _getExistsCategory(self, name):
        assert(isinstance(name, str) and len(name.strip()) > 0)
        return self.__getCatModel().getOneByWhere('data_name=%s and name=%s', [self.getModelTableName(), name.strip()])

    def __getCatModel(self):
        return sh.model(self.arguments.cat_model_name)

    def __getCategoryId(self, name):
        exists = self._getExistsCategory(name)
        assert exists is not None, '分类不存在: %s %s' % (self.getModelTableName(), name)
        return exists.id
