in order to run the frontend by "npm run dev" the below dependencies should be installed    
"axios": "^1.7.7",
"crypto-js": "^4.2.0",
"react": "^18.3.1",
"react-dom": "^18.3.1",
"react-router-dom": "^6.28.0"


in order to run the backend by "python server.py" the things need to be there in computer:

python
mySQL
Flask
CORS

Registration Phase
Ti←{0,1}^λ
Ki=h (idi||k)
Xi=h (msk||Ti)
Ai=h (msk||Ki)
Bi=Ki⊕Xi
aidi= idi⊕msk⊕Ki

this is registration id entered by user and that is converted to aidi and these Alias Identity, A_i, B_i, T sent to user by server


Authentication Phase
 at user part:
 ri←{0,1}^λ
 m1=ri⊕Ai
Ri=h (ri)
m2=aidi⊕Ri
Get timestamp ti
 m3=h (idi||ri||Ai||Ti||ti)

the above is user part 
 (ti , m1 , m2, m3, Bi, Ti)  - these are passed to server     , and user has only these Alias Identity, A_i, B_i, T           which sent by server  so m1,m2,m3 should be generated in backend i think you should tell


At server part:
 Check ti
 Xi=h (msk||Ti)
 Ki=Bi⊕Xi
 Ai= h (msk||Ki)
 ri=m1⊕Ki
 Ri=h (ri)
 aidi=m2⊕Ri
 idi=aidi⊕msk⊕Ki
 m3′=h (idi||ri||Ai||Ti||tj) 

Check m3′=m3

server should verify this and give as authentication successfull


Sending reply:
 Ti*←{0,1}λ
 Xi*=h (msk||Ti*)
 ski, j=h (idi||ri||Ti*)
 Bi*=Ki⊕Xi*
 m4=Ti*⊕Ri⊕Ai
 m5=Bi*⊕aidi⊕ski, j
 Get timestamp tj
 m6=h (ski, j||idi||Bi*||Ti*||tj)

(tj , m4, m5, m6)  -- these sent to client

client 

 e) ExKey. Recover
 Check tj
 Ti*=m4⊕Ri⊕Ai
 
ski, j=h (idi||ri||Ti* )
 Bi*=m5⊕aidi⊕ski, j
 m6′=h (ski, j||idi||ri||Bi*||Ti*||tj)
 
Check m6′=m6

Then it is reply by correct server only not any hacker server
Reference from paper "A General Authentication and Key Agreement Framework for Industrial Control System"
