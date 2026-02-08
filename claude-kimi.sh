#!/bin/bash
# Claude Code with Kimi 启动脚本

export ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
export ANTHROPIC_API_KEY=sk-kimi-4cIO9Ps487BvzCHEyCAF7Ohc9wYmRduoPe6lKNkeTrNRXhnw2pxY4dgHqIIEjOT8

# 启动 Claude Code
claude "$@"
