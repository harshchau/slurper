FROM lambci/lambda:build-python3.8

RUN mkdir -p /Users/harsh/git

WORKDIR /Users/harsh/git 

COPY ./slurper ./slurper
COPY ./chrome ./chrome 
##COPY ./slurper/requirements.txt .
RUN touch requirements.txt 
RUN echo 'file:///Users/harsh/git/slurper#egg=slurper' >> ./requirements.txt
# Install libffi-devel https://github.com/lambci/docker-lambda
#RUN yum -y install libffi-devel
##RUN yum install -y yum-utils rpmdevtools 
##RUN yum -y install libX11
#RUN yumdownloader libX11-1.6.7-2.amzn2.x86_64
#RUN mkdir tmpdir
#RUN cd tmpdir
#    cd /tmp \
##RUN yumdownloader libX11.x86_64
##RUN rpmdev-extract *rpm
##RUN mkdir -p /var/task
##RUN adduser ec2-user
##RUN chown ec2-user:ec2-user /var/task
#RUN cd /var/task
#RUN cd /tmp/libX11-1.6.7-2.amzn2.x86_64/usr/lib64
#RUN cd /var/task
#RUN zip -r9 /tmp/MyCodeWithLibraries.zip *
RUN pip install -r ./requirements.txt -t dist --upgrade
# Required for chromedriver 
#RUN cp /usr/lib64/libX11.so.6 dist 
##RUN /bin/cp /Users/harsh/git/libX11-1.6.7-2.amzn2.x86_64/usr/lib64/* dist   
RUN zip -r dist.zip ./dist/

#libX11.x86_64 0:1.6.7-2.amzn2 