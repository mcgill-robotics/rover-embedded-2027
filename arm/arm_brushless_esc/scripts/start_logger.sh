if [ -d "./.venv/bin" ]; then
  source .venv/bin/activate
fi
if [ -v $0 ]; then
    arm-esc-logger --port $0 --db can_log.db
else
	  arm-esc-logger --port /dev/ttyACM0 --db can_log.db
fi
