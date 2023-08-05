import setuptools

with open ( "README.md" , "r" ) as fh :
    long_description = fh . read ()

setuptools . setup (
    name = "push_msg" ,
    version = "0.0.1" ,
    author = "Oliver Xu" ,
    author_email = "273601727@qq.com" ,
    description = "Push message to wechat" ,
    long_description = long_description ,
    long_description_content_type = "text/markdown" ,
    url = "https://blog.oliverxu.cn" ,
    packages = setuptools . find_packages (),
    classifiers = [
        "Programming Language :: Python :: 3" ,
        "License :: OSI Approved :: MIT License" ,
        "Operating System :: OS Independent" ,
    ],
)