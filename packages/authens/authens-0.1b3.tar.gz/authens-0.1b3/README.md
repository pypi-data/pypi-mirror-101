# AuthENS

Librairie Django pour l'authentification via le CAS élèves à l'ENS.

AuthENS fournit une page de connexion qui laisse le choix entre "Connexion par
CAS" et "Connexion par mot de passe".
De plus, elle gère de façon transparente les potentiels "conflits" de `username`
liés aux comptes Django standards non-CAS (1) et aux vieux comptes clippers (2).
Plus précisément :

1. Si un compte clipper `dupond` est créé alors qu'un compte Django standard
   avec le `username` `dupond` existait déjà, le compte nouvellement créé
   obtient un `username` différent (typiquement `dupond2`).
   La personne détentrice du compte continue de se connecter en tant que
   `dupond` sur le CAS élèves mais devra utiliser le nom `dupond2` lorsqu'elle
   choisira d'utiliser la connexion par mot de passe sur le site, typiquement
   après la fin de la scolarité lorsque le compte clipper est supprimé.

2. Si, quelques années plus tard, après que `dupond` a terminé sa scolarité, le
   SPI donne le login `dupond` à une nouvelle personne, AuthENS détecte que le
   nouveau compte `dupond` n'est pas le même que l'ancien et crée un nouveau
   compte (par exemple `dupond3`).
   Le compte `dupond3` peut se connecter par CAS en tant que `dupond` et le
   compte `dupond2` ne peut plus se connecter que par mot de passe.


## Configuration

### Urls

Vous devez rendre les pages de connexion de AuthENS accessibles, par exemple en
ajoutant dans votre fichier d'urls :

```python
urlpatterns = [
  ...
  path("authens/", include("authens.urls")),
  ...
]
```

La page de connexion principale de AuthENS est ensuite accessible via l'url
nommée `authens:login`.
La page de déconnexion est `authens:logout`, il est important d'utiliser cette
vue est non la vue de déconnexion par défaut de Django pour déconnecter du CAS
en plus du site.

### Dans le fichier `settings.py`

- Ajouter `"authens"` dans les [`INSTALLED_APPS`](https://docs.djangoproject.com/en/3.0/ref/settings/#installed-apps).
- Ajouter `"authens.backends.ENSCASBackend"` dans les
  [`AUTHENTICATION_BACKENDS`](https://docs.djangoproject.com/en/3.0/ref/settings/#authentication-backends).
  Si `AUTHENTICATION_BACKENDS` n'apparaît pas dans vos settings, utiliser :

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authens.backends.ENSCASBackend",
]
```

- Préciser l'url de connexion:

```python
LOGIN_URL = reverse_lazy("authens:login")
```

- (Optionnel) Par défaut AuthENS propose les 3 modes de connexion (CAS / Vieux
  compte CAS / mot de passe). Le mode de connexion "Vieux compte CAS" peut être
  désactivé en ajoutant :

```python
AUTHENS_USE_OLDCAS = False
```

- (Optionnel) AuthENS utilise le paramètre Django standard
  [`LOGIN_REDIRECT_URL`](https://docs.djangoproject.com/en/3.0/ref/settings/#login-redirect-url)
  par défaut pour rediriger l'utilisateurice en cas de connexion réussie.
  Il peut être utile de définir ce paramètre.


## Utilisation

À lire

### Création d'utilisateurices

AuthENS maintient une tables des comptes clipper connus.
Cette table est automatiquement mise à jour lors qu'une personne se connecte via
le CAS pour la première fois.
En revanche lorsqu'un nouveau compte est créé manuellement et que ce compte
correspond à un compte clipper, il faut enregistrer ce compte auprès d'AuthENS,
autrement le compte Django et le compte clipper seront considérés comme deux
comptes différents.
Authens fournit une fonction `register_cas_account` pour cela.

Exemple:

```python
from authens.shortcuts import register_cas_account
from django.http import HttpResponseRedirect
from yourapp.forms import UserCreationForm

def create_user_view(requests, cas_login: str):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            register_cas_account(user, cas_login)
            return HttpResponseRedirect("success.html")
    else:
        form = UserCreationForm()

    return render(request, "create_user.html", {"form": form}
```


## Utilisation avancée

### Migration depuis `django_cas_ng`

Pour migrer depuis `django_cas_ng`, il est recommandé de faire une
[data migration](https://docs.djangoproject.com/en/3.1/howto/writing-migrations/#migrating-data-between-third-party-apps)
et d'appliquer la fonction `register_cas_account` sur tou⋅tes les
utilisateurices.

Dans le cas où certain⋅es utilisateurices n'ont pas de clipper, on peut d'abord
tester leur existence dans le LDAP du SPI de la façon suivante:

```python
from authens.models impomrt CASAccount
from authens.shortcuts import fetch_cas_account

def migrate_user(user: User):
    # On regarde si `user` existe dans le LDAP du SPI
    ldap_info = fetch_cas_account(user.username)
    if ldap_info:
        # Si oui, on enregiste `user` en tant que compte CAS.
        # Les deux lignes suivantes sont équivalentes à appeler
        # `register_cas_account(user, user.username)` mais nous économisent une
        # requête au LDAP.
        entrance_year = ldap_info["entrance_year"]
        CASAccount.objects.create(
            user=user, cas_login=user.username, entrance_year=entrance_year
        )
```

### Utilisation des signaux

Authens émet le signal `authens.signals.post_cas_connect` à chaque fois qu'un
compte CAS se connecte. Le signal est envoyé avec les arguments suivants :

- `sender` : la classe Django utilisée pour stocker l'utilisateurice
  (vraisemblablement la class `User` par défaut);

- `instance` : l'utilisateurice concerné⋅e;

- `created` : un booléen valant `True` si l'utilisateurice vient d'être créé⋅e
  (première connexion);

- `cas_login` : le login CAS de la personne;

- `attributes` : un dictionnaire contenant des informations supplémentaires sur
  le compte, fournies par le CAS.
