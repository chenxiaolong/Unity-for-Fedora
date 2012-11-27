#!/usr/bin/env bash

SPECFILE=xorg-x11-proto-ubuntu-devel-Fedora_$(rpm -E '%fedora').spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
