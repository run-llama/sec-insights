alias l='ls -F'
alias ll='ls -lart'
export LANG=zh_CN.UTF8
export PS1='[\w]$ '
export EXINIT="set exrc nu ai sm ts=4 sw=4 laststatus=0 foldmethod=indent
:map <C-A> <Esc>:e#<C-M>"
set -o vi

set -a
source /workspaces/sec-insights/backend/.env
. /workspaces/sec-insights/backend/.venv/bin/activate