import streamlit as st
import hashlib
import branding
import dbfunctions
import webbrowser
import usermanagement as usr

branding.loadBranding()

def createUser(email, password, username):
    dbfunctions.executeWithoutFetch(f"INSERT INTO \"user\" (username, password, mail, fk_usergroupid) VALUES ('{username}', '{password}', '{email}', 2);")
    userdata = dbfunctions.executeQuery(f"SELECT DISTINCT username, password, userid from \"user\" WHERE mail = '{email}';")
    st.session_state['loginSucceed'] = True
    st.session_state['username'] = username
    st.session_state['userid'] = userdata[0][2]
    st.sidebar.success('Account created.', icon="✅")

def collectUserinfo(email, password):
    username = st.sidebar.text_input('Username')
    createBtn = st.sidebar.button('Register account')
    if createBtn:
        createUser(email, password, username)
    else:
        st.sidebar.warning('Account not created', icon="ℹ️")

def loginUser(email, password):
    userdata = dbfunctions.executeQuery(f"SELECT DISTINCT username, password, userid from \"user\" WHERE mail = '{email}';")
    if userdata:
        username = userdata[0][0]
        correctPW = userdata[0][1]
        userid = userdata[0][2]
        if password == correctPW:
            st.session_state['loginSucceed'] = True
            st.session_state['username'] = username
            st.session_state['userid'] = userid
            st.sidebar.info('Welcome back', icon="👋🏻")
        else:
            st.session_state['loginSucceed'] = False
            st.sidebar.warning('Wrong password')
    else:
        createUser(email, password, email)

st.write("""
# mangoTicket by Michi
""")

metricAllTickets, metricOpenTickets = st.columns(2)
countAllTickets = dbfunctions.executeQuery("SELECT * from \"alltickets-count\"")
countOpenTickets = dbfunctions.executeQuery("SELECT * from \"opentickets-count\"")
if not (countAllTickets[0][0] * -100) == 0:
    openTicketDelta = round(countOpenTickets[0][0] / countAllTickets[0][0] * -100)
else:
    openTicketDelta = 0
metricAllTickets.metric(label="All tickets", value=f"{countAllTickets[0][0]}")
metricOpenTickets.metric(label="Open tickets", value=f"{countOpenTickets[0][0]}", delta=f"{openTicketDelta} %")

st.write("""
This is a simple helpdesk tool. You can create different users and assign tickets to them. You can also create a database with customers. Each ticket can be assigned to a customer.
The tool is currently under development and still has some bugs/problems. If you have a suggestion, feel free to create an issue on GitHub so I can follow up on it.
""")

if st.button("View project on GitHub"):
    webbrowser.open_new_tab("https://github.com/michivonah/helpdesk")

if st.button("Self host"):
    webbrowser.open_new_tab("https://hub.docker.com/r/michivonah/mangoticket")

if not usr.checkLogin():
    st.sidebar.markdown("# Login/Register")
    st.session_state['loginSucceed'] = False
    email = st.sidebar.text_input('Mail')
    password = st.sidebar.text_input('Password', type="password")        
    loginBtn = st.sidebar.button('Sign in')

    if loginBtn:
        st.session_state['email'] = email
        passwordHashed = hashlib.sha256(password.encode())
        st.session_state['password'] = passwordHashed.hexdigest()
        loginUser(email, st.session_state.password)
        st.experimental_rerun()

else:
    st.sidebar.info('Welcome back', icon="👋🏻")
    logoutBtn = st.sidebar.button("Logout")

    if logoutBtn:
        usr.logout()
        st.sidebar.info('Logged out')
        st.experimental_rerun()
