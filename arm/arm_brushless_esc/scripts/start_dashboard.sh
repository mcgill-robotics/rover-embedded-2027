if [ -d "./.venv/bin" ]; then
  source .venv/bin/activate
fi
arm-esc-dashboard --db can_log.db $@
