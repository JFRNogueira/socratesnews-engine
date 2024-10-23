import streamlit as st


def pl_gerenciar():
    
    st.title("Gestão de publicidades legais")
    st.markdown('Possui uma sugestão de melhoria para essa tela? Entre em contato com `suporte@socratesdata.com`.')
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.subheader('Publicidades publicadas', divider=True)
        st.session_state
        
        col11, col12, col13 = st.columns(3)
        
        with col11: 
            st.button('\<\<')
        
        with col12:
            st.write('Página 1')
        
        with col13:
            st.button('\>\>')
    
    with col2:
        st.subheader('Saldo', divider=True)
        
        col21, col22, col23 = st.columns(3)
        
        with col21:
            st.metric('DOU - Contratado', '1000cm.col')
            st.divider()
            st.metric('DOE - Contratado', '1000cm.col', help='DOE do estado contratado')
            st.divider()
            st.metric('JGC - Contratado', '1000cm.col', help='Jornal de Grande Circulação. Atualizado diariamente.')
        
        with col22:
            st.metric('DOU - Utilizado', '100cm.col')
            st.divider()
            st.metric('DOE - Utilizado', '100cm.col', help='DOE do estado contratado')
            st.divider()
            st.metric('JGC - Utilizado', '100cm.col', help='Jornal de Grande Circulação. Atualizado diariamente.')
        
        with col23:
            st.metric('DOU - Disponível', '900cm.col')
            st.divider()
            st.metric('DOE - Disponível', '900cm.col', help='DOE do estado contratado')
            st.divider()
            st.metric('JGC - Utilizado', '100cm.col', help='Jornal de Grande Circulação. Atualizado diariamente.')
        
        st.button('Baixar contrato')




if __name__ == '__main__':
    pl_gerenciar()
    
    
    
    
  