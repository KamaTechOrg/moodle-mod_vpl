#include <pybind11/pybind11.h>
#include <chrono>
#include <unistd.h>
#include <cstring>
#include <fcntl.h>

#include <linux/perf_event.h>
#include <asm/unistd.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <cerrno>
#include <cstdint>
#include <iostream>

int perf_event_open(struct perf_event_attr* hw_event, pid_t pid, int cpu, int group_fd, unsigned long flags) {
    return syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
}

int startPerfCounting(pid_t pid) {
    struct perf_event_attr pe{};
    memset(&pe, 0, sizeof(struct perf_event_attr));
    pe.type = PERF_TYPE_HARDWARE;
    pe.size = sizeof(struct perf_event_attr);
    pe.config = PERF_COUNT_HW_INSTRUCTIONS;
    pe.disabled = 1;
    pe.exclude_kernel = 1;
    pe.exclude_hv = 1;

    int fd = perf_event_open(&pe, pid, -1, -1, 0);
    if (fd == -1) {
        std::cerr << "Error opening perf event: " << strerror(errno) << std::endl;
        return -1;
    }

    ioctl(fd, PERF_EVENT_IOC_RESET, 0);
    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
    return fd;
}

uint64_t stopPerfCounting(int fd) {
    ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
    uint64_t count = 0;
    read(fd, &count, sizeof(count));
    close(fd);
    return count;
}


namespace py = pybind11;

static std::chrono::high_resolution_clock::time_point start_time;

void start_measurement() {
    start_time = std::chrono::high_resolution_clock::now();
}

void end_measurement() {
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    long long duration_us = duration.count();

    char buf[32];
    std::snprintf(buf, sizeof(buf), "%lld\n", duration_us);

    if (fcntl(3, F_GETFD) == -1) {
        return;
    }

    ssize_t bytes_written = write(3, buf, std::strlen(buf));
    (void)bytes_written; 
    fsync(3);
}

PYBIND11_MODULE(measure, m) {
    m.def("start_measurement", &start_measurement, "Start the measurement");
    m.def("end_measurement", &end_measurement, "End the measurement and write elapsed time to pipe");
}