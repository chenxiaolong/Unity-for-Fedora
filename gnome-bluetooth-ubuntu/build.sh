#!/usr/bin/env bash

SPECFILE=gnome-bluetooth-ubuntu.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
