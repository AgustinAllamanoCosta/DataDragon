FROM ubuntu:18.04 as ZKP

COPY zkp/install_deps.sh /app/
RUN /app/install_deps.sh

COPY zkp/CMakeLists.txt zkp/run_linter.sh zkp/CPPLINT.cfg /app/
COPY zkp/src /app/src
RUN mkdir -p /app/build/Release

WORKDIR /app/
RUN ./run_linter.sh

WORKDIR /app/build/Release

RUN cmake ../.. -DCMAKE_BUILD_TYPE=Release
RUN make -j4

COPY zkp/examples /app/examples
COPY zkp_quick_test.sh /app/
WORKDIR /app
