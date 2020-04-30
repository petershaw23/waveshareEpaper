# start talking to the SMTP server for Gmail
s = smtplib.SMTP(‘smtp.gmail.com’, 587)
s.starttls()
s.ehlo()
# now login as my gmail user
username=’petershawiot@gmail.com’
password=’XXXXXXXX’
s.login(username,password)
# the email objects
replyto=’petershawiot@gmail.com’ # where a reply to will go
sendto=[‘michael.budjan@gmail.com’] # list to send to
sendtoShow=’petershawiot@gmail.com’ # what shows on the email as send to
subject=’Test from pysmtp’ # subject line
content=”Hello, this is a test of the system.\nHows it going\nMe” # content 
# compose the email. probably should use the email python module
mailtext=’From: ‘+replyto+’\nTo: ‘+sendtoShow+’\n’
mailtext=mailtext+’Subject:’+subject+’\n’+content
# send the email
s.sendmail(replyto, sendto, mailtext)
# we’re done
rslt=s.quit()
# print the result
print(‘Sendmail result=’ + str(rslt[1]))
