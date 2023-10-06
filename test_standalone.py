
from streamlit.testing.v1 import AppTest

# Sample app to be tested
def my_app():
    import streamlit as st

    st.title("My awesome app")

    password = st.text_input("Enter password:", key="password")
    if password and password == st.session_state.PASSWORD:
        st.write("Congrats! You can see the secret content 🎉")
    else:
        st.write("Sorry, the passwords didn't match")

def test_incorrect_password():
    at = AppTest.from_function(my_app)
    # Configure session_state, query params directly (secrets coming soon)
    at.session_state["PASSWORD"] = "Foobar"
    # Run once to display the initial app page
    at.run()
    # Inspect and manipulate elements on the page
    assert not at.exception

    # Simulate a user inputting an incorrect password
    at.text_input("password").input("bazbat")
    at.run()
    print(at)
    # Should see an error since the entered password didn't match secret
    assert at.markdown[0].value == "Sorry, the passwords didn't match"
