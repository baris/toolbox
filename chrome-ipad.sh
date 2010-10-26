#!/bin/bash

USER_AGENT_IPAD="Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10"

exec /Applications/Google Chrome.app/Contents/MacOS/Google Chrome -user-agent=$USER_AGENT_IPAD &

