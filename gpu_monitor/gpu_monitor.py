import os
import sys
import signal
import time
import datetime
import smtplib
from email.mime.text import MIMEText

pause = 1
mailto_list=[''] #收件人邮箱地址
mail_host= "smtp.tju.edu.cn" #邮箱服务器
mail_user= "" #发送警报的邮箱
mail_pass= "" #SMTP password
mail_postfix="tju.edu.cn"

def send_email(to_list,sub,content):
    me = "GPU Auto Monitor"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                       #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception:
        print("send error!")
        return False

def get_gpu_tem(gpu_id):
    shell_str = "nvidia-smi  | grep %"
    result = os.popen(shell_str)
    result_str = result.read()
    # tem_0 = result_str.split("\n")[0].split(" ")[4]
    # tem_0 = tem_0[:len(tem_0) - 1] #GPU0
    # tem_1 = result_str.split("\n")[1].split(" ")[4]
    # tem_1 = tem_1[:len(tem_1) - 1] #GPU1
    # tem_2 = result_str.split("\n")[2].split(" ")[4]
    # tem_2 = tem_2[:len(tem_2) - 1] #GPU2
    # tem_3 = result_str.split("\n")[3].split(" ")[4]
    # tem_3 = tem_3[:len(tem_3) - 1] #GPU3
    tem = result_str.split("\n")[int(gpu_id)].split(" ")[4]
    tem = tem[:len(tem) - 1] 
    result.close()
    return float(tem)

def kill_process(process_id):
    try:
        ret = os.kill(process_id, signal.SIGKILL)
        print('kill %s return %s' % (process_id, ret))
        sys.exit()
    except OSError:
        print("error!")



while(True):
    try:
        tem_num = get_gpu_tem(sys.argv[1])
        if tem_num > 80:
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            warning_str = nowTime+"  Current temperature is " + str(tem_num) + "!"
            print(warning_str)
            send_email(mailto_list, "GPU Warning!!!", warning_str)
            print("send over")
            kill_process(int(sys.argv[2]))
    finally:
        time.sleep(pause)
