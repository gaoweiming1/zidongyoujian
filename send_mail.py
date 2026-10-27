import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.header import Header
from email.mime.text import MIMEText

# GitHub Actions 的服务器是 UTC 时间，这里手动换算成北京时间
CST = timezone(timedelta(hours=8))
now = datetime.now(CST)


def env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"缺少环境变量 {name}，请去仓库 Settings → Secrets 里配置")
    return value


sender = env("MAIL_USER")     # 发件邮箱，如 123456@qq.com
password = env("MAIL_PASS")   # 授权码，不是登录密码
receiver = env("MAIL_TO")     # 收件邮箱，可以和发件相同

subject = f"每日提醒 · {now.strftime('%m月%d日')}"

body = f"""早上好！

今天是 {now.strftime('%Y年%m月%d日')}，星期{'一二三四五六日'[now.weekday()]}。

这封邮件由 GitHub Actions 自动发出。

—— 你的自动化助手
"""

msg = MIMEText(body, "plain", "utf-8")
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = Header(subject, "utf-8")

# QQ 邮箱 SMTP：地址 smtp.qq.com，SSL 端口 465
# 其他邮箱参考：163 → smtp.163.com / 465，Gmail → smtp.gmail.com / 587
with smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=30) as server:
    server.login(sender, password)
    server.sendmail(sender, [receiver], msg.as_string())

print(f"邮件已发送 → {receiver}")
