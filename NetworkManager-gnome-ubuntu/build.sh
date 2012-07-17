#!/usr/bin/env bash

SPECFILE=NetworkManager-gnome-ubuntu.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
