import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils.other_tools.allure_data.allure_report_data import TestMetrics, AllureFileClean
from utils import config
import os


class SendEmail:
    """ 发送邮箱 """

    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics
        self.allure_data = AllureFileClean()
        self.CaseDetail = self.allure_data.get_failed_cases_detail()

    @classmethod
    def send_mail(cls, user_list: list, sub, content: str, attachment_path: str) -> None:
        user = "kidd" + "<" + config.email.send_user + ">"

        # 创建多部分消息
        message = MIMEMultipart()
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)

        # 添加邮件正文
        text = MIMEText(content, _subtype='plain', _charset='utf-8')
        message.attach(text)

        # 添加附件
        if os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read())
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
            message.attach(attachment)

        server = smtplib.SMTP()
        server.connect(config.email.email_host)
        server.login(config.email.send_user, config.email.stamp_key)
        server.sendmail(user, user_list, message.as_string())
        server.close()

    def error_mail(self, error_message: str) -> None:
        email = config.email.send_list
        user_list = email.split(',')

        sub = config.project_name + "接口自动化执行异常通知"
        content = f"自动化测试执行完毕，程序中发现异常，请悉知。报错信息如下：\n{error_message}"
        attachment_path = '/Users/a1-6/Documents/my_projects/pytest-auto-api2-master/Files/自动化异常测试用例.xlsx'
        self.send_mail(user_list, sub, content, attachment_path)

    def send_main(self) -> None:
        email = config.email.send_list
        user_list = email.split(',')

        sub = config.project_name + "接口自动化报告"
        content = f"""
        各位同事, 大家好:
            自动化用例执行完成，执行结果如下:
            用例运行总数: {self.metrics.total} 个
            通过用例个数: {self.metrics.passed} 个
            失败用例个数: {self.metrics.failed} 个
            异常用例个数: {self.metrics.broken} 个
            跳过用例个数: {self.metrics.skipped} 个
            成  功   率: {self.metrics.pass_rate} %

        {self.allure_data.get_failed_cases_detail()}
        失败用例详情查看附件！！！
        """
        # 添加附件路径
        attachment_path = '/Users/a1-6/Documents/my_projects/pytest-auto-api2-master/Files/自动化异常测试用例.xlsx'
        self.send_mail(user_list, sub, content, attachment_path)


if __name__ == '__main__':
    SendEmail(AllureFileClean().get_case_count()).send_main()
