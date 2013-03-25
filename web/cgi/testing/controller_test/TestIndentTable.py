#!coding=utf-8
# ../../controller/IndentTable.py
import unittest
import site_helper as sh
t_ctrl = sh.ctrl('IndentTable')
db = sh.getDBHelper()

class TestIndentTable(unittest.TestCase):

    def setUp(self):
        model = sh.model('SiteConfig')
        # 使用truncate是为了每个test中SiteConfigid从1开始
        db.executeQuery('truncate %s' % model.table_name)
        model.insert({'name': 'n1', 'value': 'v1', 'title': 't1'})
        model.insert({'name': 'n2', 'value': 'v2', 'title': 't2'})
        model.insert({'name': 'n3', 'value': 'v3', 'title': 't3'})

    def test_indent_1(self):
        source = '''
        aaa
            bb
            cc
        '''

        target = [
            ['aaa',[
                ['bb',[]],
                ['cc',[]]
            ]],
        ]

        self.assertEqual(t_ctrl.indent(source), target)

    def test_indent_2(self):
        source = '''
        aaa
            bb
            cc  :   efg 
        dd
        '''

        target = [
            ['aaa',[
                ['bb',[]],
                ['cc  :   efg',[]]
            ]],
            ['dd',[]]
        ]

        self.assertEqual(t_ctrl.indent(source), target )

    def test_indent_3(self):
        source = '''
        aaa
            bb
            cc
        ddd
            ee
                ff
            gg
            hh
        ll
        '''

        target = [
            ['aaa',[
                ['bb',[]],
                ['cc',[]]
            ]],
            ['ddd', [
                ['ee',[
                    ['ff',[]]
                ]],
                ['gg', []],
                ['hh', []]
            ]],
            ['ll',[]]
        ]

        self.assertEqual(t_ctrl.indent(source), target )

    def test_indent_4(self):
        source = '''
        aaa
            bb
                lyh
                ll
            cc
        ddd
            ee
                ff
            gg
                jj
                k


        ll

            887

        99
            
        '''

        target = [
            ['aaa',[
                ['bb',[
                    ['lyh',[]],
                    ['ll',[]],
                ]],
                ['cc',[]]
            ]],
            ['ddd', [
                ['ee',[
                    ['ff',[]]
                ]],
                ['gg', [
                    ['jj',[]],
                    ['k',[]],
                ]],
            ]],
            ['ll',[
                ['887', []],
            ]],
            ['99',[]],
        ]

        self.assertEqual(t_ctrl.indent(source), target )

    def test_indent_5(self):
        source = ''
        target = []
        self.assertEqual(t_ctrl.indent(source), target )

        source = '''1'''
        target = [['1', []]]
        self.assertEqual(t_ctrl.indent(source), target )

        source = '''
        1
        2
        3
        '''
        target = [
            ['1', []],
            ['2', []],
            ['3', []],
        ]
        self.assertEqual(t_ctrl.indent(source), target )

    def test_refill(self):
        source = '''
        aaa
            bb
                lyh
                ll
            cc
        ddd
            ee
                ff
            gg
                jj
                k


        ll

            888

        99
            
        '''

        target = [
            ['aaa'],
            ['aaa','bb'],
            ['aaa','bb','lyh'],
            ['aaa','bb','ll'],
            ['aaa','cc'],
            ['ddd'],
            ['ddd','ee'],
            ['ddd','ee','ff'],
            ['ddd','gg'],
            ['ddd','gg','jj'],
            ['ddd','gg','k'],
            ['ll'],
            ['ll','888'],
            ['99'],
        ]

        indent = t_ctrl.indent(source)
        self.assertEqual(t_ctrl.refill(indent), target)

        # 测试contentToRefill集合了indent和refill
        self.assertEqual(t_ctrl.contentToRefill(source), target)


    def test_indentsToDict(self):
        source = '''
        aaa
            bb: BB
            cc: CC
        ddd
            ee:
                ff
            gg
            hh:
        ll
        '''

        
        target = sh.storage({
            'aaa': sh.storage({
                    'cc': 'CC',
                    'bb': 'BB'}),
            'ddd': sh.storage({
                    'ee': sh.storage({'ff': ''}), # toDict时，冒号可写可不写
                    'gg': '',
                    'hh': ''}),
            'll' : '',
            })


        indents = t_ctrl.indent(source)
        results = t_ctrl.indentsToDict(indents)
        self.assertEqual(results, target)
        self.assertEqual(type(results.aaa), sh.storage_class)

        # 测试contentToDict集合了indent和indentsToDict
        self.assertEqual(t_ctrl.contentToDict(source), target)



    # 当使用add_index=True时就会给值添加index，用于需要顺序处理的情况
    # 比如下面的aaa的序号等于1, 此时应该让所有key都应该有值
    def test_indentsToDict_addIndex(self):
        source = '''
        aaa
            bb: BB
            cc: CC
        ddd
            ee
                ff
            gg
            hh:
        ll
        '''

        target = sh.storage({
            '__index' : 0,
            'aaa': sh.storage({
                    '__index' : 1, 
                    'cc': 'CC',
                    'bb': 'BB'}),
            'ddd': sh.storage({
                    '__index' : 2,
                    'ee': sh.storage({
                        '__index' : 3,
                        'ff': ''}),
                    'gg': '',
                    'hh': ''}), # toDict时，key后面的冒号可有可无
            'll' : '',
            })

        indents = t_ctrl.indent(source)
        results = t_ctrl.indentsToDict(indents, add_index=True)
        self.assertEqual(results, target)

    def test_indentsToList(self):
        source = '''
        aaa
            bb: BB
            cc: CC
        ddd
            ee
                ff
            gg
            hh:
                ii
                    jj: kk
        ll
        '''

        target = [
            ['aaa', sh.storage({
                'bb': 'BB',
                'cc': 'CC'})],
            ['ddd', [
                ['ee', 
                    ['ff']],
                'gg',
                ['hh:', # toList时冒号不是可选的
                    [['ii', sh.storage({ # dict(storage)仅会出现在叶子节点上
                        'jj': 'kk'})] # 出现key value对时转为dict
                    ]
                ]]
            ],
            'll'
        ]

        indents = t_ctrl.indent(source)
        results = t_ctrl.indentsToList(indents)
        self.assertEqual(results, target)
        self.assertEqual(type(results[0][1]), sh.storage_class)

        # 测试contentToList集合了indent和indentsToList
        self.assertEqual(t_ctrl.contentToList(source), target)


    def test_indentsToList_2(self):
        source_1 = '''aa\nbb\ncc'''
        source_2 = '''
        aa
        bb
        cc
        '''

        target = [
            ['aa',[]],
            ['bb',[]],
            ['cc',[]],
        ]

        self.assertEqual(t_ctrl.indent(source_1), target)
        self.assertEqual(t_ctrl.indent(source_2), target)
        self.assertEqual(t_ctrl.indent(source_1), t_ctrl.indent(source_2))

        list_target =  ['aa', 'bb', 'cc' ]
        list_results = t_ctrl.indentsToList(t_ctrl.indent(source_1))
        self.assertEqual(list_results, list_target)

    def test_indentsToList_3(self):
        source = ''
        target = []
        self.assertEqual(t_ctrl.contentToList(source), target)


    # 使用toModel可以直接用id列表获得items
    def test_toModel_widthIndentList_1(self):
        source = '''
        1
        2
        3
        '''

        indents = t_ctrl.indent(source)
        list_results = t_ctrl.indentsToList(indents)
        items = t_ctrl.toModel(list_results, default_model='SiteConfig')

        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].name, 'n1')
        self.assertEqual(items[2].value, 'v3')
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 1)


    # 可以重新指定属性值
    def test_toModel_widthIndentList_2(self):
        source = '''
        1
            name: na
        2
            value: vb
        '''

        indents = t_ctrl.indent(source)
        list_results = t_ctrl.indentsToList(indents)
        items = t_ctrl.toModel(list_results, default_model='SiteConfig')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, 'na')
        self.assertEqual(items[0].value, 'v1')
        self.assertEqual(items[1].name, 'n2')
        self.assertEqual(items[1].value, 'vb')
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 2)


    # 可以混合使用
    def test_toModel_widthIndentList_3(self):
        source = '''
        1
            name: na
        2
            value: vb

        aa
            bb
                cc: dd

            ee
            ff
                3
                    name: nc
        '''

        last_target = [
            'aa',
                [['bb', sh.storage({'cc': 'dd'})],
                  'ee',
                  ['ff', sh.storage({'name': 'nc',  'SiteConfigid': 3L,  'value': 'v3', 'title': 't3'})]
                ]
        ]

        indents = t_ctrl.indent(source)
        list_results = t_ctrl.indentsToList(indents)
        items = t_ctrl.toModel(list_results, default_model='SiteConfig')
        items = sh.removePrivateValues(items)

        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].name, 'na')
        self.assertEqual(items[0].value, 'v1')
        self.assertEqual(items[1].name, 'n2')
        self.assertEqual(items[1].value, 'vb')
        self.assertEqual(items[2], last_target)
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 4)


    # 不指定default_model的话，id就视为字符串
    def test_toModel_widthIndentList_4(self):
        source = '''
        1

            name: na
        2
            value: vb
        aa
            bb
                cc: dd
            ee
            ff
                3

                    name: nc
        '''

        target = [
            ['1', sh.storage({'name': 'na'})],
            ['2', sh.storage({'value': 'vb'})],
            ['aa', [
                ['bb', sh.storage({'cc': 'dd'})],
                'ee',
                ['ff', 
                    ['3', sh.storage({'name': 'nc'})]]
                ]
            ]
        ]

        indents = t_ctrl.indent(source)
        list_results = t_ctrl.indentsToList(indents)
        self.assertEqual(t_ctrl.toModel(list_results), target )
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 4)
        
    def test_toModel_widthIndentList_5(self):
        source = ''
        items = t_ctrl.toModel(t_ctrl.contentToList(source), default_model='SiteConfig')
        self.assertEqual(items, [])


    def test_toModel_widthIndentList_6(self):
        source = '1'
        items = t_ctrl.toModel(t_ctrl.contentToList(source), default_model='SiteConfig')
        self.assertTrue(isinstance(items, list))

    # 可以自定义model name, 也可混合使用
    def test_toModel_widthIndentList_7(self):
        source = '''
        1
            id: 1
            model: SiteConfig
            name: na
        2
            value: vb
        aa
            3
                id: 2
                model: SiteConfig
                name: nc
        '''

        target = [
            ['1', sh.storage({
                'SiteConfigid': 1L,
                'value': 'v1',
                'name': 'na',
                'title': 't1',
                })
            ],
            ['2', sh.storage({'value': 'vb'})],
            ['aa', [
                '3', sh.storage({
                    'SiteConfigid': 2L,
                    'value': 'v2',
                    'name': 'nc',
                    'title': 't2',
                    })
                ]
            ]
        ]

        indents = t_ctrl.indent(source)
        list_results = t_ctrl.indentsToList(indents)
        items = t_ctrl.toModel(list_results)
        items = sh.removePrivateValues(items)
        self.assertEqual(items, target)
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 3)


    def test_toModel_widthIndentDict_1(self):
        source = '''
        1
            name: na
        2
            value: vb
            title: append title
        aa
            bb
                cc: dd

            ee
            ff:
                gg
            hh

                3
                    name: nc
        '''

        target = sh.storage({
            '1': sh.storage({
                'name': 'na',
                'SiteConfigid': 1L,
                'value': 'v1',
                'title': 't1',
                }),
            '2': sh.storage({
                'name': 'n2',
                'SiteConfigid': 2L,
                'value': 'vb',
                'title': 'append title', # 也可以添加model columns之外的值
                }),
            'aa': sh.storage({
                'bb': sh.storage({'cc': 'dd'}),
                'ee': '',
                'ff': sh.storage({'gg': ''}),
                'hh': sh.storage({
                    '3': sh.storage({
                        'name': 'nc',
                        'SiteConfigid': 3L,
                        'value': 'v3',
                        'title': 't3',
                    })})
                }),
        })

        indents = t_ctrl.indent(source)
        dict_results = t_ctrl.indentsToDict(indents)
        items = t_ctrl.toModel(dict_results, default_model='SiteConfig')
        items = sh.removePrivateValues(items)
        self.assertEqual(items, target)
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 4)

    # 不指定default_model时, 数字当做普通字符串处理
    def test_toModel_widthIndentDict_2(self):
        source = '''
        1
            name: na
        2
            value: vb
        aa
            bb
                cc: dd

            ee
            ff:
                gg
            hh

                3
                    name: nc
        '''

        target = sh.storage({
            '1': sh.storage({'name': 'na'}),
            '2': sh.storage({'value': 'vb'}),
            'aa': sh.storage({ # dict(storage)可以出现在非叶子节点
                'bb': sh.storage({'cc': 'dd'}),
                'ee': '',
                'ff': sh.storage({'gg': ''}),
                'hh': sh.storage({
                    '3': sh.storage({
                        'name': 'nc'})
                }),
            }),
        })

        indents = t_ctrl.indent(source)
        dict_results = t_ctrl.indentsToDict(indents)
        items = t_ctrl.toModel(dict_results)
        self.assertEqual(items, target)
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 4)

    # 可以自定义model name, 优先级高于default_model
    def test_toModel_widthIndentDict_3(self):
        c_model = sh.model('Category')
        new_id_1 = c_model.insert({'data_name': 'd', 'name': 'n'})
        new_id_2 = c_model.insert({'data_name': 'd2', 'name': 'n2'})

        source = '''
        a
            id: 1
            model: SiteConfig
            name: na
        %d
            name: over write name
        %d
            name: forget id
            model: SiteConfig
        aa
            3
                id: 2
                model: SiteConfig
                name: nc
        ''' % (new_id_1, new_id_2)

        target = sh.storage({
            'a': sh.storage({ # 因为%d可能为1，但dict中要求key唯一，所以用a代替
                'SiteConfigid': 1L,
                'value': 'v1',
                'name': 'na',
                'title': 't1',
                }),
            str(new_id_1): sh.storage({
                'Categoryid': new_id_1, # 不显示指定model时，用default_model
                'data_name': 'd',
                'name': 'over write name',
                }),
            str(new_id_2): sh.storage({
                'Categoryid': new_id_2, # 必须同时指定model与id才认为是SiteConfig
                'data_name': 'd2',
                'name': 'forget id',
                'model': 'SiteConfig',
                }),
            'aa': sh.storage({
                    '3': sh.storage({
                        'SiteConfigid': 2L,
                        'value': 'v2',
                        'name': 'nc',
                        'title': 't2',
                    }),
                }),
        })

        indents = t_ctrl.indent(source)
        dict_results = t_ctrl.indentsToDict(indents)
        items = t_ctrl.toModel(dict_results, default_model='Category')
        items = sh.removePrivateValues(items)
        self.assertEqual(items, target)
        self.assertEqual(t_ctrl.getIndentsLevel(indents), 3)

    def test_toModel_widthIndentDict_4(self):
        source = '1'
        target = sh.storage({
            '1': sh.storage({
                'name': 'n1',
                'SiteConfigid': 1L,
                'value': 'v1',
                'title': 't1',
                }),
        })
        items = t_ctrl.toModel(t_ctrl.contentToDict(source), default_model='SiteConfig')
        items = sh.removePrivateValues(items)
        self.assertEqual(items, target)


    # 计算list indents的最大缩进层级数
    def test_getListLevel(self):
        level_1 = '''
        1

        2
        3
        '''
        self.assertEqual(t_ctrl.getIndentsLevel(t_ctrl.indent(level_1)), 1)

        level_2 = '''
        1

        2
            4
        3
            5
            6
        '''
        self.assertEqual(t_ctrl.getIndentsLevel(t_ctrl.indent(level_2)), 2)

        level_3 = '''
        1

        2
                        4
        3
            5
                7
                8
            6
        '''
        self.assertEqual(t_ctrl.getIndentsLevel(t_ctrl.indent(level_3)), 3)

        level_4 = '''
        1
            9
                10
                    11
        2
            4
        3

            5
                    7
                    8
            6
        '''
        self.assertEqual(t_ctrl.getIndentsLevel(t_ctrl.indent(level_4)), 4)

    # 可以使用indentsToConfig把indents逆转为字符配置表
    def test_indentsToConfig(self):
        source = '''
        a
            id:    1
            model: SiteConfig    
            name:  na

        b
                name: over write name
        c
              name:      forget id      
              model  : SiteConfig \n
        '''
        target = '''
a
    id:    1
    model: SiteConfig
    name:  na
b
    name: over write name
c
    name:      forget id
    model  : SiteConfig
    '''
        indents = t_ctrl.indent(source)
        self.assertEqual(t_ctrl.indentsToConfig(indents), target.strip())
