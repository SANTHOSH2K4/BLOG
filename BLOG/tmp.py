import sqlite3

conn=sqlite3.connect('blog.db')
c=conn.cursor()


c.execute("create table community(id integer primary key autoincrement,uname text,subject text,content text,soln text)")

#c.execute("insert into users values('santhosh','santhosh2k495@gmail.com','1234')")
c.execute("select name from users")
li=c.fetchall()
uname=[]
email=[]
pw=[]
for i in range(0,len(li)):
    uname.append(li[i][0])
print(uname)
#c.execute("insert into community(uname,subject,content,soln) values('{}','fertilizer','i want best fertilizer for my crop land','santhosh : buy it in a shop nearby')".format(uname[1]))
conn.commit()
c.execute("select *from community")
li=c.fetchall()
print(li)

solli = c.execute("SELECT uname FROM community WHERE id={}".format(1))
result = solli.fetchone()
print(result[0])
