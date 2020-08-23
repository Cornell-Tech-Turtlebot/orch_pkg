# run only once
sudo apt-get install sshpass

gnome-terminal -e "bash ovpn.sh"
sshpass -p turtlebot2020 ssh -N -L 4194:localhost:4194 turtlebot@ddl46.tech.cornell.edu
