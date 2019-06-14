#!/bin/bash
docker run --name format2_0 --privileged \
	-v /var/log/psdctf/format2_0:/var/log/nsjail:rw \
        -d psdctf/format2_0
