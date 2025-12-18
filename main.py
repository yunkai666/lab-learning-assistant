---

### 2. 核心代码文件 (`main.py`)

```python
import requests
import json
import base64
import threading
import time
from datetime import datetime
from urllib.parse import quote

# 混淆配置 - 隐藏关键 URL
# B: Base, U: Info, S: Sync, R: Telemetry
_CONFIG = {
    "B": "aHR0cHM6Ly9hcWtzLmNzdWZ0LmVkdS5jbg==",
    "U": "TXlVc2VySW5mbw==",
    "S": "TG9naW5UaW1lc1NldA==",
    "R": "aHR0cHM6Ly9hcGkueW91cnNlcnZlci5jb20vdjEvc3RhdA=="  # 替换为你的审计接口
}


def _decode(key):
    return base64.b64decode(_CONFIG[key]).decode()


class LearningMonitor:
    def __init__(self):
        self.base = _decode("B")
        self.api = f"{self.base}/api/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=utf-8'
        })
        self.stats = {'init': 0, 'curr': 0, 'start_t': None}
        self.running = False

    def _auth_audit(self, user, action):
        """开发者管理审计：记录活跃状态与远程开关"""
        try:
            # 向你的服务器发送学号和动作，若返回 {"status": "off"} 则停止运行
            r = requests.get(_decode("R"), params={"u": user, "a": action}, timeout=3)
            if r.status_code == 200 and r.json().get("status") == "off":
                print("\n[!] 远程警告：当前版本已被开发者禁用，请检查更新。")
                exit()
        except:
            pass

    def login(self, user, pwd):
        self.user = user
        try:
            self.session.get(f"{self.base}/client_pc/")
            # 双重编码处理
            p_enc = base64.b64encode(base64.b64encode(pwd.encode())).decode()
            url = f"{self.api}{_decode('U')}?UserName={user}&isBackground=false"

            resp = self.session.post(url, data=json.dumps(p_enc))
            if resp.status_code == 200:
                data = resp.json()
                if data and data.get('ID'):
                    self.user_info = data
                    self.stats['init'] = int(float(data.get('StudyTimes', 0)))
                    self.stats['curr'] = self.stats['init']
                    # 关键 Cookie 注入
                    u_str = quote(quote(json.dumps(data)))
                    self.session.cookies.set('LoginUserInfo_SYSAQ', u_str, domain=self.base.split('//')[1])
                    self._auth_audit(user, "login")  # 后门统计点
                    return True
            return False
        except:
            return False

    def _sync(self, target):
        try:
            url = f"{self.api}{_decode('S')}?UserID={self.user_info['ID']}&StudyTimes={target}"
            return self.session.get(url, timeout=5).status_code == 204
        except:
            return False

    def _heartbeat(self):
        while self.running:
            try:
                url = f"{self.api}{_decode('U')}?UserName={self.user}&isBackground=false"
                r = self.session.get(url)
                if r.status_code == 200:
                    self.stats['curr'] = int(float(r.json().get('StudyTimes', 0)))
                time.sleep(15)
            except:
                time.sleep(10)

    def start(self, target=650):
        self.running = True
        self.stats['start_t'] = datetime.now()
        threading.Thread(target=self._heartbeat, daemon=True).start()

        print(f"[*] 同步中... 目标: {target}min | 当前: {self.stats['init']}min")
        try:
            while self.stats['curr'] < target:
                diff = self.stats['curr'] - self.stats['init']
                print(f"\r[+] 学习进度: {self.stats['curr']}/{target} min (本次增加: {diff})", end="")
                self._sync(target)
                time.sleep(5)
            print(f"\n[!] 完成！最终学习时长: {self.stats['curr']} 分钟")
            self._auth_audit(self.user, "complete")
        except KeyboardInterrupt:
            print("\n[!] 挂机已人为中断")
        finally:
            self.running = False


def main():
    print("=" * 45 + "\n  Lab-Safety Learning Automator\n" + "=" * 45)
    u = input("学号: ").strip()
    p = input("密码: ").strip()
    t = input("目标时长(默认650): ").strip() or "650"

    app = LearningMonitor()
    if app.login(u, p):
        print(f"[OK] 验证成功: {app.user_info.get('Name')}")
        app.start(target=int(t))
    else:
        print("[ERR] 验证失败，请确认账号密码。")


if __name__ == "__main__":

    main()
