# PySlovnik
> PySlovník je Python wrapper pro Internetovou jazykovou příručku od Ústavu pro jazyk český Akademie věd České republiky

PySlovník je zatím ještě v plenkách, očekávejte bugy.

Je to v podstatě web scraper který bere data z https://prirucka.ujc.cas.cz/ a transformuje je do použitelné podoby. Je to můj první projekt takového typu takže jakékoliv připomínky budou vítány.

## Instalace

```sh
$ pip install git+https://github.com/CrumblyLiquid/PySlovnik.git#egg=PySlovnik
```


## Použití

```py
    slova = Slovnik().hledat("jak")
    for slovo in slova:
        print(f"{slovo.slovo} ({slovo.rod}): {slovo.vyznam}")
```

## Příspěvky

Pokud najdete nějakou chybu nebo budete chtít něco přidat, otevřete si chybu nebo požádejte o PR. Každý kousek se cení!

## Licence

[GNU GPLv3](LICENSE)