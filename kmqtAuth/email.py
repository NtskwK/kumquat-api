import re

from django.core.mail import send_mail


def is_email(email):
    # 定义邮箱地址的正则表达式
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def send_activate_eam_email(email_address: str, activation_url: str):
    assert is_email(email_address), f"Invalid email address: {email_address}"
    send_mail(
        subject="Kmqt 账号激活",
        message=f"请前往以下地址激活您的账号：\n{activation_url}",
        from_email="morrin356@163.com",
        recipient_list=["1124075801@qq.com"],
    )
