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

WORKDIR /app/api/

COPY requirements.txt . 
COPY /api/api.py .
COPY /api/service.py .

RUN pip3 install -r requirements.txt

ENV LC_ALL=C.UTF-8 
ENV LANG=C.UTF-8
EXPOSE 80
CMD ["uvicorn", "api:app", "--host=0.0.0.0", "--port=80"]
