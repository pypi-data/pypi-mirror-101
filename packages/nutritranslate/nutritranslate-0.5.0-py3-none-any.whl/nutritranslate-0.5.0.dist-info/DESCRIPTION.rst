# Use instructions

```python
from nutritranslate import nt
engTerm = nt.translate('energía')
```

# Publish new version
Update the version in setup.py
```bash
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

