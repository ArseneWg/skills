#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# Copy this file, edit the steps below, and run it.
# The agent runs the script; the user follows prompts in their terminal.
#
# Usage:
#   bash hitl-loop.template.sh
#
# Two helpers:
#   step "<instruction>"          → show instruction, wait for Enter
#   capture VAR "<question>"      → show question, read response into VAR
#
# At the end, captured values are printed as KEY=VALUE for the agent to parse.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- edit below ---------------------------------------------------------

step "Prepare the target environment, device, service, file, or command exactly as required for the reported issue."

step "Run the shortest action that should reproduce the user-reported symptom."

capture SYMPTOM_PRESENT "Did the exact user-reported symptom appear? (y/n)"

capture SYMPTOM_DETAIL "Paste the exact error, log line, output difference, timing, or visible symptom (or 'none'):"

capture CONDITIONS "Record the key input, command, version, configuration, or device state used for this run:"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'SYMPTOM_PRESENT=%s\n' "$SYMPTOM_PRESENT"
printf 'SYMPTOM_DETAIL=%s\n' "$SYMPTOM_DETAIL"
printf 'CONDITIONS=%s\n' "$CONDITIONS"
