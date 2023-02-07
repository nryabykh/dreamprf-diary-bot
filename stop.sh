kill -15 $(ps ax | grep dreamprf | grep -v grep | awk '{print $1}')
