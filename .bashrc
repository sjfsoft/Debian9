# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
# export LS_OPTIONS='--color=auto'
# eval "`dircolors`"
# alias ls='ls $LS_OPTIONS'
# alias ll='ls $LS_OPTIONS -l'
# alias l='ls $LS_OPTIONS -lA'
#
# Some more alias to avoid making mistakes:
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'
alias l='ls --color=auto -Al'
alias rm='rm -f -r'
alias cp='cp -f'
alias mv='mv -f'
alias rz='rz -b -y'
alias sz='sz -b'
alias cls='clear'
alias log='cat /var/log/auth.log'
alias logd='rm /var/log/auth.log'
alias net='netstat -ant'
alias nets='netstat -lnp'
alias tv='cat /var/log/tv.log'
alias h='history'
alias hd='history'
alias last='last -a'
alias lastd='rm /var/log/wtmp'
alias s='cat /var/log/shadowsocksr.log'
alias sd='rm /var/log/shadowsocksr.log'
alias vlm='cat /var/log/vlmcsd.log'
alias vlmd='rm /var/log/vlmcsd.log'
