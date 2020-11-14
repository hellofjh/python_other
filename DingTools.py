import uiautomator2 as u2
import time
from interval import Interval

class DingTools:
    def __init__(self):
        self.device_id = "fc89366d"
        self.package_name = "com.alibaba.android.rimet" # com.alibaba.android.rimet:钉钉 com.xingin.xhs：小红书
        self.con = u2.connect(self.device_id)

    def _star(self):
        self.con.app_start(self.package_name)

    def _stop(self):
        self.con.app_stop(self.package_name)

    # 初始化检查 找不到工作台 初始化app
    def word_check_init(self):
        while True:
            try:
                self._star()
                self.con.xpath('//*[@resource-id="com.alibaba.android.rimet:id/home_bottom_tab_button_work"]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()
                break
            except:
                print('stop')
                self._stop()

    def run(self):
        try:
            self.con(text="考勤打卡").click()
            self.con(text="上班打卡").click()
            self.con(text="上班打卡成功").get_text()
            self._stop()
            return True
        except:
            return False


_class = DingTools()
run_interval = Interval("08:50:00", "9:00:00")

while True:
    now_time = time.strftime("%H:%M:%S", time.localtime())
    if now_time in run_interval:
        _class.word_check_init()
        res = _class.run()
        print(res)
    time.sleep(5)
    print("loading...")
