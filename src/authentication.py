import streamlit as st

class Authentication:



    def __init__(self):
        # Credenciais definidas manualmente
        self.valid_users = {
            "admin": "senhaforte"
        }



    def authenticate(self, username, password):
        """
        Método para autenticar o usuário.
        :param username: Nome de usuário.
        :param password: Senha do usuário.
        :return: True se as credenciais forem válidas, False caso contrário.
        """
        # Verifica se o usuário e senha correspondem
        return username in self.valid_users and self.valid_users[username] == password


    
    def logout(self):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()


        
    def login_ui(self):

        col1, col2 = st.columns(2)

        with col1: 
            st.subheader("Painel de avisos", divider=True)
            st.markdown("Aqui você encontrará informações importantes sobre o sistema.")
            
        with col2: 
            st.subheader("Login", divider=True, help="Utilize as credenciais enviadas por e-mail.")

            username = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")

            # Verificar credenciais ao clicar no botão
            if st.button("Entrar"):
                if Authentication().authenticate(username, password):
                    st.success(f"Bem-vindo, {username}!")
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")
