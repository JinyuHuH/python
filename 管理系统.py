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


# 查询功能
def look():
    if n1.get() == '' and n2.get() == '' and n3.get() == '' and n3.get() == '' and n4.get() == '' and n5.get() == '' and n6.get() == '' and n7.get() == '' and n8.get() == '' and n9.get() == '':
        return None
    else:
        sql = "select * from 学生信息 where 学号 like'" + n1.get() + "%' or 姓名 ='" + n2.get() + "' or 性别='" + n3.get() + "'or 学院 ='" + n4.get() + "' or 联系电话='" + n5.get() + "'or 身份证号码 ='" + n6.get() + "' or 专业='" + n7.get() + "'or 年级 ='" + n8.get() + "' or 是否毕业='" + n9.get() + "' "
        print(sql)
        ret = sql_conn(sql, 1)
        print(ret)
        delete_tab(table)
        tab(ret)


# 修改功能
def alter():
    if n1.get() == '' and n2.get() == '' and n3.get() == '' and n4.get() == '' and n5.get() == '' and n6.get() == '' and n7.get() == '' and n8.get() == '' and n9.get() == '':
        return None
    else:
        sql = "update  学生信息 set 姓名='{}',性别='{}',学院='{}',联系电话='{}',身份证号码='{}',专业='{}',年级='{}',是否毕业='{}' where 学号 ='{}' "
        sqlss = sql.format(n2.get(), n3.get(), n4.get(), n5.get(),
                           n6.get(), n7.get(), n8.get(), n9.get(), n1.get())
        tkinter.messagebox.showinfo('', '修改成功!')
        print(sqlss)
        ret = sql_conn(sqlss, 0)
        delete_tab(table)
        tab(ret)
        all_data()


# 插入功能
def insert():
    if n1.get() == '' and n2.get() == '' and n3.get() == '' and n4.get() == '' and n5.get() == '' and n6.get() == '' and n7.get() == '' and n8.get() == '' and n9.get() == '':
        tkinter.messagebox.showerror('警告', '请填写完整！')
        return None
    else:
        sql = "insert  学生信息(学号,姓名,性别,学院,联系电话,身份证号码,专业,年级,是否毕业) values  ('{}','{}','{}','{}','{}','{}','{}','{}','{}') "
        sqlss = sql.format(n1.get(), n2.get(), n3.get(), n4.get(), n5.get(),
                           n6.get(), n7.get(), n8.get(), n9.get())
        tkinter.messagebox.showinfo('', '添加成功!')
        print(sqlss)
        sql_conn(sqlss, 0)
        delete_tab()
        # tab(ret)
    all_data()


# 删除功能，仅实现以学号为索引删除数据
def delete():
    if n1.get() == '':
        tkinter.messagebox.showerror('警告', '请输入要删除的学生学号！')
    else:
        sql = "delete from 学生信息 where 学号='" + n1.get() + "';"
        ret = sql_conn(sql, 0)
        tkinter.messagebox.showinfo('', '删除成功!')
        print(ret)
        delete_tab(table)
        tab(ret)
        all_data()


tk = Tk()
tk.title("学生管理信息管理系统")
tk.maxsize(1000, 560)  # 设置窗口最大尺寸
Label(tk, text='欢迎使用学生管理系统', font=tkFont.Font(size=18), width=60, height=3, bg='#FFE7BA').grid(row=0,
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
frame = Frame(bg='#FFE7BA')
frame.grid(row=2, pady=20)
n1 = StringVar()
n2 = StringVar()
n3 = StringVar()
n4 = StringVar()
n5 = StringVar()
n6 = StringVar()
n7 = StringVar()
n8 = StringVar()
n9 = StringVar()

Label(frame, text="学号：",bg='#FFE7BA',height=3).grid(row=0, column=1)
Label(frame, text="姓名：",bg='#FFE7BA').grid(row=1, column=1)
Label(frame, text="性别：",bg='#FFE7BA').grid(row=2, column=1)
Label(frame, text="学院：",bg='#FFE7BA').grid(row=0, column=4)
Label(frame, text="联系电话：",bg='#FFE7BA').grid(row=1, column=4)
Label(frame, text="身份证号码：",bg='#FFE7BA',).grid(row=2, column=4)
Label(frame, text="专业：",bg='#FFE7BA',height=2).grid(row=0, column=7)
Label(frame, text="年级：",bg='#FFE7BA',height=2).grid(row=1, column=7)
Label(frame, text="是否毕业：",height=3,bg='#FFE7BA').grid(row=2, column=7)

Entry(frame, textvariable=n1).grid(row=0, column=2)
Entry(frame, textvariable=n2).grid(row=1, column=2)
Entry(frame, textvariable=n3).grid(row=2, column=2)
Entry(frame, textvariable=n4).grid(row=0, column=5)
Entry(frame, textvariable=n5).grid(row=1, column=5)
Entry(frame, textvariable=n6).grid(row=2, column=5)
Entry(frame, textvariable=n7).grid(row=0, column=8)
Entry(frame, textvariable=n8).grid(row=1, column=8)
Entry(frame, textvariable=n9).grid(row=2, column=8)
Label(frame,text='',width=2,bg='#FFE7BA').grid(row=0,rowspan=3,column=0)
Label(frame,text='',width=2,bg='#FFE7BA').grid(row=0,rowspan=3,column=3)
Label(frame,text='',width=2,bg='#FFE7BA').grid(row=0,rowspan=3,column=6)
Label(frame,text='',width=2,bg='#FFE7BA').grid(row=0,rowspan=3,column=9)
Button(frame, text="查询", width=12, command=look, bg='#FFE7BA').grid(row=0, column=10, ipadx=5, ipady=5)
Button(frame, text="修改", width=12, command=alter, bg='#FFE7BA').grid(row=1, column=10, ipadx=5, ipady=5)
Button(frame, text="添加", width=12, command=insert, bg='#FFE7BA').grid(row=0, column=11,ipadx=5, ipady=5)
Button(frame, text="删除", width=12, command=delete, bg='#FFE7BA').grid(row=1, column=11,ipadx=5, ipady=5)

tk.mainloop()

