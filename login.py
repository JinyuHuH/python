import tkinter as tk
import tkinter.messagebox
import pickle

show = tk.Tk()
show.title('学生信息管理系统登录页面')
show.geometry('400x280+660+380')
"""canvas = tk.Canvas(show, width=400, height=135, bg='gray')
image_file = tk.PhotoImage(file='abc.png')
image = canvas.create_image(200, 0, anchor='n', image=image_file)
canvas.pack(side='top')
tk.Label(show, text='Wellcome！',font=('Arial', 16)).pack()"""

tk.Label(show, text='欢迎使用学生信息管理系统', font=('楷体', 16), width=36, height=7, bg='#FFE7BA').place(x=0, y=-10)
tk.Label(show, text='', width=60, height=10, bg='#FFE7BA').place(x=0, y=140)

tk.Label(show, text='用户名:', font=('楷体', 14), bg='#FFE7BA').place(x=10, y=120)
tk.Label(show, text='密码:', font=('楷体', 14), bg='#FFE7BA').place(x=10, y=150)

# 用户名
var_usr_name = tk.StringVar()
var_usr_name.set('')
entry_usr_name = tk.Entry(show, textvariable=var_usr_name, font=('Arial', 14)).place(x=120, y=120)
# 用户密码
var_usr_pwd = tk.StringVar()
var_usr_pwd.set('')
entry_usr_pwd = tk.Entry(show, textvariable=var_usr_pwd, font=('Arial', 14), show='*').place(x=120, y=150)


def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    # 这里设置异常捕获，当我们第一次访问用户信息文件时是不存在的，所以这里设置异常捕获。
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
            usr_file.close()

    # 如果用户名和密码匹配成功，则会登录成功，并跳出弹窗
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name] and var1.get() == 1:
            tkinter.messagebox.showinfo(title='欢迎', message='恭喜您成功登录，' + usr_name)
            show.destroy()
            import 管理系统
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name] and var2.get() == 1:
            tkinter.messagebox.showinfo(title='欢迎', message='恭喜您成功登录，' + usr_name)
            show.destroy()
            import 学生
        else:
            tkinter.messagebox.showerror(message='您的密码输入错误，请再次输入！.')
    else:
        is_sign_up = tkinter.messagebox.askyesno('你好！ ', '您并没有注册用户. 现在是否需要注册?')
        if is_sign_up:
            usr_sign_up()


def usr_sign_up():
    def sign_to_Website():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        # 判断密码，如果两次密码输入不一致，则提示错误
        if np != npf:
            tkinter.messagebox.showerror('错误', '密码和确认密码必须相同!')

        elif nn in exist_usr_info:
            tkinter.messagebox.showerror('错误', '用户已注册!')

        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tkinter.messagebox.showinfo('欢迎', '您已成功注册!')
            window_sign_up.destroy()

    window_sign_up = tk.Toplevel()
    window_sign_up.geometry('300x180')
    window_sign_up.title('注册窗口')

    new_name = tk.StringVar()
    new_name.set('')
    tk.Label(window_sign_up, text='', width=70, height=20, bg='#FFE7BA').place(x=0, y=0)
    tk.Label(window_sign_up, text='登录名: ', bg='#FFE7BA').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name).place(x=130, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='密码: ', bg='#FFE7BA').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=130, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='确认密码: ', bg='#FFE7BA').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=130, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='立即注册', bg='#FFE7BA', command=sign_to_Website)
    btn_comfirm_sign_up.place(x=180, y=120)


btn_login = tk.Button(show, text='  登录  ', width=10, command=usr_login, bg='#FFE7BA').place(x=60, y=230)
btn_sign_up = tk.Button(show, text='  注册  ', width=10, command=usr_sign_up, bg='#FFE7BA').place(x=200, y=230)
var1 = tk.IntVar()
var2 = tk.IntVar()
b1 = tk.Label(show, text='权限：', bg='#FFE7BA').place(x=30, y=190)
c1 = tk.Checkbutton(show, variable=var1, text='管理员', bg='#FFE7BA').place(x=90, y=190)
c2 = tk.Checkbutton(show, variable=var2, text='学生', bg='#FFE7BA').place(x=200, y=190)
show.mainloop()
