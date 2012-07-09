#!/usr/bin/env bash

SPECFILE=unity-scope-video-remote.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
