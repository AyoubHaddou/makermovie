cd ~/.streamlit/

echo "\[theme]
primaryColor='#584BFF'
backgroundColor='#0E1117'
secondaryBackgroundColor='#262730'
textColor='#FAFAFA'
font='sans serif'\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml