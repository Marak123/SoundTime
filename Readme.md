# API Endpoints
----

#### Auths
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /api/auth/login | Logowanie do istniejącego użytkownika |
| POST | /api/auth/refresh | Wygeneruj nowy token identyfikacji |
| POST | /api/auth/logout | Wyloguj się |

#### Users
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| GET | /api/users/ | Pobierz listę wszystkich użytkowników |
| POST | /api/users/ | Tworzenie użytkownika |
| GET | /api/users/:id/ | Pobierz informacje o użytkowniku z :id |
| PUT | /api/users/:id/ | Modyfikuj informacje o użytkowniku z :id |
| PATCH | /api/users/:id/ | Modyfikuj pojedyńcze informacje o użytkowniku z :id |
| DELETE | /api/users/:id/ | Usuń użytkownika o :id |

#### Groups
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| GET | /api/groups | Pobierz listę wszystkich grup |
| POST | /api/group/add | Dodaj nową grupę |
| GET | /api/group/:id | Pobierz informacje o grupie z :id |
| DELETE | /api/group/:id | Usuń grupę z :id |
| PUT | /api/group/:id | Modyfikuj grupę z :id |

#### Songs
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| GET | /api/songs | Pobierz listę wszystkich piosenek |
| POST | /api/song/add | Dodaj nową piosenkę |
| GET | /api/song/:id | Pobierz informacje o piosence z :id |
| DELETE | /api/song/:id | Usuń piosenkę |
| PUT | /api/song/:id | Modyfikuj informacje o piosence |
| GET | /api/song/:id/play | Odtwórz piosenkę z :id |

<!-- #### Hours Of Playback
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| GET | /api/hours | Pobierz listę wszystkich piosenek | -->