#!/usr/bin/env bash

SPECFILE=unity-lens-videos.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
