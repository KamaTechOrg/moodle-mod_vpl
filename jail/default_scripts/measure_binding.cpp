#include <pybind11/pybind11.h>
#include <chrono>
#include <unistd.h>
#include <cstring>
#include <iostream>
#include <cstdio>

namespace py = pybind11;

static std::chrono::high_resolution_clock::time_point start_time;

void start_measurement() {
    start_time = std::chrono::high_resolution_clock::now();
    std::cerr << "DEBUG: start_measurement called\n";
}

void end_measurement() {
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    long long duration_us = duration.count();

    char buf[32];
    std::snprintf(buf, sizeof(buf), "%lld", duration_us);

    std::cerr << "DEBUG: About to write to fd=3: " << buf << "\n";

    ssize_t bytes_written = write(3, buf, std::strlen(buf));
    if (bytes_written < 0) {
        perror("DEBUG: write to time pipe failed");
    } else {
        std::cerr << "DEBUG: Wrote to time pipe: " << buf << " (" << bytes_written << " bytes)\n";
    }
}

PYBIND11_MODULE(measure, m) {
    m.doc() = "Python module for measurement functions";
    m.def("start_measurement", &start_measurement, "Start the measurement");
    m.def("end_measurement", &end_measurement, "End the measurement and write elapsed time to pipe");
}
