Make sure to install dependencise for the right architecture

below is for x86_64

```shell
pip install -r requirements.txt --platform manylinux2014_x86_64 --target ./lib --only-binary=:all:

(cd lib; zip ../lambda_function.zip -r .)

zip lambda_function.zip -u main.py

zip lambda_function.zip -u books.json

chmod 755 lambda_function.zip
```
