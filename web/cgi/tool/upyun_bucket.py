#!/usr/bin/env python
#coding=utf-8
import sys
import upyun_api
v = sys.argv

if __name__ == '__main__':

    if len(v) < 2 or v[1] not in ['show', 'rm', 'size', 'info', ]:
        print 'Usage: python tool/upyun_bucket.py show bucket_name path'
        print 'Usage: python tool/upyun_bucket.py size bucket_name path'
        print 'Usage: python tool/upyun_bucket.py rm bucket_name path'
    else:
        ins = upyun_api.UpYun(v[2], 'sdjl', 'dc1172261d0a30e0c475271aaf73fdd98a')
        ins.setApiDomain('v0.api.upyun.com')
        ins.debug = True

        if v[1] == 'show':
            print ins.getList(v[3]).read()

        elif v[1] == 'rm':

            def _del(p):
                r = ins.getFileInfo(p)
                if r['type'] == 'folder':
                    for i in [j.partition('\t')[0] for j in ins.getList(p).read().split('\n')]:
                        _del(p.rstrip('/') + '/' + i )
                ins.delete(p)
                print 'delete', p

            _del(v[3].rstrip('/'))

        elif v[1] == 'size':
            size = ins.getBucketUsage(v[3])
            if size > 1024 * 1024 * 1024:
                print '%.2f GB' % float((size) / (1024 * 1024 * 1024))

            elif size > 1024 * 1024:
                print '%.2f MB' % float((size) / (1024 * 1024))

            else:
                print '%.2f KB' % float((size) / 1024)

        elif v[1] == 'info':
            print ins.getFileInfo(v[3])

