# automailer #

## Summary ##
automailer一个用于批处理邮件分发的小工具。 写这个工具的初衷是在日常工作中有时候由于种种考量，需要将同样的邮件单独发给若干个不同的人。

automailer的使用方法如下：
```
$> python automailer -i configfile -f mailtxt [-a attachment] [-r | --respectively]
```

选项的意思如下：
* -i : 指定的配置文件(ini格式)
* -f : 指定的邮件正文模板(需要是纯文本)
* -a : 邮件的附件指定(尚未实现)
* -r(或 --respectively) : 当收件人有多个时，邮件将单独发给各个收件人。如不指定此项，则默认将所有收件人在一封邮件内全部作为TO对象，并发送。

## Config File Format ##
由于该工具的配置文件选择了ini格式，因此对于内容和形式上有所限制。一个模板如下：

```
[sender]
smtp = smtp.xxx.com
user = xiaowing
address = xiaowing@xxx.com
password = $$$$$$$

[receiver]
aaa@hotmail.com = Harry Potter
bbb@gmail.com = Ron Weasley
ccc@yahoo.com = Hermione Granger

[mailtext]
subject = A test mail for you!
```

* sender段 : 配置送信者的SMTP认证信息等
* receiver段 : 配置收件人一览。这里需要将邮件地址作为key，收件人姓名作为value。因为有可能会有重名
* mailtext ：其实没啥作用，就是想有个地方设置邮件标题...

- 以上 -
