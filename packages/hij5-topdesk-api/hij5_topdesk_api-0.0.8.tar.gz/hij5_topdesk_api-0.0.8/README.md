## Hoe update je dit ding?

1. Pas de versie aan in setup.cfg
1. Maak de `dist` folder leeg. 
1. `python -m build`
   Als je geen twine geinstalleerd hebt:
   `python -m pip install twine`
1. `python -m twine upload --skip-existing dist/*`
1. Gebruik als username `__token__` en als password de API token.