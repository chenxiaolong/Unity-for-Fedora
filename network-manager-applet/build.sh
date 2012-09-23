#!/usr/bin/env bash

SPECFILE=network-manager-applet-ubuntu-Fedora_18.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
