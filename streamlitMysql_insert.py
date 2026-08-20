import streamlit as st
import pymysql
import pandas as pd

st.title("사용자 추가 (userTable,id는 4자리 문자)")

name  = st.text_input("이름 입력")
email = st.text_input("이메일 입력")
birthyear = st.number_input("출생년도 입력",min_value=1900,max_value=2100,step=1)

if st.button("저장하기"):
    if not name.strip() or not email.strip():
        st.warning("이름과 이메일은 필수입니다!")
        
    else:
        try: 
            # conn = pymysql.connect(host="localhost", user="root",password="1111",database="employees",charset="utf8mb4")
            conn = pymysql.connect(host=st.secrets["DB_HOST"], user=st.secrets["DB_USER"],password=st.secrets["DB_PASSWORD"],database=st.secrets["DB_NAME"],charset="utf8mb4")
            cur = conn.cursor()
            print("1")
            
            cur.execute("select max(cast(id as UNSIGNED)) from usertable")
            result  = cur.fetchone()
            max_id = result[0] if result and result[0] is not None else 0 
            next_id = str(max_id+1).zfill(4)
            print("2")
            sql  = "insert into usertable (id,userName,email,birthYear) values (%s,%s,%s,%s)"
            cur.execute(sql,(next_id,name,email,birthyear))
            conn.commit()
            
            st.success(f"ID = {next_id}, 이름={name} 저장 완료!")
            
            cur.execute("SELECT id, UserName, email, birthYear from userTable order by id")
            rows = cur.fetchall()
            if rows:
                df= pd.DataFrame(rows, columns = ['id',"username","email","birthYear"])
                st.write("현재 저장된 사용자 목록")
                st.dataframe(df)
            else:
                st.info("테이블이 비어있습니다.") 
        except Exception as e:
            st.error(f"오류발생:{e}")
            
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass