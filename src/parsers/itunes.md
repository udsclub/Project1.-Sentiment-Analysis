### iTunes App Store Dataset
Для отримання відгуків використовувалося api з iTunes app for Windows, а саме методи

`GetReviews` - для отримання відгуків по конкретному `app_id` з `skip/take` пейджингом - `curl "https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?id=1001885753&startIndex=0&endIndex=100&displayable-kind=11&sort=4&appVersion=all" -H "X-Apple-Store-Front: 143441-1,32"` - тут `app_id=1001885753`

`GetTop` для отримання списку id всіх доступних жанрів `Games/Navigation/Music/...` та отримання по 200 `app_id` по заданому жанру в кожній з категорій top free/paid/grossing - `curl "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?id=25129&popId=38&genreId=6000&dataOnly=true" -H "User-Agent: iTunes/12.4.1 (Windows; Microsoft Windows 10.0 x64(Build 9200); x64) AppleWebKit/7601.6016.1000.1"`, наприклад `genreId=6000` - задає жанр books, а загальний діапазон genreId 6000-6023

`CountrySelector` - для отримання переліку можливих значеннь `X-Apple-Store-Front` header, який власне задає країну магазину - `curl "https://itunes.apple.com/WebObjects/MZStore.woa/wa/countrySelectorPage?dataOnly=True" -H "X-Apple-Store-Front: 143441-1,32"`
