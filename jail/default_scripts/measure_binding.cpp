#include <pybind11/pybind11.h>
#include <chrono>
#include <unistd.h>
#include <cstring>
#include <fcntl.h>

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
    (void)bytes_written; // Suppress unused variable warning
    fsync(3);
}

PYBIND11_MODULE(measure, m) {
    m.def("start_measurement", &start_measurement, "Start the measurement");
    m.def("end_measurement", &end_measurement, "End the measurement and write elapsed time to pipe");
}