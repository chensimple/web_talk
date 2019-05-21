import tornado.ioloop
import tornado.web
import tornado.websocket
import os
totle_list = dict()  # 存储所有登录用户 "ip:用户名" 以ip为关键字

# 局域网聊天室程序，只需用户名即可聊天，以ip为关键字，单ip重复登录会覆盖用户名，聊天记录本地保存，支持同时开启多个聊天室


class chat_group:  # 单个聊天室中用户组
    members = dict()

    def add(self, mem, ip):  # 增加用户
        self.members[ip] = mem

    def get_names(self):  # 返回所有用户名
        return list(self.members.values())


class MainHandler(tornado.web.RequestHandler):  # 输入用户名界面
    def get(self):
        self.render("web.html")

    def post(self):
        pass


class LoginHandler(tornado.web.RequestHandler):  # 选择聊天室页面
    def get(self):
        self.write("请先登录")

    def post(self):
        totle_list[self.request.remote_ip] = self.get_argument("username")
        '''
        # test login
        print(self.request.remote_ip + ":" + self.get_argument("username") +
              "登录")
              '''
        self.render("chat.html", rooms=list(room_li.keys()))


class ChatHandler(tornado.web.RequestHandler):  # 聊天室界面
    def get(self):
        self.write("请先登录")

    def post(self):
        s = self.get_argument("whichroom")  # 获取聊天室名字
        if s == "new":  # 添加聊天室
            room_name = "".join([totle_list[self.request.remote_ip], "的房间"])
            room_li[room_name] = chat_group()
            room_li[room_name].add(totle_list[self.request.remote_ip],
                                   self.request.remote_ip)
            '''
            print("在线房间:" + "\r\n".join(list(room_li.keys())))
            print("在线总用户列表", totle_list)
            '''
            self.render(
                "chatting.html",
                username=totle_list[self.request.remote_ip],
                users="\r\n".join(room_li[room_name].get_names()),
                roomname=room_name)
        else:
            room_name = s.split(" ")[1]
            room_li[room_name].add(totle_list[self.request.remote_ip],
                                   self.request.remote_ip)
            self.render(
                "chatting.html",
                username=totle_list[self.request.remote_ip],
                users="\r\n".join(room_li[room_name].get_names()),
                roomname=room_name)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):  # websocket处理函数
    waiters = {}  # 聊天室组 "聊天室名字:[处理列表]"

    def open(self):
        name = self.get_argument("name")  # 获取聊天室名字
        if name in self.waiters:
            self.waiters[name].append(self)
        else:
            self.waiters[name] = [self]

    def on_close(self):
        name = self.get_argument("name")
        self.waiters[name].remove(self)
        ChatSocketHandler.waiters[name].remove(self)

    def on_message(self, message):
        name = self.get_argument("name")
        for waiter in self.waiters[name]:
            waiter.write_message(message)


if __name__ == "__main__":
    room_li = dict()  # 存储所有聊天室组及对应的用户组
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/login/chat", ChatHandler),
        (r"/chatting", ChatSocketHandler),
    ],
        static_path=os.path.join(
        os.path.dirname(__file__),
        'static'))
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
