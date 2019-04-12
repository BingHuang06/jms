import subprocess


class Bash(object):
    def __init__(self):
        self.ret = None

    def execute(self, command):
        self.ret = subprocess.Popen('{0}'.format(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.ret.wait()
        print(self.ret.stderr.read())

    @property
    def stdout(self):
        return self.ret.stdout.read()

    @property
    def stderr(self):
        return self.ret.stderr.read()

    @property
    def code(self):
        return self.ret.returncode


class ServerUserManager(object):
    def __init__(self, sh):
        self.sh = sh()

    def present(self, username='', password='', shell="/bin/bash", is_active=""):
        if username == "admin":
            return [0, 'admin用户']

        cmd_add = 'id {username} || useradd  {username} -s {shell}'.format(username=username, shell=shell)
        self.sh.execute(cmd_add)

        if self.sh.code != 0:
            return [1, '用户添加失败']

        if password:
            cmd_passwd = 'echo {password} | passwd --stdin {username}'.format(username=username, password=password)
            self.sh.execute(cmd_passwd)
            if self.sh.code != 0:
                return [1, '用户密码修改失败']

        if is_active == True:
            cmd_active = 'usermod -U {username}'.format(username=username)
            self.sh.execute(cmd_active)
            if self.sh.code != 0:
                return [1, '用户激活失败']
        elif is_active == False:
            cmd_active = 'usermod -L {username}'.format(username=username)
            self.sh.execute(cmd_active)
            if self.sh.code != 0:
                return [1, '用户禁用失败']

        return [0, '添加用户成功']

    def absent(self, username, force=False):
        if username == "admin":
            return [0, 'admin用户']

        if not self.check_user_exist(username):
            return [0, '用户不存在']

        cmd = ['userdel'.format(username=username)]
        if force:
            cmd.append('--force -r')

        cmd.append(username)
        cmd = ' '.join(cmd)
        self.sh.execute(cmd)
        if self.sh.code != 0:
            return [1, '移除用户失败']
        else:
            return [0, '移除用户成功']

    def check_user_exist(self, username):
        cmd = 'id {username}'.format(username=username)
        self.sh.execute(cmd)

        if self.sh.code == 0:
            return True
        else:
            return False
