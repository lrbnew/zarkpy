#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
ios_markers = ['ios', 'ipad', 'iphone']
android_markers = ['android', 'adr']
wp_markers = ['windows phone', 'wp7']
qq_markers = ['mqqbrowser']
uc_markers = ['uc', 'UC']

def device():
    ua = web.ctx.env.get('HTTP_USER_AGENT', '')
    ua = ua.lower()
    for i in android_markers:
        if i in ua:
            return 'android'

    for i in ios_markers:
        if i in ua:
            return 'ios'

    for i in wp_markers:
        if i in ua:
            return 'wp'

    return 'other'

def browser():
    ua = web.ctx.env.get('HTTP_USER_AGENT', '')
    ac = web.ctx.env.get('HTTP_ACCEPT', '')
    ua = ua.lower()
    for i in uc_markers:
        if i in ac + ua:
            return 'uc'
    for i in qq_markers:
        if i in ua:
            return 'qq'
    return 'other'

