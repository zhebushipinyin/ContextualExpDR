#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import numpy as np


def trial(i, win, df, clk, tables, buttons, txt, myMouse=None, time_feedback=False):
    """
    Run a trial of given data
    Returns the values recorded

    Parameters
    ----------
    i : int
        trial number
    win : visual.Window
        windows created by psychopy
    df : pd.DataFrame
        Exp data contains gambles and conditions
    clk : core.Clock
        clock to record time
    tables: list
        list contains Table objects, [jq_head, table_jq, table]
    buttons: list
        list contains elements for buttons, [visual.TextStim, visual.ShapeStim]
    txt: list
        feedback for timeout, [visual.TextStim, visual.TextStim]
    myMouse: event.Mouse
        mouse object
    time_feedback: bool
        whether or not to give time feed back, default is False

    Returns
    -------
    result : list
    """
    if myMouse is None:
        myMouse = event.Mouse()
    inverse, mirror = np.random.randint(0, 2, 2)
    # inverse, mirror = (0, 0)
    p = df.loc[i, 'p']
    x = df.loc[i, 'x1']
    y = df.loc[i, 'x2']
    t_bound = 20
    timeout = txt[0]
    time_txt = txt[1]
    if time_feedback:
        time_txt.pos = (0, win.size[1]*3/8)
    result = {
        'inverse':inverse,
        'mirror':mirror
    }

    jq_head = tables[0]
    table_jq = tables[1]
    table = tables[2]
    table_jq.txt.text = "%s%%，%s元\n%s%%，%s元" % (int(100 * p), int(x), 100 - int(100 * p), int(y))
    state = 'running'
    x1 = x
    y1 = y
    click_flag = 0
    for flag in range(2):
        event.clearEvents()
        col = [0] * 2
        col[0] = [x - k * (x - y) / 5 for k in range(6)]
        if flag == 1:
            col[1] = [x1 - k * (x1 - y1) / 5 for k in range(6)]
        col_p = col[flag]
        value = [[0 for j in range(3)] for k in range(7)]
        clk.reset()
        while True:
            if time_feedback:
                time_txt.text = t_bound-int(np.round(clk.getTime()))
                time_txt.draw()
            if clk.getTime() > t_bound:
                if flag == 0:
                    result['first_upper'] = -1
                    result['first_lower'] = -1
                    result['upper'] = -1
                    result['lower'] = -1
                    result['rt1'] = t_bound
                    result['rt2'] = t_bound
                    result['rt'] = -1
                else:
                    result['upper'] = -1
                    result['lower'] = -1
                    result['rt2'] = t_bound
                timeout.text = '超时！'
                timeout.draw()
                win.flip()
                core.wait(0.3)
                state = 'quit'
                break
            if state == 'running':
                for k in range(1, 7):
                    for j in range(2):
                        table[k][j].t(mirror, inverse)
                        if value[k][j] == 1:
                            table[k][j].dui.draw()
                        if myMouse.isPressedIn(table[k][j].shape) and value[k][j] == 0:
                            if click_flag == 0:
                                rt_think = clk.getTime()
                                click_flag = 1
                            value[k] = [0] * 3
                            value[k][j] = 1
                            table[k][j].dui.draw()
                        table[k][j].shape.draw()
                    table[k][2].t(mirror, inverse)
                    table[k][2].shape.draw()
                    table[k][2].txt.text = u"%s元" % int(col_p[k-1])
                    table[k][2].txt.draw()
                for j in range(3):
                    table[0][j].t(mirror)
                    table[0][j].shape.draw()
                    table[0][j].txt.draw()
                jq_head.t(mirror)
                table_jq.t(mirror)
                jq_head.shape.draw()
                table_jq.shape.draw()
                jq_head.txt.draw()
                table_jq.txt.draw()
                key = event.getKeys(["escape"])
                if "escape" in key:
                    state = "exit"

                check = [0] * (7 - 1)
                now = [0] * (7 - 1)
                point = 0
                for k in range(1, 7):
                    point += value[k][0] + value[k][1]
                    if value[k][1] == 1:
                        now[k - 1] = 1
                j = 0
                while j <= 5:
                    if value[j + 1][1] == 1:
                        check[j] = 1
                    else:
                        break
                    j += 1
                if check == now and point == 6:
                    if flag==0 and (sum(check) in [0, 6]):
                        pass
                    else:
                        if buttons[1].contains(myMouse):
                            buttons[1].fillColor = [-1, -1, -1]
                            buttons[1].opacity = 0.3
                        else:
                            buttons[1].fillColor = [0, 0, 0]
                            buttons[1].opacity = 1
                        buttons[1].draw()
                        buttons[0].draw()
                win.flip()
                # 获得被试所选转折点
                if check == now and myMouse.isPressedIn(buttons[1]) and point == 6:
                    rt = clk.getTime()
                    col_v = [col_p[0]] + col_p + [col_p[-1]]
                    change = sum(check)
                    x1 = col_v[change]
                    y1 = col_v[change+1]
                    if flag == 0:
                        result['first_upper']=x1
                        result['first_lower']=y1
                        result['rt1'] = rt
                        result['rt'] = rt_think
                    else:
                        result['upper']=x1
                        result['lower']=y1
                        result['rt2'] = rt
                    # 标记为第二轮
                    state = "quit"
                    event.clearEvents()
            # 进入下一层
            if state == "quit":
                win.flip()
                state = "running"
                break
            # 强行终止
            elif state == "exit":
                win.flip()
                win.close()
                core.quit()

    return result
