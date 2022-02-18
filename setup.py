import platform

from setuptools import Extension, setup


def get_ext_modules() -> list:
    """
    获取三方模块

    Linux和Windows需要编译封装接口
    Mac由于缺乏二进制库支持无法使用
    """
    if platform.system() == "Linux":
        extra_compile_flags = [
            "-std=c++17",
            "-O3",
            "-Wno-delete-incomplete",
            "-Wno-sign-compare",
        ]
        extra_link_args = ["-lstdc++"]
        runtime_library_dirs = ["$ORIGIN"]
    else:
        extra_compile_flags = ["-O2", "-MT"]
        extra_link_args = []
        runtime_library_dirs = []

    vnrohonmd = Extension(
        "vnpy_rohon.api.vnrohonmd",
        [
            "vnpy_rohon/api/vnrohon/vnrohonmd/vnrohonmd.cpp",
        ],
        include_dirs=["vnpy_rohon/api/include",
                      "vnpy_rohon/api/vnrohon"],
        define_macros=[],
        undef_macros=[],
        library_dirs=["vnpy_rohon/api/libs", "vnpy_rohon/api"],
        libraries=["thostmduserapi_se", "thosttraderapi_se"],
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        depends=[],
        language="cpp",
    )

    vnrohontd = Extension(
        "vnpy_rohon.api.vnrohontd",
        [
            "vnpy_rohon/api/vnrohon/vnrohontd/vnrohontd.cpp",
        ],
        include_dirs=["vnpy_rohon/api/include",
                      "vnpy_rohon/api/vnrohon"],
        define_macros=[],
        undef_macros=[],
        library_dirs=["vnpy_rohon/api/libs", "vnpy_rohon/api"],
        libraries=["thostmduserapi_se", "thosttraderapi_se"],
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        depends=[],
        language="cpp",
    )

    return [vnrohontd, vnrohonmd]


setup(
    ext_modules=get_ext_modules(),
)
