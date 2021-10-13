from setuptools import setup


setup(
    name="helper-codes",
    version=0.1,
    description="Helper function for the model interpretability discussions",
    zip_safe=False,  # Avoid eggs, to avoid complex handling of package data
    packages=["helper_codes"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
)
