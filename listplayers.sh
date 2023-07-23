#!/usr/bin/expect
set timeout 20
spawn telnet localhost 8081
expect -re "Please enter password:"
send "${ServerPassword}\r"
expect -re "end session."
send "listplayers\r"
expect -re "in the game"
send "exit\r"