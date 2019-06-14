FROM nsjail

RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y libc6:i386

ENV TIMEOUT 60

ENV CGROUP_CPU_MS_PER_SEC 100
ENV CGROUP_PIDS_MAX 8
ENV CGROUP_MEM_MAX 67108864

WORKDIR /app
COPY format2_0 flag /app/

CMD [ "-R", "/bin", \
      "-R", "/lib", \
      "-R", "/lib64", \
      "--", "/app/format2_0" \
]

