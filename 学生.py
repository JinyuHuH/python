from tkinter import *
import tkinter.font as tkFont
from tkinter.ttk import Treeview
import tkinter.messagebox
import pyodbc


# 数据库连接
def sql_conn(sql, n):
    conn = pyodbc.connect(DRIVER='{SQL Server}', SERVER='localhost', DATABASE='bookdb123', UID="db0123", PWD="db0123")
    cursor = conn.cursor()
    cursor.execute(sql)
    if n == 1:
        ret = cursor.fetchall()
        return ret
    else:
        conn.commit()
        conn.close()
        return


# 遍历全部数据
def all_data():
    sql = "select * from 学生信息"
    ret = sql_conn(sql, 1)
    tab(ret)


# 遍历table数据
def tab(ret):
    for i in range(len(ret)):
        print(ret)
        table.insert('', i, values=(
            ret[i][0], ret[i][1], ret[i][2], ret[i][3], ret[i][4], ret[i][5], ret[i][6], ret[i][7], ret[i][8]))


# 清空table数据
def delete_tab(table):
    items = table.get_children()
    [table.delete(item) for item in items]


# 查询功能,按学号关键字查询学生信息
def look():
    if n1.get() == '' and n2.get() == '' and n3.get() == '' and n3.get() == '' and n4.get() == '' and n5.get() == '' and n6.get() == '' and n7.get() == '' and n8.get() == '' and n9.get() == '':
        return None
    else:
        sql = "select * from 学生信息 where 学号 like'" + n1.get()+"%'"
        print(sql)
        ret = sql_conn(sql, 1)
        print(ret)
        delete_tab(table)
        tab(ret)


tk = Tk()
tk.title("学生信息管理系统")
tk.maxsize(1000, 900)  # 设置窗口最大尺寸
Label(tk, text='欢迎使用学生信息管理系统', font=tkFont.Font(size=18), width=60, height=2, bg='#FFE7BA').grid(row=0,
                                                                                                  sticky=W + E)

columns = ('学号', '姓名', '性别', '学院', '联系电话', '身份证号码', '专业', '年级', '是否毕业')
table = Treeview(tk, height=14, show="headings", columns=columns)
table.column('学号', width=50, anchor='center')
table.column('姓名', width=50, anchor='center')
table.column('性别', width=50, anchor='center')
table.column('学院', width=50, anchor='center')
table.column('联系电话', width=50, anchor='center')
table.column('身份证号码', width=50, anchor='center')
table.column('专业', width=50, anchor='center')
table.column('年级', width=50, anchor='center')
table.column('是否毕业', width=50, anchor='center')
table.heading('学号', text="学号")
table.heading('姓名', text="姓名")
table.heading('性别', text="性别")
table.heading('学院', text="地址")
table.heading('联系电话', text="联系电话")
table.heading('身份证号码', text="身份证号码")
table.heading('专业', text="专业")
table.heading('年级', text="年级")
table.heading('是否毕业', text="是否毕业")

# all_data()
table.grid(row=1, sticky=W + E)
frame = Frame()
frame.grid(row=2, pady=20)
n1 = StringVar()
Label(frame, text="学号：").grid(row=0, column=0)
Entry(frame, textvariable=n1).grid(row=0, column=1)
Button(frame, text="查询", width=12, command=look, bg='#FFE7BA').grid(row=0, column=2, padx=10, pady=2)
tk.mainloop()