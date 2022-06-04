cd ~/.streamlit/

echo "\
[theme]\n\
primaryColor='#584BFF'\n\
backgroundColor='#0E1117'\n\
secondaryBackgroundColor='#262730'\n\
textColor='#FAFAFA'\n\
font='sans serif'\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml