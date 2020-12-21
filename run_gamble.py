#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from generate_data import *
from trial_func import *
from Table_class import *

# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('姓名:')
myDlg.addField('性别:', choices=['male', 'female'])
myDlg.addField('年龄:', 21)
myDlg.addField('分组:', choices=['A', 'B', 'C', 'D'])
# A: expand, B: shrink, C: large, D: small
myDlg.addField('屏幕分辨率:', choices=['1920*1080', '3200*1800', '1280*720', '2048*1152', '2560*1440'])
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]
exp_num = ok_data[3]
resolution = ok_data[4]
conditions = {
    'A': 'expand',
    'B': 'shrink',
    'C': 'large',
    'D': 'small'
}
condition = conditions[exp_num]
w, h = resolution.split('*')
w = int(w)
h = int(h)

df = generate(condition=condition)
df_tr = generate_train(condition=condition)
df['pix_w'] = w
df['pix_h'] = h

results = {
    'id': [], 'first_upper': [], 'first_lower': [], 'upper': [], 'lower': [],
    'rt1': [], 'rt2': [], 'mirror': [], 'inverse': []
    }
result_tr = {'id': [], 'rt': [], 'first_upper': [], 'first_lower': [], 'upper': [], 'lower': []}

win = visual.Window(size=(w, h), fullscr=True, units='pix', color=[0, 0, 0])

card_pos = [[0 for j in range(3)] for i in range(7)]
table = [[0 for j in range(3)] for i in range(7)]
value = [[0 for j in range(3)] for i in range(7)]
gou_pos = [[0 for j in range(3)] for i in range(7)]
a = 3*w / 20.
b = h / 12.

# 各表格位置
for i in range(7):
    for j in range(3):
        x1 = j * a - a
        x2 = j * a
        y1 = 4 * b - i * b
        y2 = 3 * b - i * b
        card_pos[i][j] = ([[x1, y1], [x1, y2], [x2, y2], [x2, y1]])
        gou_pos[i][j] = ([int((x1 + x2) / 2), int((y1 + y2) / 2)])
# 建立表格对象
title_text = [u"抽奖券", u"选择抽奖券", u"选择固定金额", u"固定金额"]
jq_head = Table(visual.TextStim(win, height=h / 36),
                visual.ShapeStim(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2),
                visual.ImageStim(win),
                [[-2 * a, 4 * b], [-2 * a, 3 * b], [-a, 3 * b], [-a, 4 * b]])
jq_head.txt.text = title_text[0]
table_jq = Table(visual.TextStim(win, text='奖券', height= h / 25, bold=True),
                 visual.ShapeStim(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2),
                 visual.ImageStim(win),
                 [[-2 * a, 3 * b], [-2 * a, -3 * b], [-a, -3 * b], [-a, 3 * b]])

for m in range(7):
    for n in range(3):
        table[m][n] = Table(visual.TextStim(win, height=h / 30, bold=True),
                            visual.ShapeStim(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2),
                            visual.ImageStim(win, image="img/gou.png", size=32 * h / 720),
                            card_pos[m][n])
        if m == 0:
            table[m][n].txt.text = title_text[n + 1]
            table[m][n].txt.height = h / 36
tables = [jq_head, table_jq, table]
# Confirm button
ok = visual.TextStim(win, text=u"确认", pos=(0, -4.5 * b), height=h / 36)
ok_shape = visual.ShapeStim(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2)
ok_shape.vertices = [[-0.5 * a, -5 * b], [-0.5 * a, -4 * b], [0.5 * a, -4 * b], [0.5 * a, -5 * b]]
buttons = [ok, ok_shape]
# 时间间隔
t_trial = {'t_fix': 0.5}
# 文本
txt = visual.TextStim(win, height=64 * h / 720, pos=(-w/4, 0))
text_timeout = visual.TextStim(win, height=64 * h / 720, color='red')
txt_time = [text_timeout, txt]
# 注视点
fix = visual.ImageStim(win, image="img/fix.png", size=64 * h / 720)
# 指导语
pic = visual.ImageStim(win, size=(w, h))

clk = core.Clock()
myMouse = event.Mouse()
# 指导语
while True:
    for i in range(2):
        pic.image = 'img/introduction_%s.png' % (i + 1)
        pic.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        event.clearEvents()
    txt.text = '按【空格键】进入决策实验练习'
    txt.draw()
    win.flip()
    key = event.waitKeys(keyList=['space', 'escape'])
    if 'space' in key:
        event.clearEvents()
        break
    event.clearEvents()
# training
for i in range(len(df_tr)):
    trial(i, win, df_tr, clk, tables, buttons, txt_time, myMouse=myMouse, time_feedback=True)
    core.wait(0.5)
txt.pos = (-w/4, 0)
txt.text = '按【空格键】进入正式实验'
txt.draw()
win.flip()
key = event.waitKeys(keyList=['space', 'escape'])
# trial
timeout_trial = []
timeout_marker = np.zeros(len(df))
for i in range(len(df)):
    result = trial(i, win, df, clk, tables, buttons, txt_time, myMouse=myMouse)
    print(result)
    results['id'].append(i)
    results['rt1'].append(result['rt1'])
    results['rt2'].append(result['rt2'])
    results['mirror'].append(result['mirror'])
    results['inverse'].append(result['inverse'])
    results['first_lower'].append(result['first_lower'])
    results['first_upper'].append(result['first_upper'])
    results['lower'].append(result['lower'])
    results['upper'].append(result['upper'])

    if (result['rt1']+result['rt2']<5.5) or (result['rt1']<2.5) or (result['rt2']<2.5):
        txt.text = '反应过快！请认真反应'
        timeout_trial.append(i)
        timeout_marker[i] = -1
        txt.draw()
        win.flip()
    elif result['lower'] == -1:
        # whether subjects run out of times
        timeout_trial.append(i)
        timeout_marker[i] = 1
    core.wait(0.5)

    if i in (np.array([1,2,3])*44-1):
        # timeout_trial
        for each in timeout_trial:
            result = trial(each, win, df, clk, tables, buttons, txt_time, myMouse=myMouse)
            results['rt1'][each] = result['rt1']
            results['rt2'][each] = result['rt2']
            results['mirror'][each] = result['mirror']
            results['inverse'][each] = result['inverse']
            results['first_lower'][each] = result['first_lower']
            results['first_upper'][each] = result['first_upper']
            results['lower'][each] = result['lower']
            results['upper'][each] = result['upper']
            if result['upper'] == -1:
                timeout_trial.append(each)
        timeout_trial = []
        txt.text = '请休息一下（20s后方可按空格键继续）'
        txt.draw()
        win.flip()
        core.wait(20)
        key = event.waitKeys(keyList=['space', 'escape'])

txt.text = "本试次结束，请呼叫主试"
txt.draw()
win.flip()
df['name'] = name
df['sex'] = sex
df['age'] = age
df['trial'] = results['id']
df['mirror'] = results['mirror']
df['inverse'] = results['inverse']
df['rt1'] = results['rt1']
df['rt2'] = results['rt2']
df['first_lower'] = results['first_lower']
df['first_upper'] = results['first_upper']
df['lower'] = results['lower']
df['upper'] = results['upper']
df['isTimeout'] = timeout_marker
df.to_csv('exp_data\\%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))

core.wait(3)
win.close()
core.quit()