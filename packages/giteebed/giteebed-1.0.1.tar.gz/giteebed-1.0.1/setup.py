from setuptools import setup, find_packages

setup(
    name = 'giteebed',
    version = '1.0.1',
    keywords = 'A image bed based on gitee',
    description = 'A image bed based on gitee',
    license = 'Apache License',
    url = 'https://github.com/fogsong233/gitee-bed',
    author = 'fogsong',
    author_email = '2031602579@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ["requests"]
)
